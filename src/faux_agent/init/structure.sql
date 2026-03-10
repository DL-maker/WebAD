-- ============================================================
-- LinuxAD - Schéma MySQL complet
-- À placer dans init/01_schema.sql
-- ============================================================

CREATE TABLE IF NOT EXISTS admin_users (
    id            VARCHAR(36)  PRIMARY KEY,
    username      VARCHAR(100) UNIQUE NOT NULL,
    email         VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(64)  NOT NULL,
    role          VARCHAR(20)  NOT NULL DEFAULT 'admin',
    mfa_enabled   BOOLEAN      NOT NULL DEFAULT FALSE,
    created_at    DATETIME     NOT NULL DEFAULT NOW(),
    last_login    DATETIME
);

CREATE TABLE IF NOT EXISTS machines (
    id             VARCHAR(36)  PRIMARY KEY,
    hostname       VARCHAR(255) UNIQUE NOT NULL,
    fqdn           VARCHAR(255),
    os_version     VARCHAR(100),
    kernel_version VARCHAR(100),
    status         VARCHAR(20)  NOT NULL DEFAULT 'pending',
    enrolled_at    DATETIME     NOT NULL DEFAULT NOW(),
    last_contact   DATETIME
);

CREATE TABLE IF NOT EXISTS agents (
    id            VARCHAR(36)  PRIMARY KEY,
    machine_id    VARCHAR(36)  NOT NULL,
    secret_hash   VARCHAR(64)  NOT NULL,
    status        VARCHAR(20)  NOT NULL DEFAULT 'offline',
    enrolled_at   DATETIME     NOT NULL DEFAULT NOW(),
    last_seen     DATETIME,
    ip_address    VARCHAR(45),
    agent_version VARCHAR(20),
    FOREIGN KEY (machine_id) REFERENCES machines(id)
);

CREATE TABLE IF NOT EXISTS `groups` (
    id          VARCHAR(36)  PRIMARY KEY,
    name        VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    ldap_dn     VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS users (
    uid            VARCHAR(100) PRIMARY KEY,
    ldap_dn        VARCHAR(255),
    cn             VARCHAR(255),
    email          VARCHAR(255),
    uid_number     INT UNIQUE,
    gid_number     INT,
    home_directory VARCHAR(255),
    login_shell    VARCHAR(100) DEFAULT '/bin/bash',
    created_by     VARCHAR(36),
    created_at     DATETIME NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS gpo (
    id          VARCHAR(36)  PRIMARY KEY,
    name        VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    version     INT          NOT NULL DEFAULT 1,
    status      VARCHAR(20)  NOT NULL DEFAULT 'draft',
    content     JSON,
    signature   VARCHAR(64),
    created_at  DATETIME     NOT NULL DEFAULT NOW(),
    updated_at  DATETIME     NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS gpo_assignments (
    id          VARCHAR(36)  PRIMARY KEY,
    gpo_id      VARCHAR(36)  NOT NULL,
    target_type VARCHAR(20)  NOT NULL,
    priority    INT          NOT NULL DEFAULT 100,
    enabled     BOOLEAN      NOT NULL DEFAULT TRUE,
    FOREIGN KEY (gpo_id) REFERENCES gpo(id)
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id            VARCHAR(36)  PRIMARY KEY,
    actor_type    VARCHAR(20),
    actor_id      VARCHAR(36),
    action        VARCHAR(100),
    resource_type VARCHAR(50),
    ip_address    VARCHAR(45),
    timestamp     DATETIME     NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS agent_logs (
    id        VARCHAR(36)  PRIMARY KEY,
    agent_id  VARCHAR(36),
    timestamp DATETIME     NOT NULL DEFAULT NOW(),
    level     VARCHAR(20),
    category  VARCHAR(50),
    message   TEXT
);

CREATE TABLE IF NOT EXISTS enrollment_tokens (
    id           VARCHAR(36)  PRIMARY KEY,
    token_hash   VARCHAR(64)  NOT NULL,
    description  TEXT,
    max_uses     INT          NOT NULL DEFAULT 1,
    current_uses INT          NOT NULL DEFAULT 0,
    expires_at   DATETIME,
    status       VARCHAR(20)  NOT NULL DEFAULT 'active',
    created_by   VARCHAR(36),
    created_at   DATETIME     NOT NULL DEFAULT NOW()
);