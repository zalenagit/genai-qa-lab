"""ZY Demo Store - a tiny, self-contained web app + REST API used as the system under test.

Runs with the Python standard library only, so tests work offline and in CI
without depending on public demo sites.

    python -m app.server --port 8000
"""
import argparse
import json
import re
import secrets
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

STATIC_DIR = Path(__file__).parent / "static"
TAX_RATE = 0.08

USERS = {
    "standard_user": {"password": "secret123", "locked": False},
    "locked_user": {"password": "secret123", "locked": True},
}

PRODUCTS = [
    {"id": 1, "name": "Noise-Cancelling Headset", "price": 79.99},
    {"id": 2, "name": "USB-C Charging Dock", "price": 49.50},
    {"id": 3, "name": "Mechanical Keyboard", "price": 119.00},
    {"id": 4, "name": "1080p Webcam", "price": 59.25},
]


class Store:
    """In-memory, thread-safe state. Reset between test sessions with reset()."""

    def __init__(self):
        self.lock = threading.Lock()
        self.reset()

    def reset(self):
        with self.lock:
            self.tokens = {}
            self.orders = {}
            self.next_order_id = 1001


STORE = Store()


def product_by_id(pid):
    return next((p for p in PRODUCTS if p["id"] == pid), None)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def log_message(self, fmt, *args):  # keep test output clean
        pass

    # ---------- helpers ----------
    def _json(self, status, body=None):
        payload = b"" if body is None else json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        if payload:
            self.wfile.write(payload)

    def _body(self):
        length = int(self.headers.get("Content-Length") or 0)
        if not length:
            return {}
        try:
            data = json.loads(self.rfile.read(length))
            return data if isinstance(data, dict) else None
        except json.JSONDecodeError:
            return None

    def _user(self):
        auth = self.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return None
        return STORE.tokens.get(auth[7:])

    # ---------- routes ----------
    def do_GET(self):
        if self.path == "/api/health":
            return self._json(200, {"status": "ok"})
        if self.path == "/api/products":
            return self._json(200, PRODUCTS)
        m = re.fullmatch(r"/api/products/(\d+)", self.path)
        if m:
            p = product_by_id(int(m.group(1)))
            return self._json(200, p) if p else self._json(404, {"error": "Product not found"})
        m = re.fullmatch(r"/api/orders/(\d+)", self.path)
        if m:
            user = self._user()
            if not user:
                return self._json(401, {"error": "Authentication required"})
            order = STORE.orders.get(int(m.group(1)))
            if not order or order["username"] != user:
                return self._json(404, {"error": "Order not found"})
            return self._json(200, order)
        if self.path.startswith("/api/"):
            return self._json(404, {"error": "Not found"})
        return super().do_GET()

    def do_POST(self):
        body = self._body()
        if body is None:
            return self._json(400, {"error": "Body must be a JSON object"})

        if self.path == "/api/login":
            username = (body.get("username") or "").strip()
            password = body.get("password") or ""
            if not username:
                return self._json(400, {"error": "Username is required"})
            if not password:
                return self._json(400, {"error": "Password is required"})
            user = USERS.get(username)
            if not user or user["password"] != password:
                return self._json(401, {"error": "Invalid username or password"})
            if user["locked"]:
                return self._json(423, {"error": "This account is locked"})
            token = secrets.token_hex(16)
            with STORE.lock:
                STORE.tokens[token] = username
            return self._json(200, {"token": token, "username": username})

        if self.path == "/api/orders":
            user = self._user()
            if not user:
                return self._json(401, {"error": "Authentication required"})
            items = body.get("items")
            customer = body.get("customer") or {}
            if not isinstance(items, list) or not items:
                return self._json(400, {"error": "At least one item is required"})
            for field in ("first_name", "last_name", "zip"):
                if not str(customer.get(field, "")).strip():
                    return self._json(400, {"error": f"{field} is required"})
            if not re.fullmatch(r"\d{5}", str(customer["zip"])):
                return self._json(400, {"error": "zip must be 5 digits"})
            subtotal = 0.0
            for item in items:
                p = product_by_id(item.get("product_id"))
                qty = item.get("qty", 1)
                if not p:
                    return self._json(400, {"error": f"Unknown product_id {item.get('product_id')}"})
                if not isinstance(qty, int) or not 1 <= qty <= 10:
                    return self._json(400, {"error": "qty must be an integer from 1 to 10"})
                subtotal += p["price"] * qty
            tax = round(subtotal * TAX_RATE, 2)
            with STORE.lock:
                oid = STORE.next_order_id
                STORE.next_order_id += 1
                order = {"id": oid, "username": user, "items": items, "customer": customer,
                         "subtotal": round(subtotal, 2), "tax": tax,
                         "total": round(subtotal + tax, 2), "status": "created"}
                STORE.orders[oid] = order
            return self._json(201, order)

        return self._json(404, {"error": "Not found"})

    def do_DELETE(self):
        m = re.fullmatch(r"/api/orders/(\d+)", self.path)
        if not m:
            return self._json(404, {"error": "Not found"})
        user = self._user()
        if not user:
            return self._json(401, {"error": "Authentication required"})
        oid = int(m.group(1))
        with STORE.lock:
            order = STORE.orders.get(oid)
            if not order or order["username"] != user:
                return self._json(404, {"error": "Order not found"})
            del STORE.orders[oid]
        return self._json(204)


def start_server(port=0):
    """Start the app in a background thread. Returns (server, base_url)."""
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_address[1]}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    srv = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"ZY Demo Store running at http://127.0.0.1:{args.port}")
    srv.serve_forever()
