import hashlib
import uuid
import random
import os
from datetime import datetime, timedelta

def sha256(s):
    return hashlib.sha256(s.encode()).hexdigest()

def uid():
    return str(uuid.uuid4())

def rand_date(days_back=30):
    d = datetime.now() - timedelta(days=random.randint(0, days_back))
    return d.strftime('%Y-%m-%d %H:%M:%S')

# Donnees ---------------------------------------------------

admin_users = [
    {"id": uid(), "username": "admin",     "email": "admin@linuxad.local",     "password": "Admin1234!",        "role": "superadmin", "mfa": False},
    {"id": uid(), "username": "h",         "email": "sysadmin@linuxad.local",  "password": "Nopassword1!",      "role": "operator",   "mfa": True},
    {"id": uid(), "username": "k",         "email": "k@linuxad.local",         "password": "le deniec est mal", "role": "viewer",     "mfa": False},
    {"id": uid(), "username": "t",         "email": "t@linuxad.local",         "password": "coucou",            "role": "admin",      "mfa": True},
    {"id": uid(), "username": "o",         "email": "o@linuxad.local",         "password": "own",               "role": "operator",   "mfa": False},
]

machines = [
    {"id": uid(), "hostname": "webapp-01",     "fqdn": "webapp-01.linuxad.local",     "os": "Debian 13", "kernel": "6.12.38", "status": "active"},
    {"id": uid(), "hostname": "webapp-02",     "fqdn": "webapp-02.linuxad.local",     "os": "Debian 13", "kernel": "6.12.38", "status": "rolled_back"},
    {"id": uid(), "hostname": "db-master",     "fqdn": "db-master.linuxad.local",     "os": "Alpine",    "kernel": "6.12.38", "status": "active"},
    {"id": uid(), "hostname": "db-replica",    "fqdn": "db-replica.linuxad.local",    "os": "FreeBSD",   "kernel": "13.0",    "status": "inactive"},
    {"id": uid(), "hostname": "monitoring-01", "fqdn": "monitoring-01.linuxad.local", "os": "Arch",      "kernel": "6.12.38", "status": "pending"},
]

groups = [
    {"id": uid(), "name": "webapps",          "desc": "Serveurs web en prod"},
    {"id": uid(), "name": "database-servers", "desc": "Serveurs de bdd"},
    {"id": uid(), "name": "production",       "desc": "Toutes les machines de prod"},
    {"id": uid(), "name": "monitoring",       "desc": "Machines de monitoring"},
]

ldap_users = [
    {"uid": "jdoe",    "cn": "John Doe",    "email": "jdoe@linuxad.local",    "uid_number": 10001, "gid": 10001},
    {"uid": "asmith",  "cn": "Alice Smith", "email": "asmith@linuxad.local",  "uid_number": 10002, "gid": 10002},
    {"uid": "bmartin", "cn": "Bob Martin",  "email": "bmartin@linuxad.local", "uid_number": 10003, "gid": 10003},
]

gpos = [
    {"id": uid(), "name": "security_base",   "desc": "Configuration de securite", "status": "active",   "version": 4},
    {"id": uid(), "name": "ssh-hardening",   "desc": "Durcissement SSH",          "status": "active",   "version": 2},
    {"id": uid(), "name": "monitoring-conf", "desc": "Configuration monitoring",  "status": "draft",    "version": 1},
    {"id": uid(), "name": "policy",          "desc": "politique",                 "status": "archived", "version": 3},
]

# Generation SQL ---------------------------------------------------

lines = [f"-- LinuxAD - Donnees factices - Genere le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"]

lines.append("\n-- Admin Users")
for u in admin_users:
    lines.append(f"INSERT INTO admin_users (id, username, email, password_hash, role, mfa_enabled, created_at) VALUES ('{u['id']}', '{u['username']}', '{u['email']}', '{sha256(u['password'])}', '{u['role']}', {'TRUE' if u['mfa'] else 'FALSE'}, '{rand_date(90)}') ON CONFLICT DO NOTHING;")

lines.append("\n-- Machines")
for m in machines:
    lines.append(f"INSERT INTO machines (id, hostname, fqdn, os_version, kernel_version, status, enrolled_at, last_contact) VALUES ('{m['id']}', '{m['hostname']}', '{m['fqdn']}', '{m['os']}', '{m['kernel']}', '{m['status']}', '{rand_date(60)}', '{rand_date(2)}') ON CONFLICT DO NOTHING;")

lines.append("\n-- Agents")
for m in machines:
    status = "online" if m["status"] == "active" else "offline"
    lines.append(f"INSERT INTO agents (id, machine_id, secret_hash, status, enrolled_at, last_seen, ip_address, agent_version) VALUES ('{uid()}', '{m['id']}', '{sha256('agent_secret_' + m['hostname'])}', '{status}', '{rand_date(60)}', '{rand_date(1)}', '192.168.1.{random.randint(10,200)}', '1.0.0') ON CONFLICT DO NOTHING;")

lines.append("\n-- Groups")
for g in groups:
    lines.append(f"INSERT INTO \"groups\" (id, name, description, ldap_dn) VALUES ('{g['id']}', '{g['name']}', '{g['desc']}', 'cn={g['name']},ou=Groups,dc=linuxad,dc=local') ON CONFLICT DO NOTHING;")

lines.append("\n-- Users LDAP")
admin_id = admin_users[0]['id']
for u in ldap_users:
    lines.append(f"INSERT INTO users (uid, ldap_dn, cn, email, uid_number, gid_number, home_directory, created_by) VALUES ('{u['uid']}', 'uid={u['uid']},ou=People,dc=linuxad,dc=local', '{u['cn']}', '{u['email']}', {u['uid_number']}, {u['gid']}, '/home/{u['uid']}', '{admin_id}') ON CONFLICT DO NOTHING;")

lines.append("\n-- GPO")
gpo_content = '{\"schema_version\": \"1.0\", \"policies\": []}'
for g in gpos:
    sig = sha256(g['name'] + str(g['version']))
    lines.append(f"INSERT INTO gpo (id, name, description, version, status, content, signature, created_at, updated_at) VALUES ('{g['id']}', '{g['name']}', '{g['desc']}', {g['version']}, '{g['status']}', '{gpo_content}', '{sig}', '{rand_date(30)}', '{rand_date(5)}') ON CONFLICT DO NOTHING;")

lines.append("\n-- GPO Assignments")
for g in [g for g in gpos if g['status'] == 'active']:
    lines.append(f"INSERT INTO gpo_assignments (id, gpo_id, target_type, priority, enabled) VALUES ('{uid()}', '{g['id']}', 'all', 100, TRUE) ON CONFLICT DO NOTHING;")

lines.append("\n-- Audit Logs")
actions_list = ["login", "create", "update", "delete", "enroll"]
resources    = ["machine", "user", "gpo", "group"]
for i in range(10):
    lines.append(f"INSERT INTO audit_logs (id, actor_type, actor_id, action, resource_type, ip_address, timestamp) VALUES ('{uid()}', 'admin', '{admin_users[0]['id']}', '{random.choice(actions_list)}', '{random.choice(resources)}', '10.0.0.{random.randint(1,10)}', '{rand_date(7)}') ON CONFLICT DO NOTHING;")

lines.append("\n-- Agent Logs")
levels     = ["info", "warning", "error"]
categories = ["gpo", "system", "security", "network"]
for m in machines[:3]:
    for i in range(3):
        lines.append(f"INSERT INTO agent_logs (id, agent_id, timestamp, level, category, message) VALUES ('{uid()}', (SELECT id FROM agents WHERE machine_id = '{m['id']}' LIMIT 1), '{rand_date(3)}', '{random.choice(levels)}', '{random.choice(categories)}', 'Log {i+1} for {m['hostname']}') ON CONFLICT DO NOTHING;")

lines.append("\n-- Enrollment Tokens")
for i in range(3):
    exp = (datetime.now() + timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')
    lines.append(f"INSERT INTO enrollment_tokens (id, token_hash, description, max_uses, current_uses, expires_at, status, created_by) VALUES ('{uid()}', '{sha256('token_' + str(i))}', 'Token de test {i+1}', 10, {random.randint(0,3)}, '{exp}', 'active', '{admin_id}') ON CONFLICT DO NOTHING;")

lines.append("\n-- Settings")
settings = [
    ("general",  '{"domain": "linuxad.local", "organization": "LinuxAD"}'),
    ("agent",    '{"default_poll_interval": 60, "max_poll_interval": 300, "secret_rotation_days": 30, "log_batch_size": 100}'),
    ("security", '{"jwt_expiration_seconds": 3600, "mfa_enabled": false, "password_min_length": 12, "max_login_attempts": 5, "lockout_duration_minutes": 15}'),
    ("ldap",     '{"base_dn": "dc=linuxad,dc=local", "uid_start": 10000, "gid_start": 10000}'),
    ("logs",     '{"retention_audit_days": 365, "retention_security_days": 180, "retention_gpo_days": 90, "retention_system_days": 30, "retention_debug_days": 7}'),
]
for key, value in settings:
    lines.append(f"INSERT INTO settings (key, value) VALUES ('{key}', '{value}') ON CONFLICT DO NOTHING;")

# Ecriture ---------------------------------------------------
os.makedirs("init", exist_ok=True)
output_path = os.path.join("init", "linuxad_fake_data.sql")
with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Fichier genere : {output_path}")
print(f"  {len(admin_users)} admin_users | {len(machines)} machines | {len(groups)} groups | {len(ldap_users)} users | {len(gpos)} gpo")