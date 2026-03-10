
-- Admin ---------------------------------------------------
INSERT IGNORE INTO admin_users (id, username, email, password_hash, role, mfa_enabled, created_at) VALUES
  ('8348bf00-5f0b-4166-8cae-3f98ac4a984d', 'admin', 'admin@linuxad.local', '5ce41ada64f1e8ffb0acfaafa622b141438f3a5777785e7f0b830fb73e40d3d6', 'superadmin', FALSE, '2026-01-11 00:40:38');
INSERT IGNORE INTO admin_users (id, username, email, password_hash, role, mfa_enabled, created_at) VALUES
  ('f0a72224-a075-430f-a931-04a19d988f4c', 'h', 'sysadmin@linuxad.local', 'a685113620c42ad011a5d91dffeb171f1c7d0923552c068cd293ea983b72bc41', 'operator', TRUE, '2026-01-12 00:40:38');
INSERT IGNORE INTO admin_users (id, username, email, password_hash, role, mfa_enabled, created_at) VALUES
  ('748a5aa8-1e20-4583-bcf7-3fd5ca0bc181', 'k', 'k@linuxad.local', '5fb442343eda6d210090f101117e7e08a3474c05ce924dd2aa1976183da38c09', 'viewer', FALSE, '2026-01-09 00:40:38');
INSERT IGNORE INTO admin_users (id, username, email, password_hash, role, mfa_enabled, created_at) VALUES
  ('bf681f2c-d106-451b-98ad-0064a94f34c9', 't', 't@linuxad.local', '110812f67fa1e1f0117f6f3d70241c1a42a7b07711a93c2477cc516d9042f9db', 'admin', TRUE, '2026-02-17 00:40:38');
INSERT IGNORE INTO admin_users (id, username, email, password_hash, role, mfa_enabled, created_at) VALUES
  ('1360203a-2445-43da-b0a8-b4a65372b73c', 'o', 'o@linuxad.local', '5b3975651c3cab92d044c096dc30a1c2d9525497457472de48c51ecb363d1f4a', 'operator', FALSE, '2026-02-20 00:40:38');

-- Machines ---------------------------------------------------
INSERT IGNORE INTO machines (id, hostname, fqdn, os_version, kernel_version, status, enrolled_at, last_contact) VALUES
  ('ee7d7a9d-1a98-4bb8-90cd-17b65d475e01', 'webapp-01', 'webapp-01.linuxad.local', 'Debian 13', '6.12.38', 'active', '2026-02-17 00:40:38', '2026-03-09 00:40:38');
INSERT IGNORE INTO machines (id, hostname, fqdn, os_version, kernel_version, status, enrolled_at, last_contact) VALUES
  ('299cccb9-0796-4e30-9a9e-a90bb9cf67fc', 'webapp-02', 'webapp-02.linuxad.local', 'Debian 13', '6.12.38', 'rolled_back', '2026-03-04 00:40:38', '2026-03-10 00:40:38');
INSERT IGNORE INTO machines (id, hostname, fqdn, os_version, kernel_version, status, enrolled_at, last_contact) VALUES
  ('5dbd9cf7-5f09-4658-bf83-1698ebdb6b0e', 'db-master', 'db-master.linuxad.local', 'Alpine', '6.12.38', 'active', '2026-03-10 00:40:38', '2026-03-11 00:40:38');
INSERT IGNORE INTO machines (id, hostname, fqdn, os_version, kernel_version, status, enrolled_at, last_contact) VALUES
  ('9f29b779-aa49-47ef-a694-d90f8f0fc375', 'db-replica', 'db-replica.linuxad.local', 'FreeBSD', '13.0', 'inactive', '2026-02-08 00:40:38', '2026-03-10 00:40:38');
INSERT IGNORE INTO machines (id, hostname, fqdn, os_version, kernel_version, status, enrolled_at, last_contact) VALUES
  ('e0341ef3-4c22-4cc4-a48a-8c3e24d17136', 'monitoring-01', 'monitoring-01.linuxad.local', 'Arch', '6.12.38', 'pending', '2026-01-27 00:40:38', '2026-03-10 00:40:38');

-- Agents ---------------------------------------------------──
INSERT IGNORE INTO agents (id, machine_id, secret_hash, status, enrolled_at, last_seen, ip_address, agent_version) VALUES
  ('45216365-9e34-4f6d-8cba-60a63b426c9d', 'ee7d7a9d-1a98-4bb8-90cd-17b65d475e01', '3503592b4d664f0da138eff1527d118b6f503c0506417549af09f55b45f29dd9', 'online', '2026-01-29 00:40:38', '2026-03-10 00:40:38', '192.168.1.128', '1.0.0');
INSERT IGNORE INTO agents (id, machine_id, secret_hash, status, enrolled_at, last_seen, ip_address, agent_version) VALUES
  ('aa825ff0-30a0-4674-ad6a-9b4ab055ace1', '299cccb9-0796-4e30-9a9e-a90bb9cf67fc', 'a9be22689088d77fc5654071030515455f15972232c7f23f3ccf88cac719d419', 'offline', '2026-02-14 00:40:38', '2026-03-11 00:40:38', '192.168.1.196', '1.0.0');
INSERT IGNORE INTO agents (id, machine_id, secret_hash, status, enrolled_at, last_seen, ip_address, agent_version) VALUES
  ('d912c76e-4643-4ca9-bba6-a49aa94a1ecb', '5dbd9cf7-5f09-4658-bf83-1698ebdb6b0e', 'c955bc4980b4060de077c7cd96d258b2836949143357bccd2695550b6f817d13', 'online', '2026-01-15 00:40:38', '2026-03-10 00:40:38', '192.168.1.158', '1.0.0');
INSERT IGNORE INTO agents (id, machine_id, secret_hash, status, enrolled_at, last_seen, ip_address, agent_version) VALUES
  ('9bf1b482-3823-43e0-847e-c6c976b0403f', '9f29b779-aa49-47ef-a694-d90f8f0fc375', '717b311a6c2565da50a461c8b4bcc84f00cfb9c7fe92023460a5348cd44dce8e', 'offline', '2026-01-13 00:40:38', '2026-03-11 00:40:38', '192.168.1.57', '1.0.0');
INSERT IGNORE INTO agents (id, machine_id, secret_hash, status, enrolled_at, last_seen, ip_address, agent_version) VALUES
  ('802b5df6-1ef7-407e-8169-953d5b230092', 'e0341ef3-4c22-4cc4-a48a-8c3e24d17136', 'ecadc7fde3ffa2245b30d5fc8038ea906203d24a2c133b6ba04a4c0a39770bc5', 'offline', '2026-02-16 00:40:38', '2026-03-10 00:40:38', '192.168.1.101', '1.0.0');

-- Groups ---------------------------------------------------
INSERT IGNORE INTO `groups` (id, name, description, ldap_dn) VALUES
  ('7a274ad0-f160-4e7f-bbcc-bfff0d1b865d', 'webapps', 'Serveurs web en prod', 'cn=webapps,ou=Groups,dc=linuxad,dc=local');
INSERT IGNORE INTO `groups` (id, name, description, ldap_dn) VALUES
  ('1bda4dff-6a65-4ec1-958f-512521e8dd51', 'database-servers', 'Serveurs de bdd', 'cn=database-servers,ou=Groups,dc=linuxad,dc=local');
INSERT IGNORE INTO `groups` (id, name, description, ldap_dn) VALUES
  ('0e233bbe-9541-4906-ae95-06239b38c400', 'production', 'Toutes les machines de prod', 'cn=production,ou=Groups,dc=linuxad,dc=local');
INSERT IGNORE INTO `groups` (id, name, description, ldap_dn) VALUES
  ('8cf9e433-9b79-4250-af52-bac617ff11e3', 'monitoring', 'Machines de monitoring', 'cn=monitoring,ou=Groups,dc=linuxad,dc=local');

-- Users LDAP ---------------------------------------------------
INSERT IGNORE INTO users (uid, ldap_dn, cn, email, uid_number, gid_number, home_directory, created_by) VALUES
  ('jdoe', 'uid=jdoe,ou=People,dc=linuxad,dc=local', 'John Doe', 'jdoe@linuxad.local', 10001, 10001, '/home/jdoe', '8348bf00-5f0b-4166-8cae-3f98ac4a984d');
INSERT IGNORE INTO users (uid, ldap_dn, cn, email, uid_number, gid_number, home_directory, created_by) VALUES
  ('asmith', 'uid=asmith,ou=People,dc=linuxad,dc=local', 'Alice Smith', 'asmith@linuxad.local', 10002, 10002, '/home/asmith', '8348bf00-5f0b-4166-8cae-3f98ac4a984d');
INSERT IGNORE INTO users (uid, ldap_dn, cn, email, uid_number, gid_number, home_directory, created_by) VALUES
  ('bmartin', 'uid=bmartin,ou=People,dc=linuxad,dc=local', 'Bob Martin', 'bmartin@linuxad.local', 10003, 10003, '/home/bmartin', '8348bf00-5f0b-4166-8cae-3f98ac4a984d');

-- GPO --------------------------------------------------
INSERT IGNORE INTO gpo (id, name, description, version, status, content, signature, created_at, updated_at) VALUES
  ('5cb79fa4-5837-45f4-9e66-dfb2515c3fe0', 'security_base', 'Configuration de securite', 4, 'active', '{"schema_version": "1.0", "policies": []}', '3b712f62c201287fe9868bf2904cb16e0a7ef1daf5b606cc98d88d4d0fc63784', '2026-02-23 00:40:38', '2026-03-11 00:40:38');
INSERT IGNORE INTO gpo (id, name, description, version, status, content, signature, created_at, updated_at) VALUES
  ('a9cf0068-b6bc-4a4d-a171-a24e743617f0', 'ssh-hardening', 'Durcissement SSH', 2, 'active', '{"schema_version": "1.0", "policies": []}', '63c64919f7a9738024cb499265c5e5097bb7816acbb9f0e988cf677c0e86510d', '2026-03-07 00:40:38', '2026-03-09 00:40:38');
INSERT IGNORE INTO gpo (id, name, description, version, status, content, signature, created_at, updated_at) VALUES
  ('25f89749-f5aa-4dc2-b811-bdd5b3215d5b', 'monitoring-conf', 'Configuration monitoring', 1, 'draft', '{"schema_version": "1.0", "policies": []}', 'd300a8807833e15bf22a45e313d3f8fd97fca248f65d5b6e7bd0180f34163275', '2026-03-10 00:40:38', '2026-03-11 00:40:38');
INSERT IGNORE INTO gpo (id, name, description, version, status, content, signature, created_at, updated_at) VALUES
  ('0dbce17d-5f7a-4305-ba8b-17cc49c5a55d', 'policy', 'politique', 3, 'archived', '{"schema_version": "1.0", "policies": []}', '71c06ee1a48cfe649a301a45bebd78a62ceee8418cbf0462665b54ff3549333d', '2026-02-14 00:40:38', '2026-03-09 00:40:38');

-- GPO Assignments ---------------------------------------------------
INSERT IGNORE INTO gpo_assignments (id, gpo_id, target_type, priority, enabled) VALUES
  ('4d111431-e689-4e4d-aac2-6450723c012c', '5cb79fa4-5837-45f4-9e66-dfb2515c3fe0', 'all', 100, TRUE);
INSERT IGNORE INTO gpo_assignments (id, gpo_id, target_type, priority, enabled) VALUES
  ('2db431ef-37f3-47ba-af3c-ac0c50f0c8f6', 'a9cf0068-b6bc-4a4d-a171-a24e743617f0', 'all', 100, TRUE);

-- Audit Logs ---------------------------------------------------
INSERT IGNORE INTO audit_logs (id, actor_type, actor_id, action, resource_type, ip_address, timestamp) VALUES
  ('53fcd1c1-53e1-40c0-88cd-6b4e3e85a2ee', 'admin', '8348bf00-5f0b-4166-8cae-3f98ac4a984d', 'login', 'user', '10.0.0.5', '2026-03-05 00:40:38');
INSERT IGNORE INTO audit_logs (id, actor_type, actor_id, action, resource_type, ip_address, timestamp) VALUES
  ('39053e7b-2bc2-401b-ab93-54086e76dc3d', 'admin', '8348bf00-5f0b-4166-8cae-3f98ac4a984d', 'create', 'user', '10.0.0.8', '2026-03-05 00:40:38');
INSERT IGNORE INTO audit_logs (id, actor_type, actor_id, action, resource_type, ip_address, timestamp) VALUES
  ('c4fac930-2920-4585-bd68-f36fe6d57eb5', 'admin', '8348bf00-5f0b-4166-8cae-3f98ac4a984d', 'enroll', 'machine', '10.0.0.5', '2026-03-04 00:40:38');
INSERT IGNORE INTO audit_logs (id, actor_type, actor_id, action, resource_type, ip_address, timestamp) VALUES
  ('156d8ac9-b43b-4a06-b26a-f7603c1e03fa', 'admin', '8348bf00-5f0b-4166-8cae-3f98ac4a984d', 'update', 'gpo', '10.0.0.4', '2026-03-04 00:40:38');
INSERT IGNORE INTO audit_logs (id, actor_type, actor_id, action, resource_type, ip_address, timestamp) VALUES
  ('09414423-de1c-449c-aeec-e9a2f68384da', 'admin', '8348bf00-5f0b-4166-8cae-3f98ac4a984d', 'create', 'group', '10.0.0.6', '2026-03-10 00:40:38');
INSERT IGNORE INTO audit_logs (id, actor_type, actor_id, action, resource_type, ip_address, timestamp) VALUES
  ('d64e9438-3fc3-4a52-8f07-70a69fc0276a', 'admin', '8348bf00-5f0b-4166-8cae-3f98ac4a984d', 'update', 'group', '10.0.0.9', '2026-03-06 00:40:38');
INSERT IGNORE INTO audit_logs (id, actor_type, actor_id, action, resource_type, ip_address, timestamp) VALUES
  ('c708df0e-a334-47ac-bca8-5d92e73b2bc6', 'admin', '8348bf00-5f0b-4166-8cae-3f98ac4a984d', 'update', 'machine', '10.0.0.5', '2026-03-06 00:40:38');
INSERT IGNORE INTO audit_logs (id, actor_type, actor_id, action, resource_type, ip_address, timestamp) VALUES
  ('4e6c3d62-6203-4f5e-b3c8-126dd2973274', 'admin', '8348bf00-5f0b-4166-8cae-3f98ac4a984d', 'enroll', 'gpo', '10.0.0.3', '2026-03-05 00:40:38');
INSERT IGNORE INTO audit_logs (id, actor_type, actor_id, action, resource_type, ip_address, timestamp) VALUES
  ('0737b967-9043-46ef-b22f-551298c72de4', 'admin', '8348bf00-5f0b-4166-8cae-3f98ac4a984d', 'login', 'machine', '10.0.0.5', '2026-03-11 00:40:38');
INSERT IGNORE INTO audit_logs (id, actor_type, actor_id, action, resource_type, ip_address, timestamp) VALUES
  ('61f2120b-b285-4ae3-90c6-57b00c700bfd', 'admin', '8348bf00-5f0b-4166-8cae-3f98ac4a984d', 'enroll', 'user', '10.0.0.9', '2026-03-07 00:40:38');

-- Agent Logs ---------------------------------------------------
INSERT IGNORE INTO agent_logs (id, agent_id, timestamp, level, category, message) VALUES
  ('382520a4-be68-4e77-ac1d-76a158c5b887', (SELECT id FROM agents WHERE machine_id = 'ee7d7a9d-1a98-4bb8-90cd-17b65d475e01' LIMIT 1), '2026-03-10 00:40:38', 'info', 'system', 'Test log entry 1 for webapp-01');
INSERT IGNORE INTO agent_logs (id, agent_id, timestamp, level, category, message) VALUES
  ('6366e76b-c443-499c-990b-9b6f654c5cc7', (SELECT id FROM agents WHERE machine_id = 'ee7d7a9d-1a98-4bb8-90cd-17b65d475e01' LIMIT 1), '2026-03-10 00:40:38', 'warning', 'network', 'Test log entry 2 for webapp-01');
INSERT IGNORE INTO agent_logs (id, agent_id, timestamp, level, category, message) VALUES
  ('15af52e4-eb64-467e-a483-e592ddd27891', (SELECT id FROM agents WHERE machine_id = 'ee7d7a9d-1a98-4bb8-90cd-17b65d475e01' LIMIT 1), '2026-03-11 00:40:38', 'warning', 'gpo', 'Test log entry 3 for webapp-01');
INSERT IGNORE INTO agent_logs (id, agent_id, timestamp, level, category, message) VALUES
  ('ebfe8b2c-eba3-40f3-8284-bc6ceb4b1a69', (SELECT id FROM agents WHERE machine_id = '299cccb9-0796-4e30-9a9e-a90bb9cf67fc' LIMIT 1), '2026-03-09 00:40:38', 'info', 'gpo', 'Test log entry 1 for webapp-02');
INSERT IGNORE INTO agent_logs (id, agent_id, timestamp, level, category, message) VALUES
  ('f3e01062-d762-4ba7-a6e3-bf4f975eb8e9', (SELECT id FROM agents WHERE machine_id = '299cccb9-0796-4e30-9a9e-a90bb9cf67fc' LIMIT 1), '2026-03-09 00:40:38', 'info', 'security', 'Test log entry 2 for webapp-02');
INSERT IGNORE INTO agent_logs (id, agent_id, timestamp, level, category, message) VALUES
  ('6ac39f48-d513-48e9-b674-64f19b8bb798', (SELECT id FROM agents WHERE machine_id = '299cccb9-0796-4e30-9a9e-a90bb9cf67fc' LIMIT 1), '2026-03-11 00:40:38', 'info', 'gpo', 'Test log entry 3 for webapp-02');
INSERT IGNORE INTO agent_logs (id, agent_id, timestamp, level, category, message) VALUES
  ('9025fc0b-438e-40df-ac92-8ff5d5bee2d2', (SELECT id FROM agents WHERE machine_id = '5dbd9cf7-5f09-4658-bf83-1698ebdb6b0e' LIMIT 1), '2026-03-09 00:40:38', 'warning', 'network', 'Test log entry 1 for db-master');
INSERT IGNORE INTO agent_logs (id, agent_id, timestamp, level, category, message) VALUES
  ('48a2e86b-bdc4-4397-8b2f-98399a51424a', (SELECT id FROM agents WHERE machine_id = '5dbd9cf7-5f09-4658-bf83-1698ebdb6b0e' LIMIT 1), '2026-03-09 00:40:38', 'error', 'gpo', 'Test log entry 2 for db-master');
INSERT IGNORE INTO agent_logs (id, agent_id, timestamp, level, category, message) VALUES
  ('8edc21d1-4447-4e22-9ff9-797deafdebd2', (SELECT id FROM agents WHERE machine_id = '5dbd9cf7-5f09-4658-bf83-1698ebdb6b0e' LIMIT 1), '2026-03-11 00:40:38', 'error', 'gpo', 'Test log entry 3 for db-master');

-- Enrollment Tokens ---------------------------------------------------
INSERT IGNORE INTO enrollment_tokens (id, token_hash, description, max_uses, current_uses, expires_at, status, created_by) VALUES
  ('2d316bdd-6a0b-4168-a532-b9b3f135ea64', 'ae5427ca3ceb2dc7ba7b2b23f28164e7ad7a3cbc7125aa8899aa2b3fa7aded7e', 'Token de test 1', 10, 0, '2026-03-12 00:40:38', 'active', '8348bf00-5f0b-4166-8cae-3f98ac4a984d');
INSERT IGNORE INTO enrollment_tokens (id, token_hash, description, max_uses, current_uses, expires_at, status, created_by) VALUES
  ('77b1202c-6ea6-46b1-adc3-35d831c5f33b', 'ccee1a67bb5b1c0b2cc95e39dfa8ed366388a3664558f408e0a606569337251d', 'Token de test 2', 10, 3, '2026-03-12 00:40:38', 'active', '8348bf00-5f0b-4166-8cae-3f98ac4a984d');
INSERT IGNORE INTO enrollment_tokens (id, token_hash, description, max_uses, current_uses, expires_at, status, created_by) VALUES
  ('8f24aa97-69e0-4a3e-bccb-d6c53f731126', '403d2b0f6874f04d0b86da34a1ea338c811bfa6a5529b37d4d73ef09c544f81e', 'Token de test 3', 10, 3, '2026-03-12 00:40:38', 'active', '8348bf00-5f0b-4166-8cae-3f98ac4a984d');