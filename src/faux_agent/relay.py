from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import hashlib
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from collections import defaultdict

DB = {
    "host":     "localhost",
    "dbname":   "linuxad",
    "user":     "postgres",
    "password": "root"
}

test = defaultdict(list)

def get_conn():
    return psycopg2.connect(**DB)

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

def empty_response(handler, code):
    handler.send_response(code)
    handler.send_header("Content-Length", "0")
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.end_headers()

# ── Routes ────────────────────────────────────────────────────

def handle_login(handler, body):
    username = body.get("username", "")
    password = body.get("password", "")
    mfa_code = body.get("mfa_code")

    now = time.time()
    test[username] = [t for t in test[username] if now - t < 60]
    if len(test[username]) >= 5:
        return json_response(handler, 429, {"error": {"code": "RATE_LIMITED", "message": "Trop de tentatives (5/min)"}})
    test[username].append(now)

    conn = get_conn()
    cur  = conn.cursor(cursor_factory=RealDictCursor)
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

    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("UPDATE admin_users SET last_login = NOW() WHERE id = %s", (user["id"],))
    conn.commit()
    cur.close()
    conn.close()

    access_token  = faux_jwt(username, user["role"])
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


def handle_refresh(handler, body):
    refresh_token = body.get("refresh_token", "")

    if not refresh_token.startswith("linuxad_refresh_1_"):
        return json_response(handler, 401, {"error": {"code": "INVALID_TOKEN", "message": "Refresh token invalide"}})

    token_hash = refresh_token.replace("linuxad_refresh_1_", "")

    conn = get_conn()
    cur  = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM admin_users")
    users = cur.fetchall()
    cur.close()
    conn.close()

    user = next((u for u in users if sha256(u["username"])[:12] == token_hash), None)

    if not user:
        return json_response(handler, 401, {"error": {"code": "INVALID_TOKEN", "message": "Refresh token invalide"}})

    json_response(handler, 200, {
        "access_token": faux_jwt(user["username"], user["role"]),
        "token_type":   "bearer",
        "expires_in":   3600
    })


def handle_logout(handler, body):
    # Dans un vrai systeme on invaliderait le token en DB
    empty_response(handler, 204)


def handle_machines(handler):
    conn = get_conn()
    cur  = conn.cursor(cursor_factory=RealDictCursor)
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
    cur  = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT uid, cn, email, uid_number, home_directory, login_shell FROM users ORDER BY uid_number")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    json_response(handler, 200, {"data": rows, "pagination": {"total": len(rows), "page": 1, "per_page": 20}})


def handle_gpo(handler):
    conn = get_conn()
    cur  = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, name, description, version, status, updated_at FROM gpo ORDER BY updated_at DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    json_response(handler, 200, {"data": rows, "pagination": {"total": len(rows), "page": 1, "per_page": 20}})


def handle_groups(handler):
    conn = get_conn()
    cur  = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT id, name, description, ldap_dn FROM "groups" ORDER BY name')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    json_response(handler, 200, {"data": rows, "pagination": {"total": len(rows), "page": 1, "per_page": 20}})


def handle_dashboard_stats(handler):
    conn = get_conn()
    cur  = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT status, COUNT(*) as count FROM machines GROUP BY status")
    machine_rows = {r["status"]: r["count"] for r in cur.fetchall()}

    cur.execute("SELECT status, COUNT(*) as count FROM agents GROUP BY status")
    agent_rows = {r["status"]: r["count"] for r in cur.fetchall()}

    cur.execute("SELECT COUNT(*) as count FROM users")
    user_count = cur.fetchone()["count"]

    cur.execute('SELECT COUNT(*) as count FROM "groups"')
    group_count = cur.fetchone()["count"]

    cur.execute("SELECT status, COUNT(*) as count FROM gpo GROUP BY status")
    gpo_rows = {r["status"]: r["count"] for r in cur.fetchall()}

    cur.execute("SELECT action, resource_type, timestamp FROM audit_logs ORDER BY timestamp DESC LIMIT 5")
    recent = cur.fetchall()

    cur.close()
    conn.close()

    json_response(handler, 200, {
        "machines": {
            "total":    sum(machine_rows.values()),
            "active":   machine_rows.get("active", 0),
            "inactive": machine_rows.get("inactive", 0),
            "pending":  machine_rows.get("pending", 0),
        },
        "agents": {
            "online":  agent_rows.get("online", 0),
            "offline": agent_rows.get("offline", 0),
        },
        "users":  {"total": user_count},
        "groups": {"total": group_count},
        "gpo": {
            "total":    sum(gpo_rows.values()),
            "active":   gpo_rows.get("active", 0),
            "draft":    gpo_rows.get("draft", 0),
            "archived": gpo_rows.get("archived", 0),
        },
        "recent_activity": [
            {"type": r["action"], "message": f"{r['action']} on {r['resource_type']}", "timestamp": str(r["timestamp"])}
            for r in recent
        ],
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    })


# ── Enrollment ───────────────────────────────────────────────

def handle_enrollment_tokens_create(handler, body):
    import uuid as _uuid
    from datetime import datetime, timedelta

    description     = body.get("description", "")
    max_uses        = body.get("max_uses", 10)
    expires_in_hours= body.get("expires_in_hours", 24)
    allowed_groups  = body.get("allowed_groups", [])

    if not isinstance(max_uses, int) or not (1 <= max_uses <= 1000):
        return json_response(handler, 400, {"error": {"code": "VALIDATION_ERROR", "message": "max_uses doit etre entre 1 et 1000"}})
    if not isinstance(expires_in_hours, int) or not (1 <= expires_in_hours <= 720):
        return json_response(handler, 400, {"error": {"code": "VALIDATION_ERROR", "message": "expires_in_hours doit etre entre 1 et 720"}})

    token_id    = str(_uuid.uuid4())
    token_plain = f"linuxad_enroll_1_{sha256(token_id)[:24]}"
    token_hash  = sha256(token_plain)
    expires_at  = datetime.now() + timedelta(hours=expires_in_hours)

    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("""
        INSERT INTO enrollment_tokens (id, token_hash, description, max_uses, current_uses, expires_at, status, created_by)
        VALUES (%s, %s, %s, %s, 0, %s, 'active', 'admin')
    """, (token_id, token_hash, description, max_uses, expires_at))
    conn.commit()
    cur.close()
    conn.close()

    json_response(handler, 201, {
        "id":           token_id,
        "token":        token_plain,
        "description":  description,
        "max_uses":     max_uses,
        "current_uses": 0,
        "allowed_groups": allowed_groups,
        "expires_at":   expires_at.isoformat() + "Z",
        "created_at":   time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "created_by":   "admin"
    })


def handle_enrollment_tokens_list(handler):
    conn = get_conn()
    cur  = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, description, max_uses, current_uses, expires_at, status, created_by, created_at FROM enrollment_tokens ORDER BY created_at DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    json_response(handler, 200, {
        "data": rows,
        "pagination": {"page": 1, "per_page": 20, "total": len(rows), "total_pages": 1, "has_next": False, "has_prev": False}
    })


def handle_enrollment_token_delete(handler, token_id):
    conn = get_conn()
    cur  = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM enrollment_tokens WHERE id = %s", (token_id,))
    token = cur.fetchone()

    if not token:
        cur.close()
        conn.close()
        return json_response(handler, 404, {"error": {"code": "NOT_FOUND", "message": "Token non trouve"}})

    if token["status"] == "revoked":
        cur.close()
        conn.close()
        return json_response(handler, 409, {"error": {"code": "CONFLICT", "message": "Token deja revoque"}})

    cur2 = conn.cursor()
    cur2.execute("UPDATE enrollment_tokens SET status = 'revoked' WHERE id = %s", (token_id,))
    conn.commit()
    cur.close()
    cur2.close()
    conn.close()

    json_response(handler, 200, {
        "id":         token_id,
        "status":     "revoked",
        "revoked_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "revoked_by": "admin"
    })


def handle_enroll(handler, body):
    import uuid as _uuid
    from datetime import datetime

    enrollment_token = body.get("enrollment_token", "")
    hostname         = body.get("hostname", "")
    fqdn             = body.get("fqdn", "")
    os_info          = body.get("os_info", {})
    agent_version    = body.get("agent_version", "1.0.0")

    if not all([enrollment_token, hostname, fqdn, os_info]):
        return json_response(handler, 400, {"error": {"code": "VALIDATION_ERROR", "message": "Champs requis manquants"}})

    token_hash = sha256(enrollment_token)

    conn = get_conn()
    cur  = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM enrollment_tokens WHERE token_hash = %s AND status = 'active'", (token_hash,))
    token = cur.fetchone()

    if not token:
        cur.close()
        conn.close()
        return json_response(handler, 401, {"error": {"code": "INVALID_TOKEN", "message": "Token invalide, expire ou revoque"}})

    if token["current_uses"] >= token["max_uses"]:
        cur.close()
        conn.close()
        return json_response(handler, 429, {"error": {"code": "RATE_LIMITED", "message": "Token epuise (max_uses atteint)"}})

    cur.execute("SELECT id FROM machines WHERE fqdn = %s", (fqdn,))
    if cur.fetchone():
        cur.close()
        conn.close()
        return json_response(handler, 409, {"error": {"code": "CONFLICT", "message": "Machine deja enrolee (meme FQDN)"}})

    machine_id  = str(_uuid.uuid4())
    agent_id    = str(_uuid.uuid4())
    agent_secret = f"linuxad_secret_1_{sha256(agent_id)[:24]}"

    cur2 = conn.cursor()
    cur2.execute("""
        INSERT INTO machines (id, hostname, fqdn, os_version, kernel_version, status, enrolled_at, last_contact)
        VALUES (%s, %s, %s, %s, %s, 'active', NOW(), NOW())
    """, (machine_id, hostname, fqdn,
          f"{os_info.get('distribution','')} {os_info.get('version','')}",
          os_info.get("kernel", "")))

    cur2.execute("""
        INSERT INTO agents (id, machine_id, secret_hash, status, enrolled_at, last_seen, ip_address, agent_version)
        VALUES (%s, %s, %s, 'online', NOW(), NOW(), %s, %s)
    """, (agent_id, machine_id, sha256(agent_secret),
          body.get("network_info", {}).get("primary_ip", ""),
          agent_version))

    cur2.execute("UPDATE enrollment_tokens SET current_uses = current_uses + 1 WHERE id = %s", (token["id"],))
    conn.commit()
    cur.close()
    cur2.close()
    conn.close()

    json_response(handler, 201, {
        "machine_id":       machine_id,
        "agent_id":         agent_id,
        "agent_secret":     agent_secret,
        "server_public_key": "-----BEGIN PUBLIC KEY-----\nMCowBQYDK2VwAyEA_MOCK_KEY\n-----END PUBLIC KEY-----",
        "api_endpoint":     "http://127.0.0.1:4444/api/v1",
        "polling_interval": 60,
        "enrolled_at":      time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "assigned_groups":  []
    })


# ── Agent ─────────────────────────────────────────────────────

def handle_agent_poll(handler, body):
    agent_id = body.get("agent_id", "")
    status   = body.get("status", {})

    if not agent_id:
        return json_response(handler, 400, {"error": {"code": "VALIDATION_ERROR", "message": "agent_id requis"}})
    conn = get_conn()
    cur  = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM agents WHERE id = %s", (agent_id,))
    agent = cur.fetchone()

    if not agent:
        cur.close()
        conn.close()
        return json_response(handler, 401, {"error": {"code": "INVALID_SIGNATURE", "message": "Agent inconnu"}})

    # Update last_seen et status
    cur2 = conn.cursor()
    cur2.execute("UPDATE agents SET last_seen = NOW(), status = 'online' WHERE id = %s", (agent_id,))
    cur2.execute("UPDATE machines SET last_contact = NOW() WHERE id = %s", (agent["machine_id"],))
    conn.commit()
    cur.close()
    cur2.close()
    conn.close()
    json_response(handler, 200, {
        "commands":          [],
        "gpo_updates":       [],
        "gpo_removals":      [],
        "next_poll_interval": 60,
        "server_time":       time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "rotate_secret":     False,
        "new_secret":        None
    })


def handle_agent_logs(handler, body):
    agent_id = body.get("agent_id", "")
    logs     = body.get("logs", [])

    if not agent_id:
        return json_response(handler, 400, {"error": {"code": "VALIDATION_ERROR", "message": "agent_id requis"}})

    if len(logs) > 100:
        return json_response(handler, 400, {"error": {"code": "VALIDATION_ERROR", "message": "Max 100 logs par requete"}})

    import uuid as _uuid
    conn = get_conn()
    cur  = conn.cursor()
    accepted = 0
    rejected = 0
    errors   = []
    for log in logs:
        try:
            cur.execute("""
                INSERT INTO agent_logs (id, agent_id, timestamp, level, category, message)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (str(_uuid.uuid4()), agent_id,
                  log.get("timestamp"), log.get("level"),
                  log.get("category"), log.get("message")))
            accepted += 1
        except Exception as e:
            rejected += 1
            errors.append(str(e))

    conn.commit()
    cur.close()
    conn.close()
    json_response(handler, 202, {"accepted": accepted, "rejected": rejected, "errors": errors})


def handle_agent_gpo_report(handler, body):
    import uuid as _uuid
    agent_id    = body.get("agent_id", "")
    gpo_id      = body.get("gpo_id", "")
    status      = body.get("status", "")
    if not all([agent_id, gpo_id, status]):
        return json_response(handler, 400, {"error": {"code": "VALIDATION_ERROR", "message": "Champs requis manquants"}})
    json_response(handler, 200, {
        "acknowledged":   True,
        "application_id": str(_uuid.uuid4())
    })


# ── Handler HTTP ──────────────────────────────────────────────

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
        elif self.path == "/api/v1/admin/auth/refresh":
            handle_refresh(self, body)
        elif self.path == "/api/v1/admin/auth/logout":
            handle_logout(self, body)
        elif self.path == "/api/v1/enrollment/tokens":
            handle_enrollment_tokens_create(self, body)
        elif self.path == "/api/v1/enrollment/enroll":
            handle_enroll(self, body)
        elif self.path == "/api/v1/agent/poll":
            handle_agent_poll(self, body)
        elif self.path == "/api/v1/agent/logs":
            handle_agent_logs(self, body)
        elif self.path == "/api/v1/agent/gpo/report":
            handle_agent_gpo_report(self, body)
        else:
            json_response(self, 404, {"error": {"code": "NOT_FOUND", "message": f"Route {self.path} introuvable"}})

    def do_DELETE(self):
        if self.path.startswith("/api/v1/enrollment/tokens/"):
            token_id = self.path.split("/")[-1]
            handle_enrollment_token_delete(self, token_id)
        else:
            json_response(self, 404, {"error": {"code": "NOT_FOUND", "message": f"Route {self.path} introuvable"}})

    def do_GET(self):
        if self.path.startswith("/api/v1/admin/machines"):
            handle_machines(self)
        elif self.path.startswith("/api/v1/admin/users"):
            handle_users(self)
        elif self.path.startswith("/api/v1/admin/gpo"):
            handle_gpo(self)
        elif self.path.startswith("/api/v1/admin/groups"):
            handle_groups(self)
        elif self.path.startswith("/api/v1/admin/dashboard/stats"):
            handle_dashboard_stats(self)
        elif self.path.startswith("/api/v1/enrollment/tokens"):
            handle_enrollment_tokens_list(self)
        else:
            json_response(self, 404, {"error": {"code": "NOT_FOUND", "message": f"Route {self.path} introuvable"}})


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 4444), RelayHandler)
    print(f"Relay demarre sur http://127.0.0.1:4444")
    print(f"POST /api/v1/admin/auth/login")
    print(f"POST /api/v1/admin/auth/refresh")
    print(f"POST /api/v1/admin/auth/logout")
    print(f"GET  /api/v1/admin/dashboard/stats")
    print(f"GET  /api/v1/admin/machines")
    print(f"GET  /api/v1/admin/users")
    print(f"GET  /api/v1/admin/gpo")
    print(f"GET  /api/v1/admin/groups")
    print(f"POST /api/v1/enrollment/tokens")
    print(f"GET  /api/v1/enrollment/tokens")
    print(f"DELETE /api/v1/enrollment/tokens/{{id}}")
    print(f"POST /api/v1/enrollment/enroll")
    print(f"POST /api/v1/agent/poll")
    print(f"POST /api/v1/agent/logs")
    print(f"POST /api/v1/agent/gpo/report")
    server.serve_forever()