import hashlib
import uuid
import random
from datetime import datetime, timedelta

def sha256(s):
    return hashlib.sha256(s.encode()).hexdigest()

def uid():
    return str(uuid.uuid4())

def now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def rand_date(days_back=30):
    d = datetime.now() - timedelta(days=random.randint(0, days_back))
    return d.strftime('%Y-%m-%d %H:%M:%S')

# Données ---------------------------------------------------

admin_users = [
    {"id": uid(), "username": "admin", "email": "admin@linuxad.local", "password": "Admin1234!", "role": "superadmin", "mfa": False},
    {"id": uid(), "username": "h", "email": "sysadmin@linuxad.local", "password": "Nopassword1!", "role": "operator", "mfa": True},
    {"id": uid(), "username": "k", "email": "k@linuxad.local", "password": "le deniec'est mal", "role": "viewer", "mfa": False},
    {"id": uid(), "username": "t", "email": "t@linuxad.local", "password": "coucou", "role": "admin", "mfa": True},
    {"id": uid(), "username": "o", "email": "o@linuxad.local", "password": "own", "role": "operator", "mfa": False}
]

machines = [
    {"id": uid(), "hostname": "webapp-01", "fqdn": "webapp-01.linuxad.local", "os": "Debian 13", "kernel": "6.12.38", "status": "active"},
    {"id": uid(), "hostname": "webapp-02", "fqdn": "webapp-02.linuxad.local", "os": "Debian 13", "kernel": "6.12.38", "status": "rolled_back"},
    {"id": uid(), "hostname": "db-master", "fqdn": "db-master.linuxad.local", "os": "Alpine", "kernel": "6.12.38", "status": "active"},
    {"id": uid(), "hostname": "db-replica", "fqdn": "db-replica.linuxad.local", "os": "FreeBSD", "kernel": "13.0", "status": "inactive"},
    {"id": uid(), "hostname": "monitoring-01", "fqdn": "monitoring-01.linuxad.local", "os": "Arch", "kernel": "6.12.38", "status": "pending"}
]

groups = [
    {"id": uid(), "name": "webapps", "desc": "Serveurs web en prod"},
    {"id": uid(), "name": "database-servers", "desc": "Serveurs de bdd"},
    {"id": uid(), "name": "production", "desc": "Toutes les machines de prod"},
    {"id": uid(), "name": "monitoring", "desc": "Machines de monitoring"}
]

ldap_users = [
    {"uid": "jdoe",   "cn": "John Doe",   "sn": "Doe",   "email": "jdoe@linuxad.local",   "uid_number": 10001, "gid": 10001},
    {"uid": "asmith", "cn": "Alice Smith","sn": "Smith",  "email": "asmith@linuxad.local",  "uid_number": 10002, "gid": 10002},
    {"uid": "bmartin","cn": "Bob Martin", "sn": "Martin", "email": "bmartin@linuxad.local", "uid_number": 10003, "gid": 10003}
]

gpos = [
    {"id": uid(), "name": "security_base", "desc": "Configuration de securite", "status": "active", "version": 4},
    {"id": uid(), "name": "ssh-hardening", "desc": "Durcissement SSH", "status": "active", "version": 2},
    {"id": uid(), "name": "monitoring-conf", "desc": "Configuration monitoring", "status": "draft", "version": 1},
    {"id": uid(), "name": "policy", "desc": "politique", "status": "archived", "version": 3}
]

# Génération SQL ---------------------------------------------------

lines = []
# admin_users
lines.append("\n-- Admin ---------------------------------------------------")
for u in admin_users:
    lines.append(f"""INSERT IGNORE INTO admin_users (id, username, email, password_hash, role, mfa_enabled, created_at) VALUES
  ('{u['id']}', '{u['username']}', '{u['email']}', '{sha256(u['password'])}', '{u['role']}', {'TRUE' if u['mfa'] else 'FALSE'}, '{rand_date(90)}');""")

lines.append("\n-- Machines ---------------------------------------------------")
for m in machines:
    last_contact = rand_date(2)
    lines.append(f"""INSERT IGNORE INTO machines (id, hostname, fqdn, os_version, kernel_version, status, enrolled_at, last_contact) VALUES
  ('{m['id']}', '{m['hostname']}', '{m['fqdn']}', '{m['os']}', '{m['kernel']}', '{m['status']}', '{rand_date(60)}', '{last_contact}');""")

lines.append("\n-- Agents ---------------------------------------------------──")
for m in machines:
    agent_id = uid()
    status = "online" if m["status"] == "active" else "offline"
    lines.append(f"""INSERT IGNORE INTO agents (id, machine_id, secret_hash, status, enrolled_at, last_seen, ip_address, agent_version) VALUES
  ('{agent_id}', '{m['id']}', '{sha256('agent_secret_' + m['hostname'])}', '{status}', '{rand_date(60)}', '{rand_date(1)}', '192.168.1.{random.randint(10,200)}', '1.0.0');""")

lines.append("\n-- Groups ---------------------------------------------------")
for g in groups:
    lines.append(f"""INSERT IGNORE INTO `groups` (id, name, description, ldap_dn) VALUES
  ('{g['id']}', '{g['name']}', '{g['desc']}', 'cn={g['name']},ou=Groups,dc=linuxad,dc=local');""")

lines.append("\n-- Users LDAP ---------------------------------------------------")
admin_id = admin_users[0]['id']
for u in ldap_users:
    lines.append(f"""INSERT IGNORE INTO users (uid, ldap_dn, cn, email, uid_number, gid_number, home_directory, created_by) VALUES
  ('{u['uid']}', 'uid={u['uid']},ou=People,dc=linuxad,dc=local', '{u['cn']}', '{u['email']}', {u['uid_number']}, {u['gid']}, '/home/{u['uid']}', '{admin_id}');""")

lines.append("\n-- GPO --------------------------------------------------")
gpo_content = '{"schema_version": "1.0", "policies": []}'
for g in gpos:
    sig = sha256(g['name'] + str(g['version']))
    lines.append(f"""INSERT IGNORE INTO gpo (id, name, description, version, status, content, signature, created_at, updated_at) VALUES
  ('{g['id']}', '{g['name']}', '{g['desc']}', {g['version']}, '{g['status']}', '{gpo_content}', '{sig}', '{rand_date(30)}', '{rand_date(5)}');""")

lines.append("\n-- GPO Assignments ---------------------------------------------------")
active_gpos = [g for g in gpos if g['status'] == 'active']
for g in active_gpos:
    assign_id = uid()
    lines.append(f"""INSERT IGNORE INTO gpo_assignments (id, gpo_id, target_type, priority, enabled) VALUES
  ('{assign_id}', '{g['id']}', 'all', 100, TRUE);""")

lines.append("\n-- Audit Logs ---------------------------------------------------")
actions_list = ["login", "create", "update", "delete", "enroll"]
resources    = ["machine", "user", "gpo", "group"]
for i in range(10):
    lines.append(f"""INSERT IGNORE INTO audit_logs (id, actor_type, actor_id, action, resource_type, ip_address, timestamp) VALUES
  ('{uid()}', 'admin', '{admin_users[0]['id']}', '{random.choice(actions_list)}', '{random.choice(resources)}', '10.0.0.{random.randint(1,10)}', '{rand_date(7)}');""")

lines.append("\n-- Agent Logs ---------------------------------------------------")
levels      = ["info", "warning", "error"]
categories  = ["gpo", "system", "security", "network"]
for m in machines[:3]:
    for i in range(3):
        lines.append(f"""INSERT IGNORE INTO agent_logs (id, agent_id, timestamp, level, category, message) VALUES
  ('{uid()}', (SELECT id FROM agents WHERE machine_id = '{m['id']}' LIMIT 1), '{rand_date(3)}', '{random.choice(levels)}', '{random.choice(categories)}', 'Test log entry {i+1} for {m['hostname']}');""")

lines.append("\n-- Enrollment Tokens ---------------------------------------------------")
for i in range(3):
    exp = (datetime.now() + timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')
    lines.append(f"""INSERT IGNORE INTO enrollment_tokens (id, token_hash, description, max_uses, current_uses, expires_at, status, created_by) VALUES
  ('{uid()}', '{sha256('token_' + str(i))}', 'Token de test {i+1}', 10, {random.randint(0,3)}, '{exp}', 'active', '{admin_id}');""")

#  Écriture ---------------------------------------------------
output = "\n".join(lines)
with open("./init/linuxad_fake_data.sql", "w", encoding="utf-8") as f:
    f.write(output)

print(" Fichier généré : linuxad_fake_data.sql")
print(f"   {len(admin_users)} admin_users")
print(f"   {len(machines)} machines")
print(f"   {len(machines)} agents")
print(f"   {len(groups)} groups")
print(f"   {len(ldap_users)} users LDAP")
print(f"   {len(gpos)} GPO")
print(f"   10 audit_logs")
print(f"   9 agent_logs")
print(f"   3 enrollment_tokens")