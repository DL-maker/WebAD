import mysql.connector
import hashlib
import uuid
import json
import sys
import time
from datetime import datetime, timedelta
from collections import defaultdict

# ── Config DB ────────────────────────────────────────────────
DB = {
    "host":     "localhost",
    "database": "linuxad",
    "user":     "root",
    "password": "root"
}

# Rate limiting en mémoire (5 tentatives/min par username)
_attempts: dict = defaultdict(list)

def get_conn():
    return mysql.connector.connect(**DB)

def sha256(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()

def mock_jwt(username: str, role: str) -> str:
    return f"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.{sha256(username + role)[:32]}"

def response(code: int, data: dict):
    color = "\033[92m" if code == 200 or code == 201 else "\033[91m"
    reset = "\033[0m"
    print(f"\n{color}── Réponse {code} ──────────────────────────────────{reset}")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    print()


# ── Login ────────────────────────────────────────────────────
def login(username: str, password: str, mfa_code: str = None):
    print(f"\n── Requête POST /api/v1/admin/auth/login ──────────────")
    print(json.dumps({"username": username, "password": password, "mfa_code": mfa_code}, indent=2))

    # Rate limiting
    now = time.time()
    _attempts[username] = [t for t in _attempts[username] if now - t < 60]
    if len(_attempts[username]) >= 5:
        response(429, {"error": {"code": "RATE_LIMITED", "message": "Trop de tentatives (5/min)"}})
        return
    _attempts[username].append(now)

    conn = get_conn()
    cur  = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM admin_users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    # Identifiants incorrects
    if not user or user["password_hash"] != sha256(password):
        response(401, {"error": {"code": "INVALID_CREDENTIALS", "message": "Identifiants incorrects"}})
        return

    # MFA requis mais absent
    if user["mfa_enabled"] and not mfa_code:
        response(401, {"error": {"code": "MFA_REQUIRED", "message": "Code MFA requis mais absent"}})
        return

    # MFA invalide (on vérifie juste qu'il n'est pas vide pour le mock)
    if user["mfa_enabled"] and mfa_code and len(mfa_code) != 6:
        response(401, {"error": {"code": "INVALID_MFA", "message": "Code MFA invalide"}})
        return

    # Mise à jour last_login
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("UPDATE admin_users SET last_login = NOW() WHERE id = %s", (user["id"],))
    conn.commit()
    cur.close()
    conn.close()

    access_token  = mock_jwt(username, user["role"])
    refresh_token = f"linuxad_refresh_1_{sha256(username)[:12]}"

    response(200, {
        "access_token":  access_token,
        "token_type":    "bearer",
        "expires_in":    3600,
        "refresh_token": refresh_token,
        "user": {
            "id":         str(user["id"]),
            "username":   user["username"],
            "email":      user["email"],
            "role":       user["role"],
            "last_login": user["last_login"].isoformat() if user["last_login"] else None
        }
    })


# ── Machines ─────────────────────────────────────────────────
def list_machines():
    print("\n── Requête GET /api/v1/admin/machines ─────────────────")
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

    for r in rows:
        if r.get("last_contact"):
            r["last_contact"] = r["last_contact"].isoformat()

    response(200, {"data": rows, "pagination": {"total": len(rows), "page": 1, "per_page": 20}})


# ── Users LDAP ───────────────────────────────────────────────
def list_users():
    print("\n── Requête GET /api/v1/admin/users ────────────────────")
    conn = get_conn()
    cur  = conn.cursor(dictionary=True)
    cur.execute("SELECT uid, cn, email, uid_number, home_directory, login_shell FROM users ORDER BY uid_number")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    response(200, {"data": rows, "pagination": {"total": len(rows), "page": 1, "per_page": 20}})


# ── GPO ──────────────────────────────────────────────────────
def list_gpo():
    print("\n── Requête GET /api/v1/admin/gpo ──────────────────────")
    conn = get_conn()
    cur  = conn.cursor(dictionary=True)
    cur.execute("SELECT id, name, description, version, status, updated_at FROM gpo ORDER BY updated_at DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    for r in rows:
        if r.get("updated_at"):
            r["updated_at"] = r["updated_at"].isoformat()

    response(200, {"data": rows, "pagination": {"total": len(rows), "page": 1, "per_page": 20}})


# ── CLI ──────────────────────────────────────────────────────
if __name__ == "__main__":
    args = sys.argv[1:]

    if not args:
        print(__doc__)
        sys.exit(0)

    elif args[0] == "login" and len(args) >= 3:
        mfa = args[3] if len(args) > 3 else None
        login(args[1], args[2], mfa)

    elif args[0] == "machines":
        list_machines()

    elif args[0] == "users":
        list_users()

    elif args[0] == "gpo":
        list_gpo()

    else:
        print(__doc__)