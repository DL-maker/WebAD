# WebAD — Faux Agent (Mock API)

Simuler le backend FastAPI pendant le développement du dashboard SvelteKit.

- **PostgreSQL 16** via Docker (port 5432)
- **relay.py** — serveur HTTP python3 sur le port 4444

---

## Démarrage

### 1. Requirement
```bash
pip install psycopg2
```

### 2. Lancer la bdd
```bash
cd src/faux_agent
docker-compose down -v
python3 bdd.py
docker-compose up -d
```

### 3. Lancer le relay
Dans un autre terminal :
```bash
python3 relay.py
```
Le relay écoute sur `http://127.0.0.1:4444`.

---

## Auth
Comptes de test :

| username | password | role |
|---|---|---|
| admin | Admin1234! | superadmin |
| h | Nopassword1! | operator (MFA requis) |
| k | le deniec est mal | viewer |
| t | coucou | admin (MFA requis) |
| o | own | operator |

### Login
```bash
curl -X POST http://127.0.0.1:4444/api/v1/admin/auth/login \
  -H "Content-Type: application/json" \
  -d '{
  "username": "admin",
  "password": "Admin1234!"
}'
```

### Refresh token
```bash
curl -X POST http://127.0.0.1:4444/api/v1/admin/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{
  "refresh_token": "linuxad_refresh_1_8c6976e5b541"
}'
```

### Logout
```bash
curl -X POST http://127.0.0.1:4444/api/v1/admin/auth/logout \
  -H "Content-Type: application/json" \
  -d '{
  "refresh_token": "linuxad_refresh_1_8c6976e5b541"
}'
```

---

## Machines
Lister les machines :

```bash
curl http://127.0.0.1:4444/api/v1/admin/machines
```

Détail d'une machine :
```bash
curl http://127.0.0.1:4444/api/v1/admin/machines/<machine_id>
```

Supprimer une machine :
```bash
curl -X DELETE http://127.0.0.1:4444/api/v1/admin/machines/<machine_id>
```

---

## Utilisateurs LDAP

Lister :
```bash
curl http://127.0.0.1:4444/api/v1/admin/users
```

Détail d'un user :
```bash
curl http://127.0.0.1:4444/api/v1/admin/users/jdoe
```

Créer un user :
```bash
curl -X POST http://127.0.0.1:4444/api/v1/admin/users \
  -H "Content-Type: application/json" \
  -d '{
  "uid": "nouveauuser",
  "cn": "Nouveau User",
  "sn": "User",
  "email": "nouveau@linuxad.local",
  "password": "SecurePass123!"
}'
```

Modifier :
```bash
curl -X PATCH http://127.0.0.1:4444/api/v1/admin/users/jdoe \
  -H "Content-Type: application/json" \
  -d '{
  "cn": "John D.",
  "login_shell": "/bin/zsh"
}'
```

Reset mot de passe :
```bash
curl -X POST http://127.0.0.1:4444/api/v1/admin/users/jdoe/password \
  -H "Content-Type: application/json" \
  -d '{
  "new_password": "NewSecurePass123!",
  "force_change_on_login": true
}'
```

Supprimer :
```bash
curl -X DELETE http://127.0.0.1:4444/api/v1/admin/users/jdoe
```

---

## Groupes

Lister :
```bash
curl http://127.0.0.1:4444/api/v1/admin/groups
```

Créer :
```bash
curl -X POST http://127.0.0.1:4444/api/v1/admin/groups \
  -H "Content-Type: application/json" \
  -d '{
  "name": "devops",
  "description": "Equipe devops"
}'
```

Modifier :
```bash
curl -X PATCH http://127.0.0.1:4444/api/v1/admin/groups/<group_id> \
  -H "Content-Type: application/json" \
  -d '{
  "description": "Equipe devops (renomme)"
}'
```

Ajouter/retirer des machines :
```bash
curl -X POST http://127.0.0.1:4444/api/v1/admin/groups/<group_id>/members \
  -H "Content-Type: application/json" \
  -d '{
  "add": ["<machine_id>"],
  "remove": []
}'
```

Supprimer :
```bash
curl -X DELETE http://127.0.0.1:4444/api/v1/admin/groups/<group_id>
```

---

## GPO

Lister :
```bash
curl http://127.0.0.1:4444/api/v1/admin/gpo
```

Dashboard stats :
```bash
curl http://127.0.0.1:4444/api/v1/admin/dashboard/stats
```

---

## Enrôlement

Créer un token :
```bash
curl -X POST http://127.0.0.1:4444/api/v1/enrollment/tokens \
  -H "Content-Type: application/json" \
  -d '{
  "description": "Token prod",
  "max_uses": 5,
  "expires_in_hours": 24
}'
```

Lister les tokens :
```bash
curl http://127.0.0.1:4444/api/v1/enrollment/tokens
```

Révoquer un token :
```bash
curl -X DELETE http://127.0.0.1:4444/api/v1/enrollment/tokens/<token_id>
```

Enrôler une machine :
```bash
curl -X POST http://127.0.0.1:4444/api/v1/enrollment/enroll \
  -H "Content-Type: application/json" \
  -d '{
  "enrollment_token": "linuxad_enroll_1_xxx",
  "hostname": "srv-01",
  "fqdn": "srv-01.linuxad.local",
  "os_info": {
    "distribution": "Debian",
    "version": "13",
    "kernel": "6.12"
  },
  "network_info": {
    "primary_ip": "192.168.1.50"
  },
  "agent_version": "1.0.0"
}'
```

---

## Reset complet

```bash
docker-compose down -v
python3 bdd.py
docker-compose up -d
```