// src/routes/+page.server.ts
import type { PageServerLoad } from './$types';
import { redirect } from '@sveltejs/kit';
import type { DashboardStats } from '$lib/types';

const API = 'http://127.0.0.1:4444';

export const load: PageServerLoad = async ({ cookies }) => {
    const token = cookies.get('access_token');
    if (!token) throw redirect(302, '/auth/login');

    try {
        const res = await fetch(`${API}/api/v1/admin/dashboard/stats`, {
            headers: { Authorization: `Bearer ${token}` }
        });

        if (!res.ok) throw new Error('API error');

        const stats: DashboardStats = await res.json();
        return { stats };

    } catch {
        // Relay indisponible → valeurs vides
        return {
            stats: {
                machines:        { total: 0, active: 0, inactive: 0, pending: 0, revoked: 0 },
                agents:          { online: 0, offline: 0, error: 0, updating: 0 },
                users:           { total: 0 },
                groups:          { total: 0 },
                gpo:             { total: 0, active: 0, draft: 0, archived: 0 },
                compliance:      { fully_compliant_machines: 0, partially_compliant: 0, non_compliant: 0, compliance_rate_percent: 0 },
                recent_activity: [],
                generated_at:    new Date().toISOString()
            } satisfies DashboardStats
        };
    }
};