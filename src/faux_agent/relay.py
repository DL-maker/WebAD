from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import hashlib
import time
import psycopg2
import psycopg2.extras
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

def get_cursor(conn):
    return conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

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
    cur  = get_cursor(conn)
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
    cur  = get_cursor(conn)
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
    cur  = get_cursor(conn)
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


def handle_machine_detail(handler, machine_id):
    conn = get_conn()
    cur  = get_cursor(conn)
    cur.execute("SELECT * FROM machines WHERE id = %s", (machine_id,))
    machine = cur.fetchone()

    if not machine:
        cur.close()
        conn.close()
        return json_response(handler, 404, {"error": {"code": "NOT_FOUND", "message": "Machine non trouvee"}})

    cur.execute("SELECT * FROM agents WHERE machine_id = %s", (machine_id,))
    agent = cur.fetchone()

    cur.execute("""
        SELECT g.id, g.name FROM "groups" g
        JOIN machine_groups mg ON mg.group_id = g.id
        WHERE mg.machine_id = %s
    """, (machine_id,))
    groups = cur.fetchall()

    cur.close()
    conn.close()

    json_response(handler, 200, {
        "id":             str(machine["id"]),
        "hostname":       machine["hostname"],
        "fqdn":           machine["fqdn"],
        "os_version":     machine["os_version"],
        "kernel_version": machine["kernel_version"],
        "status":         machine["status"],
        "enrolled_at":    str(machine["enrolled_at"]) if machine["enrolled_at"] else None,
        "last_contact":   str(machine["last_contact"]) if machine["last_contact"] else None,
        "agent": {
            "id":        str(agent["id"]) if agent else None,
            "status":    agent["status"] if agent else "offline",
            "version":   agent["agent_version"] if agent else None,
            "ip_address": agent["ip_address"] if agent else None,
            "last_seen": str(agent["last_seen"]) if agent and agent["last_seen"] else None,
            "kernel_module_loaded": False
        } if agent else None,
        "groups": [{"id": str(g["id"]), "name": g["name"]} for g in groups],
        "system_status": {
            "uptime_seconds": 0,
            "cpu_usage_percent": 0.0,
            "memory_usage_percent": 0.0,
            "disk_usage_percent": 0.0,
            "load_average": [0.0, 0.0, 0.0]
        },
        "gpo_status": [],
        "network_info": {
            "primary_ip": agent["ip_address"] if agent else None,
            "interfaces": []
        }
    })


def handle_machine_delete(handler, machine_id):
    conn = get_conn()
    cur  = get_cursor(conn)
    cur.execute("SELECT hostname FROM machines WHERE id = %s", (machine_id,))
    machine = cur.fetchone()

    if not machine:
        cur.close()
        conn.close()
        return json_response(handler, 404, {"error": {"code": "NOT_FOUND", "message": "Machine non trouvee"}})

    cur2 = conn.cursor()
    cur2.execute("UPDATE agents SET status = 'revoked' WHERE machine_id = %s", (machine_id,))
    cur2.execute("UPDATE machines SET status = 'revoked' WHERE id = %s", (machine_id,))
    conn.commit()
    cur.close()
    cur2.close()
    conn.close()

    json_response(handler, 200, {
        "id":         machine_id,
        "hostname":   machine["hostname"],
        "status":     "revoked",
        "revoked_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "revoked_by": "admin"
    })


def handle_users(handler):
    conn = get_conn()
    cur  = get_cursor(conn)
    cur.execute("SELECT uid, cn, email, uid_number, gid_number, home_directory, login_shell, created_at FROM users ORDER BY uid_number")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    json_response(handler, 200, {"data": rows, "pagination": {"total": len(rows), "page": 1, "per_page": 20}})


def handle_user_detail(handler, uid):
    conn = get_conn()
    cur  = get_cursor(conn)
    cur.execute("SELECT * FROM users WHERE uid = %s", (uid,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if not user:
        return json_response(handler, 404, {"error": {"code": "NOT_FOUND", "message": "Utilisateur non trouve"}})

    json_response(handler, 200, {
        **dict(user),
        "machines_authorized": [],
        "last_login_machines": []
    })


def handle_user_create(handler, body):
    import uuid as _uuid

    uid        = body.get("uid", "")
    cn         = body.get("cn", "")
    sn         = body.get("sn", "")
    email      = body.get("email", "")
    password   = body.get("password", "")
    login_shell = body.get("login_shell", "/bin/bash")
    home_dir   = body.get("home_directory", f"/home/{uid}")

    if not all([uid, cn, email, password]):
        return json_response(handler, 400, {"error": {"code": "VALIDATION_ERROR", "message": "Champs requis manquants"}})
    if len(password) < 12:
        return json_response(handler, 400, {"error": {"code": "VALIDATION_ERROR", "message": "Mot de passe trop court (min 12 chars)"}})

    conn = get_conn()
    cur  = get_cursor(conn)
    cur.execute("SELECT uid FROM users WHERE uid = %s OR email = %s", (uid, email))
    if cur.fetchone():
        cur.close()
        conn.close()
        return json_response(handler, 409, {"error": {"code": "CONFLICT", "message": "uid ou email deja existant"}})

    cur.execute("SELECT COALESCE(MAX(uid_number), 10000) + 1 AS next FROM users")
    uid_number = cur.fetchone()["next"]

    cur2 = conn.cursor()
    cur2.execute("""
        INSERT INTO users (uid, ldap_dn, cn, email, uid_number, gid_number, home_directory, login_shell, created_by)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'admin')
    """, (uid, f"uid={uid},ou=People,dc=linuxad,dc=local", cn, email, uid_number, uid_number, home_dir, login_shell))
    conn.commit()
    cur.close()
    cur2.close()
    conn.close()

    json_response(handler, 201, {
        "uid":            uid,
        "cn":             cn,
        "sn":             sn,
        "email":          email,
        "uid_number":     uid_number,
        "gid_number":     uid_number,
        "home_directory": home_dir,
        "login_shell":    login_shell,
        "groups":         body.get("groups", []),
        "ldap_dn":        f"uid={uid},ou=People,dc=linuxad,dc=local",
        "created_at":     time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    })


def handle_user_patch(handler, uid, body):
    conn = get_conn()
    cur  = get_cursor(conn)
    cur.execute("SELECT * FROM users WHERE uid = %s", (uid,))
    user = cur.fetchone()

    if not user:
        cur.close()
        conn.close()
        return json_response(handler, 404, {"error": {"code": "NOT_FOUND", "message": "Utilisateur non trouve"}})

    fields = []
    values = []
    for field in ["cn", "email", "login_shell"]:
        if field in body:
            fields.append(f"{field} = %s")
            values.append(body[field])

    if fields:
        values.append(uid)
        cur2 = conn.cursor()
        cur2.execute(f"UPDATE users SET {', '.join(fields)} WHERE uid = %s", values)
        conn.commit()
        cur2.close()

    cur.execute("SELECT * FROM users WHERE uid = %s", (uid,))
    updated = cur.fetchone()
    cur.close()
    conn.close()
    json_response(handler, 200, dict(updated))


def handle_user_delete(handler, uid):
    conn = get_conn()
    cur  = get_cursor(conn)
    cur.execute("SELECT uid FROM users WHERE uid = %s", (uid,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        return json_response(handler, 404, {"error": {"code": "NOT_FOUND", "message": "Utilisateur non trouve"}})

    cur2 = conn.cursor()
    cur2.execute("DELETE FROM users WHERE uid = %s", (uid,))
    conn.commit()
    cur.close()
    cur2.close()
    conn.close()

    json_response(handler, 200, {
        "uid":        uid,
        "deleted":    True,
        "deleted_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "deleted_by": "admin"
    })


def handle_user_password(handler, uid, body):
    new_password = body.get("new_password", "")
    force_change = body.get("force_change_on_login", False)

    if len(new_password) < 12:
        return json_response(handler, 400, {"error": {"code": "VALIDATION_ERROR", "message": "Mot de passe trop court (min 12 chars)"}})

    conn = get_conn()
    cur  = get_cursor(conn)
    cur.execute("SELECT uid FROM users WHERE uid = %s", (uid,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        return json_response(handler, 404, {"error": {"code": "NOT_FOUND", "message": "Utilisateur non trouve"}})

    cur.close()
    conn.close()

    json_response(handler, 200, {
        "uid":                  uid,
        "password_changed":     True,
        "changed_at":           time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "force_change_on_login": force_change
    })


def handle_gpo(handler):
    conn = get_conn()
    cur  = get_cursor(conn)
    cur.execute("""
        SELECT id, name, description, version, status, updated_at, created_at, signature
        FROM gpo ORDER BY updated_at DESC
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    data = []
    for r in dict_rows(rows):
        r["tags"] = []
        r["policies_count"] = 0
        r["assignments_count"] = 0
        r["machines_targeted"] = 0
        r["compliance"] = {"success": 0, "pending": 0, "failed": 0}
        r["signed_at"] = None
        r["signed_by"] = None
        data.append(r)
    json_response(handler, 200, {"data": data, "pagination": {"total": len(data), "page": 1, "per_page": 20}})


def dict_rows(rows):
    return [dict(r) for r in rows]


def handle_gpo_detail(handler, gpo_id):
    conn = get_conn()
    cur  = get_cursor(conn)
    cur.execute("SELECT * FROM gpo WHERE id = %s", (gpo_id,))
    gpo = cur.fetchone()

    if not gpo:
        cur.close(); conn.close()
        return json_response(handler, 404, {"error": {"code": "NOT_FOUND", "message": "GPO non trouvee"}})

    cur.execute("SELECT * FROM gpo_assignments WHERE gpo_id = %s", (gpo_id,))
    assignments = cur.fetchall()
    cur.close(); conn.close()

    gpo = dict(gpo)
    json_response(handler, 200, {
        **gpo,
        "schema_version": "1.0",
        "metadata": {"author": "admin", "tags": []},
        "targeting": {"mode": "include", "groups": [], "machines": []},
        "assignments": [dict(a) for a in assignments],
        "deployment_status": {"total_targeted": 0, "success": 0, "pending": 0, "failed": 0, "machines": []},
        "version_history": [{"version": gpo["version"], "updated_at": str(gpo["updated_at"]), "updated_by": "admin"}],
        "rollback": {"enabled": True, "automatic_on_failure": True, "keep_backups": 5}
    })


def handle_gpo_create(handler, body):
    import uuid as _uuid

    name        = body.get("name", "")
    description = body.get("description", "")
    content     = body.get("content", {"schema_version": "1.0", "policies": []})

    if not name:
        return json_response(handler, 400, {"error": {"code": "VALIDATION_ERROR", "message": "Nom requis"}})

    gpo_id = str(_uuid.uuid4())

    conn = get_conn()
    cur  = get_cursor(conn)
    cur.execute("SELECT id FROM gpo WHERE name = %s", (name,))
    if cur.fetchone():
        cur.close(); conn.close()
        return json_response(handler, 409, {"error": {"code": "CONFLICT", "message": "Nom de GPO deja existant"}})

    import json as _json
    cur2 = conn.cursor()
    cur2.execute("""
        INSERT INTO gpo (id, name, description, version, status, content, created_at, updated_at)
        VALUES (%s, %s, %s, 1, 'draft', %s, NOW(), NOW())
    """, (gpo_id, name, description, _json.dumps(content)))
    conn.commit()
    cur.close(); cur2.close(); conn.close()

    json_response(handler, 201, {
        "id": gpo_id, "name": name, "description": description,
        "version": 1, "status": "draft", "content": content,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    })


def handle_gpo_patch(handler, gpo_id, body):
    conn = get_conn()
    cur  = get_cursor(conn)
    cur.execute("SELECT * FROM gpo WHERE id = %s", (gpo_id,))
    gpo = cur.fetchone()

    if not gpo:
        cur.close(); conn.close()
        return json_response(handler, 404, {"error": {"code": "NOT_FOUND", "message": "GPO non trouvee"}})

    gpo = dict(gpo)
    new_version = gpo["version"] + 1 if gpo["status"] == "active" else gpo["version"]

    fields, values = [], []
    for field in ["name", "description"]:
        if field in body:
            fields.append(f"{field} = %s")
            values.append(body[field])

    fields.append("status = 'draft'")
    fields.append(f"version = {new_version}")
    fields.append("updated_at = NOW()")
    values.append(gpo_id)

    cur2 = conn.cursor()
    cur2.execute(f"UPDATE gpo SET {', '.join(fields)} WHERE id = %s", values)
    conn.commit()

    cur.execute("SELECT * FROM gpo WHERE id = %s", (gpo_id,))
    updated = cur.fetchone()
    cur.close(); cur2.close(); conn.close()
    json_response(handler, 200, dict(updated))


def handle_gpo_sign(handler, gpo_id):
    conn = get_conn()
    cur  = get_cursor(conn)
    cur.execute("SELECT * FROM gpo WHERE id = %s", (gpo_id,))
    gpo = cur.fetchone()

    if not gpo:
        cur.close(); conn.close()
        return json_response(handler, 404, {"error": {"code": "NOT_FOUND", "message": "GPO non trouvee"}})

    gpo = dict(gpo)
    if gpo["status"] == "active":
        cur.close(); conn.close()
        return json_response(handler, 409, {"error": {"code": "CONFLICT", "message": "GPO deja active avec cette version"}})

    signature = sha256(gpo["name"] + str(gpo["version"]) + "signed")
    cur2 = conn.cursor()
    cur2.execute("UPDATE gpo SET status = 'active', signature = %s, updated_at = NOW() WHERE id = %s",
                 (signature, gpo_id))
    conn.commit()
    cur.close(); cur2.close(); conn.close()

    json_response(handler, 200, {
        "id": gpo_id, "name": gpo["name"], "version": gpo["version"],
        "status": "active", "signature": signature,
        "signed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "signed_by": "admin"
    })


def handle_gpo_assignments(handler, gpo_id, body):
    import uuid as _uuid

    assignments = body.get("assignments", [])

    conn = get_conn()
    cur  = get_cursor(conn)
    cur.execute("SELECT id FROM gpo WHERE id = %s", (gpo_id,))
    if not cur.fetchone():
        cur.close(); conn.close()
        return json_response(handler, 404, {"error": {"code": "NOT_FOUND", "message": "GPO non trouvee"}})

    cur2 = conn.cursor()
    created = 0
    for a in assignments:
        cur2.execute("""
            INSERT INTO gpo_assignments (id, gpo_id, target_type, priority, enabled)
            VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
        """, (str(_uuid.uuid4()), gpo_id,
              a.get("target_type", "all"),
              a.get("priority", 100),
              a.get("enabled", True)))
        created += cur2.rowcount

    conn.commit()
    cur.execute("SELECT COUNT(*) AS total FROM machines")
    total = cur.fetchone()["total"]
    cur.close(); cur2.close(); conn.close()

    json_response(handler, 200, {
        "gpo_id": gpo_id,
        "assignments_created": created,
        "machines_targeted": total
    })


def handle_gpo_status(handler, gpo_id):
    conn = get_conn()
    cur  = get_cursor(conn)
    cur.execute("SELECT * FROM gpo WHERE id = %s", (gpo_id,))
    gpo = cur.fetchone()

    if not gpo:
        cur.close(); conn.close()
        return json_response(handler, 404, {"error": {"code": "NOT_FOUND", "message": "GPO non trouvee"}})

    gpo = dict(gpo)
    cur.execute("SELECT COUNT(*) AS total FROM machines")
    total = cur.fetchone()["total"]
    cur.close(); conn.close()

    json_response(handler, 200, {
        "gpo_id": gpo_id, "gpo_name": gpo["name"],
        "version": gpo["version"], "status": gpo["status"],
        "deployment": {"total_targeted": total, "applied_success": 0, "applied_pending": total, "applied_failed": 0, "not_seen": 0},
        "machines": []
    })


def handle_gpo_rollback(handler, gpo_id, body):
    import uuid as _uuid

    target_version = body.get("target_version")
    reason         = body.get("reason", "")

    if not target_version:
        return json_response(handler, 400, {"error": {"code": "VALIDATION_ERROR", "message": "target_version requis"}})

    conn = get_conn()
    cur  = get_cursor(conn)
    cur.execute("SELECT * FROM gpo WHERE id = %s", (gpo_id,))
    gpo = cur.fetchone()

    if not gpo:
        cur.close(); conn.close()
        return json_response(handler, 404, {"error": {"code": "NOT_FOUND", "message": "GPO non trouvee"}})

    gpo = dict(gpo)
    cur.execute("SELECT COUNT(*) AS total FROM machines")
    total = cur.fetchone()["total"]
    cur.close(); conn.close()

    rollback_id = str(_uuid.uuid4())
    json_response(handler, 202, {
        "rollback_id": rollback_id, "gpo_id": gpo_id,
        "from_version": gpo["version"], "to_version": target_version,
        "machines_targeted": total, "status": "in_progress",
        "initiated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "initiated_by": "admin"
    })


def handle_gpo_rollback_status(handler, gpo_id, rollback_id):
    json_response(handler, 200, {
        "rollback_id": rollback_id, "gpo_id": gpo_id,
        "status": "completed", "machines_targeted": 0,
        "machines_completed": 0, "machines_failed": 0,
        "initiated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "completed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "initiated_by": "admin", "failed_machines": []
    })


def handle_gpo_test(handler, gpo_id, body):
    import uuid as _uuid
    test_id = str(_uuid.uuid4())
    machines = body.get("machines", [])
    json_response(handler, 202, {
        "test_id": test_id, "gpo_id": gpo_id,
        "status": "pending", "machines_targeted": len(machines) or 1,
        "initiated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    })


def handle_gpo_test_status(handler, gpo_id, test_id):
    json_response(handler, 200, {
        "test_id": test_id, "gpo_id": gpo_id,
        "status": "completed", "machines_targeted": 1,
        "initiated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "completed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "results": []
    })





def handle_groups(handler):
    conn = get_conn()
    cur  = get_cursor(conn)
    cur.execute("""
        SELECT g.id, g.name, g.description, g.ldap_dn,
               COUNT(DISTINCT mg.machine_id) AS machine_count,
               COUNT(DISTINCT ga.id) AS gpo_count
        FROM "groups" g
        LEFT JOIN machine_groups mg ON mg.group_id = g.id
        LEFT JOIN gpo_assignments ga ON ga.target_type = 'group'
        GROUP BY g.id, g.name, g.description, g.ldap_dn
        ORDER BY g.name
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    json_response(handler, 200, {"data": rows, "pagination": {"total": len(rows), "page": 1, "per_page": 20}})


def handle_group_create(handler, body):
    import uuid as _uuid
    name        = body.get("name", "")
    description = body.get("description", "")

    if not name or len(name) < 3:
        return json_response(handler, 400, {"error": {"code": "VALIDATION_ERROR", "message": "Nom requis (min 3 chars)"}})

    group_id = str(_uuid.uuid4())
    ldap_dn  = f"cn={name},ou=Groups,dc=linuxad,dc=local"

    conn = get_conn()
    cur  = get_cursor(conn)
    cur.execute('SELECT id FROM "groups" WHERE name = %s', (name,))
    if cur.fetchone():
        cur.close()
        conn.close()
        return json_response(handler, 409, {"error": {"code": "CONFLICT", "message": "Nom de groupe deja existant"}})

    cur2 = conn.cursor()
    cur2.execute('INSERT INTO "groups" (id, name, description, ldap_dn) VALUES (%s, %s, %s, %s)',
                 (group_id, name, description, ldap_dn))
    conn.commit()
    cur.close()
    cur2.close()
    conn.close()

    json_response(handler, 201, {
        "id": group_id, "name": name, "description": description,
        "ldap_dn": ldap_dn, "machine_count": 0, "gpo_count": 0,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    })


def handle_group_patch(handler, group_id, body):
    conn = get_conn()
    cur  = get_cursor(conn)
    cur.execute('SELECT * FROM "groups" WHERE id = %s', (group_id,))
    group = cur.fetchone()
    if not group:
        cur.close(); conn.close()
        return json_response(handler, 404, {"error": {"code": "NOT_FOUND", "message": "Groupe non trouve"}})

    fields, values = [], []
    for field in ["name", "description"]:
        if field in body:
            fields.append(f"{field} = %s")
            values.append(body[field])
    if fields:
        values.append(group_id)
        cur2 = conn.cursor()
        cur2.execute(f'UPDATE "groups" SET {", ".join(fields)} WHERE id = %s', values)
        conn.commit()
        cur2.close()

    cur.execute('SELECT * FROM "groups" WHERE id = %s', (group_id,))
    updated = cur.fetchone()
    cur.close(); conn.close()
    json_response(handler, 200, dict(updated))


def handle_group_delete(handler, group_id):
    conn = get_conn()
    cur  = get_cursor(conn)
    cur.execute('SELECT name FROM "groups" WHERE id = %s', (group_id,))
    group = cur.fetchone()
    if not group:
        cur.close(); conn.close()
        return json_response(handler, 404, {"error": {"code": "NOT_FOUND", "message": "Groupe non trouve"}})

    cur2 = conn.cursor()
    cur2.execute("DELETE FROM machine_groups WHERE group_id = %s", (group_id,))
    cur2.execute('DELETE FROM "groups" WHERE id = %s', (group_id,))
    conn.commit()
    cur.close(); cur2.close(); conn.close()

    json_response(handler, 200, {
        "id": group_id, "name": group["name"],
        "deleted": True, "deleted_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    })


def handle_group_members(handler, group_id, body):
    add    = body.get("add", [])
    remove = body.get("remove", [])

    conn = get_conn()
    cur  = get_cursor(conn)
    cur.execute('SELECT name FROM "groups" WHERE id = %s', (group_id,))
    group = cur.fetchone()
    if not group:
        cur.close(); conn.close()
        return json_response(handler, 404, {"error": {"code": "NOT_FOUND", "message": "Groupe non trouve"}})

    cur2 = conn.cursor()
    added = removed = 0
    for machine_id in add:
        try:
            cur2.execute("INSERT INTO machine_groups (machine_id, group_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                         (machine_id, group_id))
            added += cur2.rowcount
        except Exception:
            pass
    for machine_id in remove:
        cur2.execute("DELETE FROM machine_groups WHERE machine_id = %s AND group_id = %s", (machine_id, group_id))
        removed += cur2.rowcount
    conn.commit()

    cur.execute("SELECT COUNT(*) AS total FROM machine_groups WHERE group_id = %s", (group_id,))
    total = cur.fetchone()["total"]
    cur.close(); cur2.close(); conn.close()

    json_response(handler, 200, {
        "group_id": group_id, "group_name": group["name"],
        "added": added, "removed": removed, "total_members": total
    })




def handle_dashboard_stats(handler):
    conn = get_conn()
    cur  = get_cursor(conn)

    cur.execute("SELECT status, COUNT(*) as count FROM machines GROUP BY status")
    machine_rows = {r["status"]: r["count"] for r in cur.fetchall()}

    cur.execute("SELECT status, COUNT(*) as count FROM agents GROUP BY status")
    agent_rows = {r["status"]: r["count"] for r in cur.fetchall()}

    cur.execute("SELECT COUNT(*) as count FROM users")
    user_count = cur.fetchone()["count"]

    cur.execute("SELECT COUNT(*) as count FROM 'groups'")
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
    cur  = get_cursor(conn)
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
    cur  = get_cursor(conn)
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
    cur  = get_cursor(conn)
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
    cur  = get_cursor(conn)
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
            from datetime import datetime, timezone
            ts_raw = log.get("timestamp", "")
            try:
                ts = datetime.fromisoformat(ts_raw.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                ts = ts_raw.replace("T", " ").replace("Z", "")
            cur.execute("""
                INSERT INTO agent_logs (id, agent_id, timestamp, level, category, message)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (str(_uuid.uuid4()), agent_id,
                  ts, log.get("level"),
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
        elif self.path.startswith("/api/v1/admin/users/") and self.path.endswith("/password"):
            uid = self.path.split("/")[5]
            handle_user_password(self, uid, body)
        elif self.path == "/api/v1/admin/users":
            handle_user_create(self, body)
        elif self.path == "/api/v1/admin/groups":
            handle_group_create(self, body)
        elif self.path.startswith("/api/v1/admin/groups/") and self.path.endswith("/members"):
            group_id = self.path.split("/")[5]
            handle_group_members(self, group_id, body)
        elif self.path == "/api/v1/admin/gpo":
            handle_gpo_create(self, body)
        elif self.path.startswith("/api/v1/admin/gpo/") and self.path.endswith("/sign"):
            gpo_id = self.path.split("/")[5]
            handle_gpo_sign(self, gpo_id)
        elif self.path.startswith("/api/v1/admin/gpo/") and self.path.endswith("/assignments"):
            gpo_id = self.path.split("/")[5]
            handle_gpo_assignments(self, gpo_id, body)
        elif self.path.startswith("/api/v1/admin/gpo/") and self.path.endswith("/rollback"):
            gpo_id = self.path.split("/")[5]
            handle_gpo_rollback(self, gpo_id, body)
        elif self.path.startswith("/api/v1/admin/gpo/") and "/test" in self.path and not self.path.split("/test/")[-1]:
            gpo_id = self.path.split("/")[5]
            handle_gpo_test(self, gpo_id, body)
        else:
            json_response(self, 404, {"error": {"code": "NOT_FOUND", "message": f"Route {self.path} introuvable"}})

    def do_DELETE(self):
        if self.path.startswith("/api/v1/enrollment/tokens/"):
            token_id = self.path.split("/")[-1]
            handle_enrollment_token_delete(self, token_id)
        elif self.path.startswith("/api/v1/admin/machines/"):
            machine_id = self.path.split("/")[-1]
            handle_machine_delete(self, machine_id)
        elif self.path.startswith("/api/v1/admin/users/"):
            uid = self.path.split("/")[5]
            handle_user_delete(self, uid)
        elif self.path.startswith("/api/v1/admin/groups/"):
            group_id = self.path.split("/")[5]
            handle_group_delete(self, group_id)
        else:
            json_response(self, 404, {"error": {"code": "NOT_FOUND", "message": f"Route {self.path} introuvable"}})

    def do_PATCH(self):
        length = int(self.headers.get("Content-Length", 0))
        body   = json.loads(self.rfile.read(length)) if length else {}

        if self.path.startswith("/api/v1/admin/users/"):
            uid = self.path.split("/")[5]
            handle_user_patch(self, uid, body)
        elif self.path.startswith("/api/v1/admin/groups/"):
            group_id = self.path.split("/")[5]
            handle_group_patch(self, group_id, body)
        elif self.path.startswith("/api/v1/admin/gpo/"):
            gpo_id = self.path.split("/")[5]
            handle_gpo_patch(self, gpo_id, body)
        else:
            json_response(self, 404, {"error": {"code": "NOT_FOUND", "message": f"Route {self.path} introuvable"}})

    def do_GET(self):
        if self.path == "/api/v1/admin/machines" or self.path.startswith("/api/v1/admin/machines?"):
            handle_machines(self)
        elif self.path.startswith("/api/v1/admin/machines/"):
            machine_id = self.path.split("/")[5]
            handle_machine_detail(self, machine_id)
        elif self.path == "/api/v1/admin/users" or self.path.startswith("/api/v1/admin/users?"):
            handle_users(self)
        elif self.path.startswith("/api/v1/admin/users/"):
            uid = self.path.split("/")[5]
            handle_user_detail(self, uid)
        elif self.path == "/api/v1/admin/gpo" or self.path.startswith("/api/v1/admin/gpo?"):
            handle_gpo(self)
        elif self.path.startswith("/api/v1/admin/gpo/"):
            parts = self.path.split("/")
            gpo_id = parts[5]
            if len(parts) == 6:
                handle_gpo_detail(self, gpo_id)
            elif parts[-1] == "status":
                handle_gpo_status(self, gpo_id)
            elif len(parts) >= 8 and parts[6] == "rollback":
                handle_gpo_rollback_status(self, gpo_id, parts[7])
            elif len(parts) >= 8 and parts[6] == "test":
                handle_gpo_test_status(self, gpo_id, parts[7])
            else:
                json_response(self, 404, {"error": {"code": "NOT_FOUND", "message": f"Route {self.path} introuvable"}})
        elif self.path == "/api/v1/admin/groups" or self.path.startswith("/api/v1/admin/groups?"):
            handle_groups(self)
        elif self.path.startswith("/api/v1/admin/groups/"):
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