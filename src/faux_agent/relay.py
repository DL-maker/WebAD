from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import hashlib
import uuid
import time
import mysql.connector
from collections import defaultdict

DB = {
    "host":     "localhost",
    "database": "linuxad",
    "user":     "root",
    "password": "root"
}

test = defaultdict(list)

def get_conn():
    return mysql.connector.connect(**DB)

def sha256(s):
    return hashlib.sha256(s.encode()).hexdigest()

def faux_jwt(username, role):
    return f"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.{sha256(username + role)[:32]}"

def json_response(handler, code, data):
    body = json.dumps(data, ensure_ascii=False, default=str).encode("utf-8")
    handler.send_response(code)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", len(body))
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.end_headers()
    handler.wfile.write(body)

# ── Routes ────────────────────────────────────────────────────
def handle_login(handler, body):
    username = body.get("username", "")
    password = body.get("password", "")
    mfa_code = body.get("mfa_code")

    # Rate limiting
    now = time.time()
    test[username] = [t for t in test[username] if now - t < 60]
    if len(test[username]) >= 5:
        return json_response(handler, 429, {"error": {"code": "RATE_LIMITED", "message": "Trop de tentatives (5/min)"}})
    test[username].append(now)

    # Vérifie en DB
    conn = get_conn()
    cur  = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM admin_users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if not user or user["password_hash"] != sha256(password):
        return json_response(handler, 401, {"error": {"code": "INVALID_CREDENTIALS", "message": "Identifiants incorrects"}})

    if user["mfa_enabled"] and not mfa_code:
        return json_response(handler, 401, {"error": {"code": "MFA_REQUIRED", "message": "Code MFA requis mais absent"}})

    if user["mfa_enabled"] and mfa_code and len(str(mfa_code)) != 6:
        return json_response(handler, 401, {"error": {"code": "INVALID_MFA", "message": "Code MFA invalide"}})

    # Update last_login
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("UPDATE admin_users SET last_login = NOW() WHERE id = %s", (user["id"],))
    conn.commit()
    cur.close()
    conn.close()

    access_token  =faux_jwt(username, user["role"])
    refresh_token = f"linuxad_refresh_1_{sha256(username)[:12]}"

    json_response(handler, 200, {
        "access_token":  access_token,
        "token_type":    "bearer",
        "expires_in":    3600,
        "refresh_token": refresh_token,
        "user": {
            "id":         str(user["id"]),
            "username":   user["username"],
            "email":      user["email"],
            "role":       user["role"],
            "last_login": str(user["last_login"]) if user["last_login"] else None
        }
    })


def handle_machines(handler):
    conn = get_conn()
    cur  = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT m.id, m.hostname, m.fqdn, m.status, m.os_version,
               m.last_contact, a.status AS agent_status, a.ip_address
        FROM machines m
        LEFT JOIN agents a ON a.machine_id = m.id
        ORDER BY m.hostname
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    json_response(handler, 200, {"data": rows, "pagination": {"total": len(rows), "page": 1, "per_page": 20}})


def handle_users(handler):
    conn = get_conn()
    cur  = conn.cursor(dictionary=True)
    cur.execute("SELECT uid, cn, email, uid_number, home_directory, login_shell FROM users ORDER BY uid_number")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    json_response(handler, 200, {"data": rows, "pagination": {"total": len(rows), "page": 1, "per_page": 20}})


def handle_gpo(handler):
    conn = get_conn()
    cur  = conn.cursor(dictionary=True)
    cur.execute("SELECT id, name, description, version, status, updated_at FROM gpo ORDER BY updated_at DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    json_response(handler, 200, {"data": rows, "pagination": {"total": len(rows), "page": 1, "per_page": 20}})


class RelayHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        print(f"=> {self.command} {self.path} {args[1]}")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body   = json.loads(self.rfile.read(length)) if length else {}

        if self.path == "/api/v1/admin/auth/login":
            handle_login(self, body)
        else:
            json_response(self, 404, {"error": {"code": "NOT_FOUND", "message": f"Route {self.path} introuvable"}})

    def do_GET(self):
        if self.path.startswith("/api/v1/admin/machines"):
            handle_machines(self)
        elif self.path.startswith("/api/v1/admin/users"):
            handle_users(self)
        elif self.path.startswith("/api/v1/admin/gpo"):
            handle_gpo(self)
        else:
            json_response(self, 404, {"error": {"code": "NOT_FOUND", "message": f"Route {self.path} introuvable"}})


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 4444), RelayHandler)
    print(f"Relay démarré sur http://127.0.0.1:4444")
    print(f"POST /api/v1/admin/auth/login")
    print(f"GET  /api/v1/admin/machines")
    print(f"GET  /api/v1/admin/users")
    print(f"GET  /api/v1/admin/gpo")
    server.serve_forever()

