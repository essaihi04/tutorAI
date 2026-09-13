"""Serve media assets without exposing JSON drafts, scripts or internal files."""
from pathlib import Path
from starlette.exceptions import HTTPException
from starlette.staticfiles import StaticFiles


class PublicMediaFiles(StaticFiles):
    async def get_response(self, path, scope):
        if Path(path).suffix.lower() not in {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.avif', '.svg', '.pdf'}:
            raise HTTPException(404)
        response = await super().get_response(path, scope)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        # Even a mislabeled uploaded SVG/HTML cannot run with the app's origin.
        response.headers['Content-Security-Policy'] = "sandbox; default-src 'none'; style-src 'unsafe-inline'; img-src 'self' data:"
        return response
