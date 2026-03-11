
-- Admin ---------------------------------------------------
INSERT INTO admin_users (id, username, email, password_hash, role, mfa_enabled, created_at) VALUES
  ('a591ff7e-f51c-4b0b-ae4d-a20204ccaeab', 'admin', 'admin@linuxad.local', '5ce41ada64f1e8ffb0acfaafa622b141438f3a5777785e7f0b830fb73e40d3d6', 'superadmin', FALSE, '2026-02-18 00:37:35') ON CONFLICT DO NOTHING;
INSERT INTO admin_users (id, username, email, password_hash, role, mfa_enabled, created_at) VALUES
  ('7e679b6d-31bf-4afa-a308-944b72bc083d', 'h', 'sysadmin@linuxad.local', 'a685113620c42ad011a5d91dffeb171f1c7d0923552c068cd293ea983b72bc41', 'operator', TRUE, '2026-03-03 00:37:35') ON CONFLICT DO NOTHING;
INSERT INTO admin_users (id, username, email, password_hash, role, mfa_enabled, created_at) VALUES
  ('77ba57f3-3a8d-48bd-9340-ed9e7bc325fd', 'k', 'k@linuxad.local', '5fb442343eda6d210090f101117e7e08a3474c05ce924dd2aa1976183da38c09', 'viewer', FALSE, '2026-02-10 00:37:35') ON CONFLICT DO NOTHING;
INSERT INTO admin_users (id, username, email, password_hash, role, mfa_enabled, created_at) VALUES
  ('2c9e2e20-d05f-4e2d-b1de-46d6d4c74608', 't', 't@linuxad.local', '110812f67fa1e1f0117f6f3d70241c1a42a7b07711a93c2477cc516d9042f9db', 'admin', TRUE, '2026-03-01 00:37:35') ON CONFLICT DO NOTHING;
INSERT INTO admin_users (id, username, email, password_hash, role, mfa_enabled, created_at) VALUES
  ('f678ff88-7d35-4e86-b50b-655d851e0776', 'o', 'o@linuxad.local', '5b3975651c3cab92d044c096dc30a1c2d9525497457472de48c51ecb363d1f4a', 'operator', FALSE, '2026-02-12 00:37:35') ON CONFLICT DO NOTHING;

-- Machines ---------------------------------------------------
INSERT INTO machines (id, hostname, fqdn, os_version, kernel_version, status, enrolled_at, last_contact) VALUES
  ('50bd5cb9-e796-4f3a-9973-e90fd282bc6f', 'webapp-01', 'webapp-01.linuxad.local', 'Debian 13', '6.12.38', 'active', '2026-03-10 00:37:35', '2026-03-11 00:37:35') ON CONFLICT DO NOTHING;
INSERT INTO machines (id, hostname, fqdn, os_version, kernel_version, status, enrolled_at, last_contact) VALUES
  ('240ba872-6f88-457b-9913-f3bee66a04c8', 'webapp-02', 'webapp-02.linuxad.local', 'Debian 13', '6.12.38', 'rolled_back', '2026-02-08 00:37:35', '2026-03-12 00:37:35') ON CONFLICT DO NOTHING;
INSERT INTO machines (id, hostname, fqdn, os_version, kernel_version, status, enrolled_at, last_contact) VALUES
  ('72bbf13b-a092-43fa-8604-4ad404d4637b', 'db-master', 'db-master.linuxad.local', 'Alpine', '6.12.38', 'active', '2026-01-12 00:37:35', '2026-03-12 00:37:35') ON CONFLICT DO NOTHING;
INSERT INTO machines (id, hostname, fqdn, os_version, kernel_version, status, enrolled_at, last_contact) VALUES
  ('fdcfe20f-f55c-4e21-ad33-2484fd43d426', 'db-replica', 'db-replica.linuxad.local', 'FreeBSD', '13.0', 'inactive', '2026-02-28 00:37:35', '2026-03-10 00:37:35') ON CONFLICT DO NOTHING;
INSERT INTO machines (id, hostname, fqdn, os_version, kernel_version, status, enrolled_at, last_contact) VALUES
  ('6a07ba4a-9b24-49ca-8861-d67c837ecddf', 'monitoring-01', 'monitoring-01.linuxad.local', 'Arch', '6.12.38', 'pending', '2026-02-05 00:37:35', '2026-03-10 00:37:35') ON CONFLICT DO NOTHING;

-- Agents ---------------------------------------------------
INSERT INTO agents (id, machine_id, secret_hash, status, enrolled_at, last_seen, ip_address, agent_version) VALUES
  ('c3902c9b-3e0a-4574-b6c7-c73b039bc396', '50bd5cb9-e796-4f3a-9973-e90fd282bc6f', '3503592b4d664f0da138eff1527d118b6f503c0506417549af09f55b45f29dd9', 'online', '2026-03-05 00:37:35', '2026-03-12 00:37:35', '192.168.1.25', '1.0.0') ON CONFLICT DO NOTHING;
INSERT INTO agents (id, machine_id, secret_hash, status, enrolled_at, last_seen, ip_address, agent_version) VALUES
  ('3b50a209-3f39-4b29-b8c3-c471bff41a70', '240ba872-6f88-457b-9913-f3bee66a04c8', 'a9be22689088d77fc5654071030515455f15972232c7f23f3ccf88cac719d419', 'offline', '2026-02-09 00:37:35', '2026-03-12 00:37:35', '192.168.1.156', '1.0.0') ON CONFLICT DO NOTHING;
INSERT INTO agents (id, machine_id, secret_hash, status, enrolled_at, last_seen, ip_address, agent_version) VALUES
  ('877b2fbd-cc84-441c-94c3-588e4bf2425e', '72bbf13b-a092-43fa-8604-4ad404d4637b', 'c955bc4980b4060de077c7cd96d258b2836949143357bccd2695550b6f817d13', 'online', '2026-02-02 00:37:35', '2026-03-12 00:37:35', '192.168.1.50', '1.0.0') ON CONFLICT DO NOTHING;
INSERT INTO agents (id, machine_id, secret_hash, status, enrolled_at, last_seen, ip_address, agent_version) VALUES
  ('1b9bad27-24c2-4511-8abc-c96ebbc4688f', 'fdcfe20f-f55c-4e21-ad33-2484fd43d426', '717b311a6c2565da50a461c8b4bcc84f00cfb9c7fe92023460a5348cd44dce8e', 'offline', '2026-01-30 00:37:35', '2026-03-12 00:37:35', '192.168.1.197', '1.0.0') ON CONFLICT DO NOTHING;
INSERT INTO agents (id, machine_id, secret_hash, status, enrolled_at, last_seen, ip_address, agent_version) VALUES
  ('bd76fcfb-4149-46e4-baea-610eef1e2f5b', '6a07ba4a-9b24-49ca-8861-d67c837ecddf', 'ecadc7fde3ffa2245b30d5fc8038ea906203d24a2c133b6ba04a4c0a39770bc5', 'offline', '2026-02-09 00:37:35', '2026-03-12 00:37:35', '192.168.1.116', '1.0.0') ON CONFLICT DO NOTHING;

-- Groups ---------------------------------------------------
INSERT INTO "groups" (id, name, description, ldap_dn) VALUES
  ('8302204a-4a01-4a97-9d64-85c3c71afa18', 'webapps', 'Serveurs web en prod', 'cn=webapps,ou=Groups,dc=linuxad,dc=local') ON CONFLICT DO NOTHING;
INSERT INTO "groups" (id, name, description, ldap_dn) VALUES
  ('1e9e64d7-4454-4711-92ee-ae6389be1a7f', 'database-servers', 'Serveurs de bdd', 'cn=database-servers,ou=Groups,dc=linuxad,dc=local') ON CONFLICT DO NOTHING;
INSERT INTO "groups" (id, name, description, ldap_dn) VALUES
  ('bcf39438-ca02-45db-9911-e1486aef9bbb', 'production', 'Toutes les machines de prod', 'cn=production,ou=Groups,dc=linuxad,dc=local') ON CONFLICT DO NOTHING;
INSERT INTO "groups" (id, name, description, ldap_dn) VALUES
  ('48ad4abf-3b38-47a0-a0f5-c523a57922ce', 'monitoring', 'Machines de monitoring', 'cn=monitoring,ou=Groups,dc=linuxad,dc=local') ON CONFLICT DO NOTHING;

-- Users LDAP ---------------------------------------------------
INSERT INTO users (uid, ldap_dn, cn, email, uid_number, gid_number, home_directory, created_by) VALUES
  ('jdoe', 'uid=jdoe,ou=People,dc=linuxad,dc=local', 'John Doe', 'jdoe@linuxad.local', 10001, 10001, '/home/jdoe', 'a591ff7e-f51c-4b0b-ae4d-a20204ccaeab') ON CONFLICT DO NOTHING;
INSERT INTO users (uid, ldap_dn, cn, email, uid_number, gid_number, home_directory, created_by) VALUES
  ('asmith', 'uid=asmith,ou=People,dc=linuxad,dc=local', 'Alice Smith', 'asmith@linuxad.local', 10002, 10002, '/home/asmith', 'a591ff7e-f51c-4b0b-ae4d-a20204ccaeab') ON CONFLICT DO NOTHING;
INSERT INTO users (uid, ldap_dn, cn, email, uid_number, gid_number, home_directory, created_by) VALUES
  ('bmartin', 'uid=bmartin,ou=People,dc=linuxad,dc=local', 'Bob Martin', 'bmartin@linuxad.local', 10003, 10003, '/home/bmartin', 'a591ff7e-f51c-4b0b-ae4d-a20204ccaeab') ON CONFLICT DO NOTHING;

-- GPO --------------------------------------------------
INSERT INTO gpo (id, name, description, version, status, content, signature, created_at, updated_at) VALUES
  ('9329b00c-0733-41e4-8c8e-5b7589c6e411', 'security_base', 'Configuration de securite', 4, 'active', '{"schema_version": "1.0", "policies": []}', '3b712f62c201287fe9868bf2904cb16e0a7ef1daf5b606cc98d88d4d0fc63784', '2026-02-27 00:37:35', '2026-03-12 00:37:35') ON CONFLICT DO NOTHING;
INSERT INTO gpo (id, name, description, version, status, content, signature, created_at, updated_at) VALUES
  ('56be2d9b-56bd-45f1-9dd8-828688276a09', 'ssh-hardening', 'Durcissement SSH', 2, 'active', '{"schema_version": "1.0", "policies": []}', '63c64919f7a9738024cb499265c5e5097bb7816acbb9f0e988cf677c0e86510d', '2026-03-03 00:37:35', '2026-03-09 00:37:35') ON CONFLICT DO NOTHING;
INSERT INTO gpo (id, name, description, version, status, content, signature, created_at, updated_at) VALUES
  ('d71bd46c-feca-4584-985d-9034fd7cccf2', 'monitoring-conf', 'Configuration monitoring', 1, 'draft', '{"schema_version": "1.0", "policies": []}', 'd300a8807833e15bf22a45e313d3f8fd97fca248f65d5b6e7bd0180f34163275', '2026-02-28 00:37:35', '2026-03-08 00:37:35') ON CONFLICT DO NOTHING;
INSERT INTO gpo (id, name, description, version, status, content, signature, created_at, updated_at) VALUES
  ('1235bd28-f8db-455f-ad75-de616a4e44cf', 'policy', 'politique', 3, 'archived', '{"schema_version": "1.0", "policies": []}', '71c06ee1a48cfe649a301a45bebd78a62ceee8418cbf0462665b54ff3549333d', '2026-03-11 00:37:35', '2026-03-08 00:37:35') ON CONFLICT DO NOTHING;

-- GPO Assignments ---------------------------------------------------
INSERT INTO gpo_assignments (id, gpo_id, target_type, priority, enabled) VALUES
  ('902fde6d-53fd-4996-8e0f-2a1d93789e12', '9329b00c-0733-41e4-8c8e-5b7589c6e411', 'all', 100, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO gpo_assignments (id, gpo_id, target_type, priority, enabled) VALUES
  ('5884895b-843d-47eb-9b34-1d1285b2c34d', '56be2d9b-56bd-45f1-9dd8-828688276a09', 'all', 100, TRUE) ON CONFLICT DO NOTHING;

-- Audit Logs ---------------------------------------------------
INSERT INTO audit_logs (id, actor_type, actor_id, action, resource_type, ip_address, timestamp) VALUES
  ('1de26465-f54e-49e1-ae4c-bf80301f9596', 'admin', 'a591ff7e-f51c-4b0b-ae4d-a20204ccaeab', 'delete', 'gpo', '10.0.0.4', '2026-03-06 00:37:35') ON CONFLICT DO NOTHING;
INSERT INTO audit_logs (id, actor_type, actor_id, action, resource_type, ip_address, timestamp) VALUES
  ('62ac434f-0bd9-4346-8ac7-3d61cf93da49', 'admin', 'a591ff7e-f51c-4b0b-ae4d-a20204ccaeab', 'delete', 'group', '10.0.0.7', '2026-03-12 00:37:35') ON CONFLICT DO NOTHING;
INSERT INTO audit_logs (id, actor_type, actor_id, action, resource_type, ip_address, timestamp) VALUES
  ('ca3a4d46-509d-4725-bf75-cceb1dcc1b47', 'admin', 'a591ff7e-f51c-4b0b-ae4d-a20204ccaeab', 'update', 'group', '10.0.0.2', '2026-03-08 00:37:35') ON CONFLICT DO NOTHING;
INSERT INTO audit_logs (id, actor_type, actor_id, action, resource_type, ip_address, timestamp) VALUES
  ('e84174a6-4ca3-4379-9ef5-a3dca50f6f79', 'admin', 'a591ff7e-f51c-4b0b-ae4d-a20204ccaeab', 'delete', 'gpo', '10.0.0.6', '2026-03-08 00:37:35') ON CONFLICT DO NOTHING;
INSERT INTO audit_logs (id, actor_type, actor_id, action, resource_type, ip_address, timestamp) VALUES
  ('9173a1a3-9f80-4e45-9dae-ac6d1ba2822b', 'admin', 'a591ff7e-f51c-4b0b-ae4d-a20204ccaeab', 'login', 'machine', '10.0.0.2', '2026-03-09 00:37:35') ON CONFLICT DO NOTHING;
INSERT INTO audit_logs (id, actor_type, actor_id, action, resource_type, ip_address, timestamp) VALUES
  ('108771ea-2d0b-4fe5-a897-f96cf15f7991', 'admin', 'a591ff7e-f51c-4b0b-ae4d-a20204ccaeab', 'login', 'machine', '10.0.0.5', '2026-03-05 00:37:35') ON CONFLICT DO NOTHING;
INSERT INTO audit_logs (id, actor_type, actor_id, action, resource_type, ip_address, timestamp) VALUES
  ('f614f9d3-e946-48cb-8354-53191bf74cb9', 'admin', 'a591ff7e-f51c-4b0b-ae4d-a20204ccaeab', 'create', 'machine', '10.0.0.6', '2026-03-08 00:37:35') ON CONFLICT DO NOTHING;
INSERT INTO audit_logs (id, actor_type, actor_id, action, resource_type, ip_address, timestamp) VALUES
  ('496b1079-5c30-44c4-894b-60d21fe2f7d9', 'admin', 'a591ff7e-f51c-4b0b-ae4d-a20204ccaeab', 'login', 'group', '10.0.0.2', '2026-03-05 00:37:35') ON CONFLICT DO NOTHING;
INSERT INTO audit_logs (id, actor_type, actor_id, action, resource_type, ip_address, timestamp) VALUES
  ('8c96505f-2004-456b-9ce4-eed8d8c5bd91', 'admin', 'a591ff7e-f51c-4b0b-ae4d-a20204ccaeab', 'create', 'user', '10.0.0.10', '2026-03-08 00:37:35') ON CONFLICT DO NOTHING;
INSERT INTO audit_logs (id, actor_type, actor_id, action, resource_type, ip_address, timestamp) VALUES
  ('0ab2fb52-dc1e-44fb-9dda-0d33c2c4954e', 'admin', 'a591ff7e-f51c-4b0b-ae4d-a20204ccaeab', 'login', 'gpo', '10.0.0.10', '2026-03-10 00:37:35') ON CONFLICT DO NOTHING;

-- Agent Logs ---------------------------------------------------
INSERT INTO agent_logs (id, agent_id, timestamp, level, category, message) VALUES
  ('e5d30ea4-7743-4c36-9478-86dd44d20d33', (SELECT id FROM agents WHERE machine_id = '50bd5cb9-e796-4f3a-9973-e90fd282bc6f' LIMIT 1), '2026-03-09 00:37:35', 'warning', 'system', 'Test log entry 1 for webapp-01') ON CONFLICT DO NOTHING;
INSERT INTO agent_logs (id, agent_id, timestamp, level, category, message) VALUES
  ('cf52147e-87d8-429e-a480-206ffa1ab64e', (SELECT id FROM agents WHERE machine_id = '50bd5cb9-e796-4f3a-9973-e90fd282bc6f' LIMIT 1), '2026-03-11 00:37:35', 'warning', 'gpo', 'Test log entry 2 for webapp-01') ON CONFLICT DO NOTHING;
INSERT INTO agent_logs (id, agent_id, timestamp, level, category, message) VALUES
  ('1362b262-9b9f-44e5-94da-90aefa3dd138', (SELECT id FROM agents WHERE machine_id = '50bd5cb9-e796-4f3a-9973-e90fd282bc6f' LIMIT 1), '2026-03-09 00:37:35', 'warning', 'gpo', 'Test log entry 3 for webapp-01') ON CONFLICT DO NOTHING;
INSERT INTO agent_logs (id, agent_id, timestamp, level, category, message) VALUES
  ('2561cb3f-9d7f-418e-bd64-2787cbec07f3', (SELECT id FROM agents WHERE machine_id = '240ba872-6f88-457b-9913-f3bee66a04c8' LIMIT 1), '2026-03-09 00:37:35', 'error', 'security', 'Test log entry 1 for webapp-02') ON CONFLICT DO NOTHING;
INSERT INTO agent_logs (id, agent_id, timestamp, level, category, message) VALUES
  ('63902630-9806-4a9e-a04c-dfbe572f0375', (SELECT id FROM agents WHERE machine_id = '240ba872-6f88-457b-9913-f3bee66a04c8' LIMIT 1), '2026-03-11 00:37:35', 'info', 'security', 'Test log entry 2 for webapp-02') ON CONFLICT DO NOTHING;
INSERT INTO agent_logs (id, agent_id, timestamp, level, category, message) VALUES
  ('1ccf0e46-affc-4a7d-9565-44e108f03731', (SELECT id FROM agents WHERE machine_id = '240ba872-6f88-457b-9913-f3bee66a04c8' LIMIT 1), '2026-03-11 00:37:35', 'info', 'system', 'Test log entry 3 for webapp-02') ON CONFLICT DO NOTHING;
INSERT INTO agent_logs (id, agent_id, timestamp, level, category, message) VALUES
  ('28b72caf-2c48-40de-b8bc-c71e4d0b0539', (SELECT id FROM agents WHERE machine_id = '72bbf13b-a092-43fa-8604-4ad404d4637b' LIMIT 1), '2026-03-10 00:37:35', 'info', 'system', 'Test log entry 1 for db-master') ON CONFLICT DO NOTHING;
INSERT INTO agent_logs (id, agent_id, timestamp, level, category, message) VALUES
  ('6c89884d-36ab-481a-ba2a-1c83d195718a', (SELECT id FROM agents WHERE machine_id = '72bbf13b-a092-43fa-8604-4ad404d4637b' LIMIT 1), '2026-03-10 00:37:35', 'info', 'gpo', 'Test log entry 2 for db-master') ON CONFLICT DO NOTHING;
INSERT INTO agent_logs (id, agent_id, timestamp, level, category, message) VALUES
  ('77db2d0f-33ae-4589-b793-9d19579c8cd6', (SELECT id FROM agents WHERE machine_id = '72bbf13b-a092-43fa-8604-4ad404d4637b' LIMIT 1), '2026-03-09 00:37:35', 'info', 'system', 'Test log entry 3 for db-master') ON CONFLICT DO NOTHING;

-- Enrollment Tokens ---------------------------------------------------
INSERT INTO enrollment_tokens (id, token_hash, description, max_uses, current_uses, expires_at, status, created_by) VALUES
  ('0642287d-4d65-412e-afab-195eac1a41af', 'ae5427ca3ceb2dc7ba7b2b23f28164e7ad7a3cbc7125aa8899aa2b3fa7aded7e', 'Token de test 1', 10, 3, '2026-03-13 00:37:35', 'active', 'a591ff7e-f51c-4b0b-ae4d-a20204ccaeab') ON CONFLICT DO NOTHING;
INSERT INTO enrollment_tokens (id, token_hash, description, max_uses, current_uses, expires_at, status, created_by) VALUES
  ('c23184c0-d1ac-4fa1-942c-48e34d0611b9', 'ccee1a67bb5b1c0b2cc95e39dfa8ed366388a3664558f408e0a606569337251d', 'Token de test 2', 10, 0, '2026-03-13 00:37:35', 'active', 'a591ff7e-f51c-4b0b-ae4d-a20204ccaeab') ON CONFLICT DO NOTHING;
INSERT INTO enrollment_tokens (id, token_hash, description, max_uses, current_uses, expires_at, status, created_by) VALUES
  ('8189017d-2550-43ef-bf7a-65800b8d3a24', '403d2b0f6874f04d0b86da34a1ea338c811bfa6a5529b37d4d73ef09c544f81e', 'Token de test 3', 10, 0, '2026-03-13 00:37:35', 'active', 'a591ff7e-f51c-4b0b-ae4d-a20204ccaeab') ON CONFLICT DO NOTHING;