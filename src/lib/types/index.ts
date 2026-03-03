// ── Pagination ──
export interface Pagination {
    page: number;
    per_page: number;
    total: number;
    total_pages: number;
    has_next: boolean;
    has_prev: boolean;
}
export interface PaginatedResponse<T> {
    data: T[];
    pagination: Pagination;
}

// ── Machines ──
export interface MachineSummary {
    id: string;
    hostname: string;
    fqdn: string;
    description: string | null;
    os_version: string;
    kernel_version: string;
    status: 'pending' | 'active' | 'inactive' | 'revoked';
    agent_status: 'online' | 'offline' | 'error' | 'updating';
    agent_version: string;
    ip_address: string;
    groups: string[];
    enrolled_at: string;
    last_contact: string;
    gpo_compliance: {
        total: number;
        applied: number;
        pending: number;
        failed: number;
    };
}

export interface MachineDetail {
    id: string;
    hostname: string;
    fqdn: string;
    description: string | null;
    os_version: string;
    kernel_version: string;
    status: 'pending' | 'active' | 'inactive' | 'revoked';
    enrolled_at: string;
    last_contact: string;
    agent: {
        id: string;
        status: string;
        version: string;
        ip_address: string;
        last_seen: string;
        kernel_module_loaded: boolean;
    };
    groups: { 
        id: string; name: string }[];
        system_status: {
        uptime_seconds: number;
        cpu_usage_percent: number;
        memory_usage_percent: number;
        disk_usage_percent: number;
        load_average: [number, number, number];
    };
    gpo_status: GpoMachineStatus[];
    network_info: NetworkInfo;
    created_at: string;
    updated_at: string;
}

// ── Utilisateurs LDAP ──
export interface UserSummary {
    uid: string;
    cn: string;
    sn: string;
    given_name: string | null;
    email: string;
    uid_number: number;
    gid_number: number;
    home_directory: string;
    login_shell: string;
    groups: string[];
    created_at: string;
    last_password_change: string | null;
}

// ── Groupes ──
export interface GroupSummary {
    id: string;
    name: string;
    description: string | null;
    ldap_dn: string;
    machine_count: number;
    gpo_count: number;
    created_at: string;
}

export interface GpoSummary {
    id: string;
    name: string;
    description: string | null;
    version: number;
    status: 'draft' | 'active' | 'archived' | 'revoked';
    tags: string[];
    policies_count: number;
    assignments_count: number;
    machines_targeted: number;
    compliance: {
        success: number;
        pending: number;
        failed: number;
    };
    signed_at: string | null;
    signed_by: string | null;
    created_at: string;
    updated_at: string;
}

// ── Dashboard Stats ──
export interface DashboardStats {
    machines: { total: number; active: number; inactive: number; pending:number; revoked: number };
    agents: { online: number; offline: number; error: number; updating:number };
    users: { total: number };
    groups: { total: number };
    gpo: { total: number; active: number; draft: number; archived: number };
    compliance: {
        fully_compliant_machines: number;
        partially_compliant: number;
        non_compliant: number;
        compliance_rate_percent: number;
    };
recent_activity: { type: string; message: string; timestamp: string }[];
generated_at: string;
}

// ── Admin Users ──
export interface AdminUser {
    id: string;
    username: string;
    email: string;
    role: 'superadmin' | 'admin' | 'operator' | 'viewer';
    mfa_enabled: boolean;
    last_login: string | null;
    created_at: string;
}

// ── Logs ──
export interface AgentLog {
    id: string;
    agent_id: string;
    machine_id: string;
    hostname: string;
    timestamp: string;
    level: 'debug' | 'info' | 'warning' | 'error' | 'critical';
    category: string;
    message: string;
    details: Record<string, unknown> | null;
    received_at: string;
}

export interface AuditLog {
    id: string;
    actor_type: 'admin' | 'agent' | 'system';
    actor_id: string;
    actor_username: string;
    timestamp: string;
    action: string;
    resource_type: string;
    resource_id: string;
    resource_name: string;
    details: Record<string, unknown> | null;
    ip_address: string;
}

export interface NetworkInfo {
    primary_ip: string;
    mac_address: string;
    interfaces: {
    name: string;
        ip: string;
        mac: string;
    }[];
}

export interface GpoMachineStatus {
    gpo_id: string;
    gpo_name: string;
    version_applied: number;
    version_latest: number;
    status: 'success' | 'pending' | 'failed' | 'rolled_back';
    applied_at: string | null;
}

export interface GpoPolicy {
    id: string;
    name: string;
    type: string;
    enabled: boolean;
    priority: number;
    config: Record<string, unknown>;
    triggers?: { event: string; action: string; target: string }[];
    validation?: { command: string; expected_exit_code: number };
}

export interface GpoDetail extends GpoSummary {
    schema_version: string;
    content: {
        policies: GpoPolicy[];
    };
    metadata: {
        author: string;
        tags: string[];
    };
    targeting: {
        mode: 'include' | 'exclude' | 'all';
        groups: string[];
        machines: string[];
        os_filter?: {
            distribution?: string;
            version_min?: string;
        };
    };
    signature: string | null;
    assignments: {
        target_type: 'machine' | 'group' | 'all';
        target_name: string;
        priority: number;
        enabled: boolean;
    }[];
    deployment_status: {
        total_targeted: number;
        success: number;
        pending: number;
        failed: number;
        machines: {
            machine_id: string;
            hostname: string;
            status: string;
            applied_at: string | null;
            }[];
        };
        version_history: {
            version: number;
            updated_at: string;
            updated_by: string;
        }[];
        rollback: {
            enabled: boolean;
            automatic_on_failure: boolean;
            keep_backups: number;
        };
}

export interface Settings {
    general: {
        domain: string;
        organization: string;
    };
    agent: {
        default_poll_interval: number;
        max_poll_interval: number;
        secret_rotation_days: number;
        log_batch_size: number;
    };
    security: {
        jwt_expiration_seconds: number;
        mfa_enabled: boolean;
        password_min_length: number;
        max_login_attempts: number;
        lockout_duration_minutes: number;
    };
    ldap: {
        base_dn: string;
        uid_start: number;
        gid_start: number;
    };
    logs: {
        retention_audit_days: number;
        retention_security_days: number;
        retention_gpo_days: number;
        retention_system_days: number;
        retention_debug_days: number;
    };
}