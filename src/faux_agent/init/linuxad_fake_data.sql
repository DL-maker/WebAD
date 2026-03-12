
-- Admin ---------------------------------------------------
INSERT INTO admin_users (id, username, email, password_hash, role, mfa_enabled, created_at) VALUES
  ('26025715-d000-4497-88a7-cd58f1ea8202', 'admin', 'admin@linuxad.local', '5ce41ada64f1e8ffb0acfaafa622b141438f3a5777785e7f0b830fb73e40d3d6', 'superadmin', FALSE, '2026-02-04 01:02:50') ON CONFLICT DO NOTHING;
INSERT INTO admin_users (id, username, email, password_hash, role, mfa_enabled, created_at) VALUES
  ('1930827e-b633-4d24-9550-1c12f4262ee4', 'h', 'sysadmin@linuxad.local', 'a685113620c42ad011a5d91dffeb171f1c7d0923552c068cd293ea983b72bc41', 'operator', TRUE, '2025-12-22 01:02:50') ON CONFLICT DO NOTHING;
INSERT INTO admin_users (id, username, email, password_hash, role, mfa_enabled, created_at) VALUES
  ('42cb1aab-24e8-4b4b-ad7f-bbc820bfb025', 'k', 'k@linuxad.local', '5fb442343eda6d210090f101117e7e08a3474c05ce924dd2aa1976183da38c09', 'viewer', FALSE, '2026-02-04 01:02:50') ON CONFLICT DO NOTHING;
INSERT INTO admin_users (id, username, email, password_hash, role, mfa_enabled, created_at) VALUES
  ('d433c388-9d9a-4cf9-8915-37701a1ecb99', 't', 't@linuxad.local', '110812f67fa1e1f0117f6f3d70241c1a42a7b07711a93c2477cc516d9042f9db', 'admin', TRUE, '2025-12-26 01:02:50') ON CONFLICT DO NOTHING;
INSERT INTO admin_users (id, username, email, password_hash, role, mfa_enabled, created_at) VALUES
  ('41cf93b7-b2c9-4a8d-83a6-1a8b288b549c', 'o', 'o@linuxad.local', '5b3975651c3cab92d044c096dc30a1c2d9525497457472de48c51ecb363d1f4a', 'operator', FALSE, '2026-02-25 01:02:50') ON CONFLICT DO NOTHING;

-- Machines ---------------------------------------------------
INSERT INTO machines (id, hostname, fqdn, os_version, kernel_version, status, enrolled_at, last_contact) VALUES
  ('cd9e13d9-89c0-4414-86cb-3d3cc31c7cc5', 'webapp-01', 'webapp-01.linuxad.local', 'Debian 13', '6.12.38', 'active', '2026-01-12 01:02:50', '2026-03-12 01:02:50') ON CONFLICT DO NOTHING;
INSERT INTO machines (id, hostname, fqdn, os_version, kernel_version, status, enrolled_at, last_contact) VALUES
  ('b9a0a733-c522-43eb-9b4f-e703d789edb9', 'webapp-02', 'webapp-02.linuxad.local', 'Debian 13', '6.12.38', 'rolled_back', '2026-02-06 01:02:50', '2026-03-12 01:02:50') ON CONFLICT DO NOTHING;
INSERT INTO machines (id, hostname, fqdn, os_version, kernel_version, status, enrolled_at, last_contact) VALUES
  ('6eac38b9-5970-4000-b577-253f52f4322d', 'db-master', 'db-master.linuxad.local', 'Alpine', '6.12.38', 'active', '2026-02-03 01:02:50', '2026-03-10 01:02:50') ON CONFLICT DO NOTHING;
INSERT INTO machines (id, hostname, fqdn, os_version, kernel_version, status, enrolled_at, last_contact) VALUES
  ('bd045dd1-c93c-43a4-9667-9c58531023fb', 'db-replica', 'db-replica.linuxad.local', 'FreeBSD', '13.0', 'inactive', '2026-01-24 01:02:50', '2026-03-12 01:02:50') ON CONFLICT DO NOTHING;
INSERT INTO machines (id, hostname, fqdn, os_version, kernel_version, status, enrolled_at, last_contact) VALUES
  ('2ec5371f-2ee0-44ff-a709-9abbe3f858a5', 'monitoring-01', 'monitoring-01.linuxad.local', 'Arch', '6.12.38', 'pending', '2026-01-11 01:02:50', '2026-03-10 01:02:50') ON CONFLICT DO NOTHING;

-- Agents ---------------------------------------------------
INSERT INTO agents (id, machine_id, secret_hash, status, enrolled_at, last_seen, ip_address, agent_version) VALUES
  ('6ccbeb42-efd3-436a-8258-b4cbb76c1e61', 'cd9e13d9-89c0-4414-86cb-3d3cc31c7cc5', '3503592b4d664f0da138eff1527d118b6f503c0506417549af09f55b45f29dd9', 'online', '2026-02-17 01:02:50', '2026-03-12 01:02:50', '192.168.1.104', '1.0.0') ON CONFLICT DO NOTHING;
INSERT INTO agents (id, machine_id, secret_hash, status, enrolled_at, last_seen, ip_address, agent_version) VALUES
  ('3f3680a4-90df-4d8b-8524-c479ba297b50', 'b9a0a733-c522-43eb-9b4f-e703d789edb9', 'a9be22689088d77fc5654071030515455f15972232c7f23f3ccf88cac719d419', 'offline', '2026-02-04 01:02:50', '2026-03-12 01:02:50', '192.168.1.23', '1.0.0') ON CONFLICT DO NOTHING;
INSERT INTO agents (id, machine_id, secret_hash, status, enrolled_at, last_seen, ip_address, agent_version) VALUES
  ('0a2e11f0-3c16-4a89-b2c7-977c338c9ebe', '6eac38b9-5970-4000-b577-253f52f4322d', 'c955bc4980b4060de077c7cd96d258b2836949143357bccd2695550b6f817d13', 'online', '2026-02-10 01:02:50', '2026-03-12 01:02:50', '192.168.1.95', '1.0.0') ON CONFLICT DO NOTHING;
INSERT INTO agents (id, machine_id, secret_hash, status, enrolled_at, last_seen, ip_address, agent_version) VALUES
  ('f5239831-2581-4776-acf2-4f3009c13d0b', 'bd045dd1-c93c-43a4-9667-9c58531023fb', '717b311a6c2565da50a461c8b4bcc84f00cfb9c7fe92023460a5348cd44dce8e', 'offline', '2026-01-28 01:02:50', '2026-03-11 01:02:50', '192.168.1.28', '1.0.0') ON CONFLICT DO NOTHING;
INSERT INTO agents (id, machine_id, secret_hash, status, enrolled_at, last_seen, ip_address, agent_version) VALUES
  ('223aae6f-d63e-401d-a2ba-9a3510c4c93b', '2ec5371f-2ee0-44ff-a709-9abbe3f858a5', 'ecadc7fde3ffa2245b30d5fc8038ea906203d24a2c133b6ba04a4c0a39770bc5', 'offline', '2026-01-13 01:02:50', '2026-03-11 01:02:50', '192.168.1.35', '1.0.0') ON CONFLICT DO NOTHING;

-- Groups ---------------------------------------------------
INSERT INTO "groups" (id, name, description, ldap_dn) VALUES
  ('6d9e7af2-aacb-4fd6-8381-b5a50915cb4d', 'webapps', 'Serveurs web en prod', 'cn=webapps,ou=Groups,dc=linuxad,dc=local') ON CONFLICT DO NOTHING;
INSERT INTO "groups" (id, name, description, ldap_dn) VALUES
  ('4ea89319-a897-4a41-a3c3-b975f271e225', 'database-servers', 'Serveurs de bdd', 'cn=database-servers,ou=Groups,dc=linuxad,dc=local') ON CONFLICT DO NOTHING;
INSERT INTO "groups" (id, name, description, ldap_dn) VALUES
  ('b062a88f-786f-4d46-b25d-1e45cc1f1f4a', 'production', 'Toutes les machines de prod', 'cn=production,ou=Groups,dc=linuxad,dc=local') ON CONFLICT DO NOTHING;
INSERT INTO "groups" (id, name, description, ldap_dn) VALUES
  ('ce87b0c9-e7fd-4494-ad9d-6e41d95f3ed8', 'monitoring', 'Machines de monitoring', 'cn=monitoring,ou=Groups,dc=linuxad,dc=local') ON CONFLICT DO NOTHING;

-- Users LDAP ---------------------------------------------------
INSERT INTO users (uid, ldap_dn, cn, email, uid_number, gid_number, home_directory, created_by) VALUES
  ('jdoe', 'uid=jdoe,ou=People,dc=linuxad,dc=local', 'John Doe', 'jdoe@linuxad.local', 10001, 10001, '/home/jdoe', '26025715-d000-4497-88a7-cd58f1ea8202') ON CONFLICT DO NOTHING;
INSERT INTO users (uid, ldap_dn, cn, email, uid_number, gid_number, home_directory, created_by) VALUES
  ('asmith', 'uid=asmith,ou=People,dc=linuxad,dc=local', 'Alice Smith', 'asmith@linuxad.local', 10002, 10002, '/home/asmith', '26025715-d000-4497-88a7-cd58f1ea8202') ON CONFLICT DO NOTHING;
INSERT INTO users (uid, ldap_dn, cn, email, uid_number, gid_number, home_directory, created_by) VALUES
  ('bmartin', 'uid=bmartin,ou=People,dc=linuxad,dc=local', 'Bob Martin', 'bmartin@linuxad.local', 10003, 10003, '/home/bmartin', '26025715-d000-4497-88a7-cd58f1ea8202') ON CONFLICT DO NOTHING;

-- GPO --------------------------------------------------
INSERT INTO gpo (id, name, description, version, status, content, signature, created_at, updated_at) VALUES
  ('9f3b2d7c-58d1-40f5-8a41-c4b1af88d6f9', 'security_base', 'Configuration de securite', 4, 'active', '{"schema_version": "1.0", "policies": []}', '3b712f62c201287fe9868bf2904cb16e0a7ef1daf5b606cc98d88d4d0fc63784', '2026-03-05 01:02:50', '2026-03-09 01:02:50') ON CONFLICT DO NOTHING;
INSERT INTO gpo (id, name, description, version, status, content, signature, created_at, updated_at) VALUES
  ('05a68c3f-8452-4aaa-b805-25a7b6c9849c', 'ssh-hardening', 'Durcissement SSH', 2, 'active', '{"schema_version": "1.0", "policies": []}', '63c64919f7a9738024cb499265c5e5097bb7816acbb9f0e988cf677c0e86510d', '2026-03-08 01:02:50', '2026-03-07 01:02:50') ON CONFLICT DO NOTHING;
INSERT INTO gpo (id, name, description, version, status, content, signature, created_at, updated_at) VALUES
  ('9fd10aaf-2015-427a-b3e2-e62ea296909d', 'monitoring-conf', 'Configuration monitoring', 1, 'draft', '{"schema_version": "1.0", "policies": []}', 'd300a8807833e15bf22a45e313d3f8fd97fca248f65d5b6e7bd0180f34163275', '2026-02-28 01:02:50', '2026-03-07 01:02:50') ON CONFLICT DO NOTHING;
INSERT INTO gpo (id, name, description, version, status, content, signature, created_at, updated_at) VALUES
  ('4ac9a659-af4b-4949-b7f5-e0d7a4097311', 'policy', 'politique', 3, 'archived', '{"schema_version": "1.0", "policies": []}', '71c06ee1a48cfe649a301a45bebd78a62ceee8418cbf0462665b54ff3549333d', '2026-02-16 01:02:50', '2026-03-07 01:02:50') ON CONFLICT DO NOTHING;

-- GPO Assignments ---------------------------------------------------
INSERT INTO gpo_assignments (id, gpo_id, target_type, priority, enabled) VALUES
  ('b95d5ae3-21d6-4f65-a639-886a67242baf', '9f3b2d7c-58d1-40f5-8a41-c4b1af88d6f9', 'all', 100, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO gpo_assignments (id, gpo_id, target_type, priority, enabled) VALUES
  ('1065ca50-fb5a-42f5-8180-0f28b2ac4a50', '05a68c3f-8452-4aaa-b805-25a7b6c9849c', 'all', 100, TRUE) ON CONFLICT DO NOTHING;

-- Audit Logs ---------------------------------------------------
INSERT INTO audit_logs (id, actor_type, actor_id, action, resource_type, ip_address, timestamp) VALUES
  ('d0bc0817-a14c-456d-8d0b-f16bbd9f58d9', 'admin', '26025715-d000-4497-88a7-cd58f1ea8202', 'update', 'user', '10.0.0.7', '2026-03-09 01:02:50') ON CONFLICT DO NOTHING;
INSERT INTO audit_logs (id, actor_type, actor_id, action, resource_type, ip_address, timestamp) VALUES
  ('56d9ed53-b246-4243-be27-202b3f7e077f', 'admin', '26025715-d000-4497-88a7-cd58f1ea8202', 'login', 'user', '10.0.0.4', '2026-03-08 01:02:50') ON CONFLICT DO NOTHING;
INSERT INTO audit_logs (id, actor_type, actor_id, action, resource_type, ip_address, timestamp) VALUES
  ('9c194743-21aa-48c7-bca1-f570a095bd4b', 'admin', '26025715-d000-4497-88a7-cd58f1ea8202', 'update', 'gpo', '10.0.0.2', '2026-03-08 01:02:50') ON CONFLICT DO NOTHING;
INSERT INTO audit_logs (id, actor_type, actor_id, action, resource_type, ip_address, timestamp) VALUES
  ('87139d70-e6c9-4c58-8298-488389e09da2', 'admin', '26025715-d000-4497-88a7-cd58f1ea8202', 'update', 'user', '10.0.0.2', '2026-03-08 01:02:50') ON CONFLICT DO NOTHING;
INSERT INTO audit_logs (id, actor_type, actor_id, action, resource_type, ip_address, timestamp) VALUES
  ('a3f205e9-4c73-49b9-9ccc-5df36342324b', 'admin', '26025715-d000-4497-88a7-cd58f1ea8202', 'create', 'group', '10.0.0.10', '2026-03-07 01:02:50') ON CONFLICT DO NOTHING;
INSERT INTO audit_logs (id, actor_type, actor_id, action, resource_type, ip_address, timestamp) VALUES
  ('86ab8afa-8abe-4980-adbf-d467b35ef242', 'admin', '26025715-d000-4497-88a7-cd58f1ea8202', 'login', 'group', '10.0.0.1', '2026-03-08 01:02:50') ON CONFLICT DO NOTHING;
INSERT INTO audit_logs (id, actor_type, actor_id, action, resource_type, ip_address, timestamp) VALUES
  ('f1d82ef0-d6cd-4da9-af21-c37230448ebb', 'admin', '26025715-d000-4497-88a7-cd58f1ea8202', 'enroll', 'user', '10.0.0.4', '2026-03-07 01:02:50') ON CONFLICT DO NOTHING;
INSERT INTO audit_logs (id, actor_type, actor_id, action, resource_type, ip_address, timestamp) VALUES
  ('80ac6dd9-6b9f-4abd-a20f-265494a209a2', 'admin', '26025715-d000-4497-88a7-cd58f1ea8202', 'enroll', 'group', '10.0.0.3', '2026-03-06 01:02:50') ON CONFLICT DO NOTHING;
INSERT INTO audit_logs (id, actor_type, actor_id, action, resource_type, ip_address, timestamp) VALUES
  ('c894f41a-52a6-4e7e-8f54-babdd5eab634', 'admin', '26025715-d000-4497-88a7-cd58f1ea8202', 'enroll', 'group', '10.0.0.3', '2026-03-11 01:02:50') ON CONFLICT DO NOTHING;
INSERT INTO audit_logs (id, actor_type, actor_id, action, resource_type, ip_address, timestamp) VALUES
  ('2d985c74-fd2d-475c-b68d-146bed080f9c', 'admin', '26025715-d000-4497-88a7-cd58f1ea8202', 'enroll', 'group', '10.0.0.3', '2026-03-11 01:02:50') ON CONFLICT DO NOTHING;

-- Agent Logs ---------------------------------------------------
INSERT INTO agent_logs (id, agent_id, timestamp, level, category, message) VALUES
  ('3c226cb8-f546-4166-a57c-b194aefb154c', (SELECT id FROM agents WHERE machine_id = 'cd9e13d9-89c0-4414-86cb-3d3cc31c7cc5' LIMIT 1), '2026-03-10 01:02:50', 'error', 'system', 'Test log entry 1 for webapp-01') ON CONFLICT DO NOTHING;
INSERT INTO agent_logs (id, agent_id, timestamp, level, category, message) VALUES
  ('e8ab8d27-f552-4b0f-ad7d-642d653d934c', (SELECT id FROM agents WHERE machine_id = 'cd9e13d9-89c0-4414-86cb-3d3cc31c7cc5' LIMIT 1), '2026-03-09 01:02:50', 'error', 'network', 'Test log entry 2 for webapp-01') ON CONFLICT DO NOTHING;
INSERT INTO agent_logs (id, agent_id, timestamp, level, category, message) VALUES
  ('e92423b3-5e3a-4625-b720-ea312552f818', (SELECT id FROM agents WHERE machine_id = 'cd9e13d9-89c0-4414-86cb-3d3cc31c7cc5' LIMIT 1), '2026-03-12 01:02:50', 'error', 'security', 'Test log entry 3 for webapp-01') ON CONFLICT DO NOTHING;
INSERT INTO agent_logs (id, agent_id, timestamp, level, category, message) VALUES
  ('b9262d29-9d91-4dd2-9941-432d28fbb124', (SELECT id FROM agents WHERE machine_id = 'b9a0a733-c522-43eb-9b4f-e703d789edb9' LIMIT 1), '2026-03-11 01:02:50', 'error', 'network', 'Test log entry 1 for webapp-02') ON CONFLICT DO NOTHING;
INSERT INTO agent_logs (id, agent_id, timestamp, level, category, message) VALUES
  ('1305f803-62ed-4546-92f7-f6b447ea541b', (SELECT id FROM agents WHERE machine_id = 'b9a0a733-c522-43eb-9b4f-e703d789edb9' LIMIT 1), '2026-03-10 01:02:50', 'error', 'gpo', 'Test log entry 2 for webapp-02') ON CONFLICT DO NOTHING;
INSERT INTO agent_logs (id, agent_id, timestamp, level, category, message) VALUES
  ('f3886406-7360-4f84-a488-6e36c39f6369', (SELECT id FROM agents WHERE machine_id = 'b9a0a733-c522-43eb-9b4f-e703d789edb9' LIMIT 1), '2026-03-09 01:02:50', 'warning', 'system', 'Test log entry 3 for webapp-02') ON CONFLICT DO NOTHING;
INSERT INTO agent_logs (id, agent_id, timestamp, level, category, message) VALUES
  ('2ee66796-b850-4346-838b-a003a1da8c02', (SELECT id FROM agents WHERE machine_id = '6eac38b9-5970-4000-b577-253f52f4322d' LIMIT 1), '2026-03-09 01:02:50', 'warning', 'network', 'Test log entry 1 for db-master') ON CONFLICT DO NOTHING;
INSERT INTO agent_logs (id, agent_id, timestamp, level, category, message) VALUES
  ('6cd83773-5129-4667-8350-f32e9decece1', (SELECT id FROM agents WHERE machine_id = '6eac38b9-5970-4000-b577-253f52f4322d' LIMIT 1), '2026-03-10 01:02:50', 'warning', 'gpo', 'Test log entry 2 for db-master') ON CONFLICT DO NOTHING;
INSERT INTO agent_logs (id, agent_id, timestamp, level, category, message) VALUES
  ('66a7d1dd-51b8-43e5-9561-79075a659a39', (SELECT id FROM agents WHERE machine_id = '6eac38b9-5970-4000-b577-253f52f4322d' LIMIT 1), '2026-03-10 01:02:50', 'error', 'security', 'Test log entry 3 for db-master') ON CONFLICT DO NOTHING;

-- Enrollment Tokens ---------------------------------------------------
INSERT INTO enrollment_tokens (id, token_hash, description, max_uses, current_uses, expires_at, status, created_by) VALUES
  ('6690d1a2-e8f5-4935-9ce7-830dd2de1418', 'ae5427ca3ceb2dc7ba7b2b23f28164e7ad7a3cbc7125aa8899aa2b3fa7aded7e', 'Token de test 1', 10, 1, '2026-03-13 01:02:50', 'active', '26025715-d000-4497-88a7-cd58f1ea8202') ON CONFLICT DO NOTHING;
INSERT INTO enrollment_tokens (id, token_hash, description, max_uses, current_uses, expires_at, status, created_by) VALUES
  ('5d6dd8ee-571c-460e-b06f-b20107b9d625', 'ccee1a67bb5b1c0b2cc95e39dfa8ed366388a3664558f408e0a606569337251d', 'Token de test 2', 10, 2, '2026-03-13 01:02:50', 'active', '26025715-d000-4497-88a7-cd58f1ea8202') ON CONFLICT DO NOTHING;
INSERT INTO enrollment_tokens (id, token_hash, description, max_uses, current_uses, expires_at, status, created_by) VALUES
  ('f37179dd-ff07-4b9a-9533-1dfa6dc8fb39', '403d2b0f6874f04d0b86da34a1ea338c811bfa6a5529b37d4d73ef09c544f81e', 'Token de test 3', 10, 2, '2026-03-13 01:02:50', 'active', '26025715-d000-4497-88a7-cd58f1ea8202') ON CONFLICT DO NOTHING;