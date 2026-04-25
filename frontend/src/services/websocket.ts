/**
 * WebSocket service for real-time voice pipeline communication.
 */

type MessageHandler = (data: any) => void;

export class WebSocketService {
  private ws: WebSocket | null = null;
  private handlers: Map<string, MessageHandler[]> = new Map();
  private connectTimer: ReturnType<typeof setTimeout> | null = null;
  private connectGeneration = 0;

  connect(token: string, retries = 2): Promise<void> {
    // Cancel any pending connect from a previous call
    if (this.connectTimer) {
      clearTimeout(this.connectTimer);
      this.connectTimer = null;
    }
    const gen = ++this.connectGeneration;

    return new Promise((resolve, reject) => {
      const attempt = (remaining: number) => {
        if (gen !== this.connectGeneration) return; // stale call

        // Close previous connection and wait briefly for backend cleanup
        if (this.ws) {
          try {
            this.ws.onclose = null;
            this.ws.onerror = null;
            this.ws.onmessage = null;
            this.ws.onopen = null;
            this.ws.close();
          } catch {}
          this.ws = null;
        }

        const doConnect = () => {
          if (gen !== this.connectGeneration) return; // stale call
          this.connectTimer = null;

          // Use relative URL so Vite proxy forwards /ws to backend
          const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
          const host = window.location.host;
          this.ws = new WebSocket(`${protocol}//${host}/ws/tutor/${token}`);

          this.ws.onopen = () => {
            if (gen !== this.connectGeneration) {
              // Stale connection — close it silently
              try { this.ws?.close(); } catch {}
              return;
            }
            resolve();
          };

          this.ws.onmessage = (event) => {
            try {
              const data = JSON.parse(event.data);
              const handlers = this.handlers.get(data.type) || [];
              handlers.forEach((handler) => handler(data));

              // Also notify 'all' handlers
              const allHandlers = this.handlers.get('all') || [];
              allHandlers.forEach((handler) => handler(data));
            } catch {
              // Binary data (audio)
              const handlers = this.handlers.get('binary') || [];
              handlers.forEach((handler) => handler(event.data));
            }
          };

          this.ws.onerror = (error) => {
            if (gen !== this.connectGeneration) return;
            if (remaining > 0) {
              console.warn(`[WebSocket] Connection failed, retrying (${remaining} left)...`);
              this.connectTimer = setTimeout(() => attempt(remaining - 1), 1000);
            } else {
              reject(error);
            }
          };

          this.ws.onclose = (event) => {
            // Surface the close code/reason so the UI can differentiate
            // normal disconnects from auth expirations (code 4001).
            const payload = { code: event.code, reason: event.reason };
            const handlers = this.handlers.get('disconnected') || [];
            handlers.forEach((handler) => handler(payload));
            if (event.code === 4001) {
              const authHandlers = this.handlers.get('auth_expired') || [];
              authHandlers.forEach((handler) => handler(payload));
            }
          };
        };

        // Small delay to let backend fully release previous connection
        this.connectTimer = setTimeout(doConnect, 50);
      };

      attempt(retries);
    });
  }

  on(type: string, handler: MessageHandler): void {
    if (!this.handlers.has(type)) {
      this.handlers.set(type, []);
    }
    this.handlers.get(type)!.push(handler);
  }

  clearHandlers(): void {
    this.handlers.clear();
  }

  off(type: string, handler: MessageHandler): void {
    const handlers = this.handlers.get(type);
    if (handlers) {
      const idx = handlers.indexOf(handler);
      if (idx !== -1) handlers.splice(idx, 1);
    }
  }

  sendJson(data: object): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      console.log('[WebSocket] Sending message:', data);
      this.ws.send(JSON.stringify(data));
    } else {
      console.error('[WebSocket] Cannot send - not connected. ReadyState:', this.ws?.readyState);
    }
  }

  sendAudio(audioBlob: Blob): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      audioBlob.arrayBuffer().then((buffer) => {
        this.ws!.send(buffer);
      });
    }
  }

  disconnect(): void {
    // Invalidate any in-flight connect attempts
    this.connectGeneration++;
    if (this.connectTimer) {
      clearTimeout(this.connectTimer);
      this.connectTimer = null;
    }
    if (this.ws) {
      try {
        this.ws.onclose = null;
        this.ws.onerror = null;
        this.ws.onmessage = null;
        this.ws.onopen = null;
        this.ws.close();
      } catch {}
      this.ws = null;
    }
  }

  get isConnected(): boolean {
    return this.ws?.readyState === WebSocket.OPEN;
  }
}

export const wsService = new WebSocketService();
