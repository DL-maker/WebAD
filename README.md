# WebAD — Faux Agent (Mock API)

Stack locale pour simuler le backend FastAPI pendant le développement du dashboard SvelteKit.

- **PostgreSQL 16** via Docker (port 5432)
- **relay.py** — serveur HTTP python3 sur le port 4444

---

## 1. Installation des dépendances

```bash
pip install psycopg2 pyotp pyjwt
```

---

## 2. Lancer la base de données

```bash
cd src/faux_agent
docker-compose down -v
python3 bdd.py
docker-compose up -d
```
---

## 3. Lancer le relay

Dans un autre terminal :

```bash
python3 relay.py
```

Le relay écoute sur `http://127.0.0.1:4444`.

---

## 4. Obtenir un token JWT

> **Note** : Le token JWT est généré de manière aléatoire à chaque login via la bibliothèque **PyJWT** (algorithme HS256) avec une expiration de 3600 secondes. Le secret TOTP pour le MFA est également généré de manière aléatoire via **pyotp** (`pyotp.random_base32()`) — un secret différent est produit à chaque appel de `/mfa/setup`.

```bash
curl -X POST http://127.0.0.1:4444/api/v1/admin/auth/login -H "Content-Type: application/json" -d '{
  "username": "admin",
  "password": "Admin1234!"
}'
```

Comptes de test :

| username | password | role |
|---|---|---|
| admin | Admin1234! | superadmin |
| h | Nopassword1! | operator (MFA requis) |
| k | le deniec est mal | viewer |
| t | coucou | admin (MFA requis) |
| o | own | operator |

---

## 5. Inspecter la base de données

Lister toutes les tables :

```bash
docker exec linuxad_db psql -U postgres -d linuxad -c "\dt"
```

Voir les admin_users :

```bash
docker exec linuxad_db psql -U postgres -d linuxad -c "SELECT * FROM admin_users;"
```

Voir les machines :

```bash
docker exec linuxad_db psql -U postgres -d linuxad -c "SELECT * FROM machines;"
```

Voir les agents :

```bash
docker exec linuxad_db psql -U postgres -d linuxad -c "SELECT * FROM agents;"
```

Voir les groupes :

```bash
docker exec linuxad_db psql -U postgres -d linuxad -c "SELECT * FROM \"groups\";"
```

Voir les utilisateurs LDAP :

```bash
docker exec linuxad_db psql -U postgres -d linuxad -c "SELECT * FROM users;"
```

Voir les GPO :

```bash
docker exec linuxad_db psql -U postgres -d linuxad -c "SELECT * FROM gpo;"
```

Voir les tokens d'enrôlement :

```bash
docker exec linuxad_db psql -U postgres -d linuxad -c "SELECT * FROM enrollment_tokens;"
```

Voir les logs d'audit :

```bash
docker exec linuxad_db psql -U postgres -d linuxad -c "SELECT * FROM audit_logs;"
```

---

## 6. Récupérer les IDs des éléments

IDs des machines :

```bash
curl http://127.0.0.1:4444/api/v1/admin/machines
```

UIDs des utilisateurs LDAP :

```bash
curl http://127.0.0.1:4444/api/v1/admin/users
```

IDs des groupes :

```bash
curl http://127.0.0.1:4444/api/v1/admin/groups
```

IDs des GPO :

```bash
curl http://127.0.0.1:4444/api/v1/admin/gpo
```

IDs des tokens d'enrôlement :

```bash
curl http://127.0.0.1:4444/api/v1/enrollment/tokens
```

IDs des comptes admin :

```bash
curl http://127.0.0.1:4444/api/v1/admin/admin-users
```

---

## 7. Routes principales

### Auth

```bash
curl -X POST http://127.0.0.1:4444/api/v1/admin/auth/refresh -H "Content-Type: application/json" -d '{"refresh_token": "linuxad_refresh_1_8c6976e5b541"}'
```

```bash
curl -X POST http://127.0.0.1:4444/api/v1/admin/auth/logout -H "Content-Type: application/json" -d '{"refresh_token": "linuxad_refresh_1_8c6976e5b541"}'
```

### Machines

Lister :

```bash
curl http://127.0.0.1:4444/api/v1/admin/machines
```

Détail :

```bash
curl http://127.0.0.1:4444/api/v1/admin/machines/<machine_id>
```

Supprimer :

```bash
curl -X DELETE http://127.0.0.1:4444/api/v1/admin/machines/<machine_id>
```

### Utilisateurs LDAP

Lister :

```bash
curl http://127.0.0.1:4444/api/v1/admin/users
```

Créer :

```bash
curl -X POST http://127.0.0.1:4444/api/v1/admin/users -H "Content-Type: application/json" -d '{
  "uid": "nouveauuser",
  "cn": "Nouveau User",
  "sn": "User",
  "email": "nouveau@linuxad.local",
  "password": "SecurePass123!"
}'
```

Supprimer :

```bash
curl -X DELETE http://127.0.0.1:4444/api/v1/admin/users/<uid>
```

### Groupes

Lister :

```bash
curl http://127.0.0.1:4444/api/v1/admin/groups
```

Créer :

```bash
curl -X POST http://127.0.0.1:4444/api/v1/admin/groups -H "Content-Type: application/json" -d '{
  "name": "devops",
  "description": "Equipe devops"
}'
```

Ajouter une machine à un groupe :

```bash
curl -X POST http://127.0.0.1:4444/api/v1/admin/groups/<group_id>/members -H "Content-Type: application/json" -d '{
  "add": ["<machine_id>"],
  "remove": []
}'
```

Supprimer :

```bash
curl -X DELETE http://127.0.0.1:4444/api/v1/admin/groups/<group_id>
```

### GPO

Lister :

```bash
curl http://127.0.0.1:4444/api/v1/admin/gpo
```

Créer :

```bash
curl -X POST http://127.0.0.1:4444/api/v1/admin/gpo -H "Content-Type: application/json" -d '{
  "name": "nouvelle-gpo",
  "description": "Description"
}'
```

Signer (activer) :

```bash
curl -X POST http://127.0.0.1:4444/api/v1/admin/gpo/<gpo_id>/sign
```

### Enrôlement

Créer un token :

```bash
curl -X POST http://127.0.0.1:4444/api/v1/enrollment/tokens -H "Content-Type: application/json" -d '{
  "description": "Token prod",
  "max_uses": 5,
  "expires_in_hours": 24
}'
```

Enrôler une machine :

```bash
curl -X POST http://127.0.0.1:4444/api/v1/enrollment/enroll -H "Content-Type: application/json" -d '{
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

## ⚠️ Warning — Stockage des IPs des agents

> Dans la version actuelle, l'adresse IP de chaque machine cliente (agent) est stockée dans la table `agents` colonne `ip_address`, insérée lors de l'enrôlement via `POST /api/v1/enrollment/enroll` (champ `network_info.primary_ip`).
>
> Elle est aussi mise à jour à chaque poll via `POST /api/v1/agent/poll`.
>
> Dans la future implémentation réelle (FastAPI + OpenLDAP), cette IP devra être synchronisée avec les enregistrements DNS/LDAP pour que SSSD puisse résoudre les machines correctement.

---

## Reset complet

```bash
docker-compose down -v
python3 bdd.py
docker-compose up -d
```