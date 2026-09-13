"""Bound request sizes and request rates without trusting client-supplied IP headers.

Nginx adds shared limits across workers; this bounded local limiter also protects
direct ASGI access. No tokens, passwords or request bodies are logged.
"""
import time
from collections import OrderedDict
from starlette.responses import JSONResponse


class SecurityMiddleware:
    def __init__(self, app, max_clients=10000, clock=time.monotonic):
        self.app = app
        self.max_clients = max_clients
        self.clock = clock
        self.buckets = OrderedDict()

    def limited(self, key, limit, window):
        now = self.clock()
        count, reset = self.buckets.get(key, (0, now + window))
        if now >= reset:
            count, reset = 0, now + window
        # Existing blocked clients cannot evict their own history by retrying.
        self.buckets[key] = (count + 1, reset)
        self.buckets.move_to_end(key)
        while len(self.buckets) > self.max_clients:
            self.buckets.popitem(last=False)
        return max(1, int(reset - now) + 1) if count >= limit else 0

    async def __call__(self, scope, receive, send):
        if scope['type'] != 'http':
            return await self.app(scope, receive, send)
        path = scope.get('path', '').rstrip('/')
        if not path.startswith('/api/'):
            return await self.app(scope, receive, send)
        method = scope.get('method', 'GET')
        client = (scope.get('client') or ('unknown', 0))[0]
        if method != 'OPTIONS':
            limit, window = 240, 60
            if path == '/api/v1/admin/login':
                limit = 8
            elif path in ('/api/v1/auth/login', '/api/v1/auth/refresh'):
                limit = 20
            elif path == '/api/v1/registration-requests' and method == 'POST':
                limit, window = 5, 3600
            elif path == '/api/v1/concours/chat':
                limit = 10
            elif path == '/api/v1/coaching/bac-diagnostic/questions':
                limit = 10
            retry = self.limited((client, path), limit, window)
            # Bound aggregate requests too; changing path cannot bypass this.
            retry = max(retry, self.limited((client, 'all-api'), 600, 60))
            if retry:
                return await JSONResponse({'detail': 'Trop de requêtes. Réessayez plus tard.'},
                    status_code=429, headers={'Retry-After': str(retry)})(scope, receive, send)
        max_body = 25 * 1024 * 1024 if any(x in path for x in ('upload', 'exam-extract', '/courses')) else 1024 * 1024
        if path in ('/api/v1/exam/extract-text', '/api/v1/exam/evaluate',
                    '/api/v1/exam/save-progress', '/api/v1/exam/submit'):
            max_body = 8 * 1024 * 1024  # Bounded base64 photos and handwritten answers.
        length = dict(scope.get('headers', [])).get(b'content-length')
        if length:
            try:
                too_large = int(length) < 0 or int(length) > max_body
            except ValueError:
                too_large = True
            if too_large:
                return await JSONResponse({'detail': 'Requête trop volumineuse'}, status_code=413)(scope, receive, send)
        # Read before dispatch so chunked requests cannot bypass the body limit
        # or trigger a mutation with a partially accepted payload.
        body = bytearray()
        if method in ('POST', 'PUT', 'PATCH', 'DELETE'):
            while True:
                message = await receive()
                if message['type'] == 'http.disconnect':
                    return
                body.extend(message.get('body', b''))
                if len(body) > max_body:
                    return await JSONResponse({'detail': 'Requête trop volumineuse'}, status_code=413)(scope, receive, send)
                if not message.get('more_body', False):
                    break
            delivered = False

            async def replay():
                nonlocal delivered
                if not delivered:
                    delivered = True
                    return {'type': 'http.request', 'body': bytes(body), 'more_body': False}
                return await receive()
        else:
            replay = receive

        async def secure_send(message):
            if message['type'] == 'http.response.start':
                headers = [(k, v) for k, v in message.get('headers', []) if k.lower() != b'cache-control']
                headers.extend([(b'cache-control', b'no-store'), (b'x-content-type-options', b'nosniff')])
                message = {**message, 'headers': headers}
            await send(message)

        return await self.app(scope, replay, secure_send)
