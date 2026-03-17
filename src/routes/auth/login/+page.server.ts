// src/routes/auth/login/+page.server.ts
import type { Actions, PageServerLoad } from './$types';
import { fail, redirect } from '@sveltejs/kit';

const API = 'http://127.0.0.1:4444';

// Redirige vers / si déjà connecté
export const load: PageServerLoad = async ({ cookies }) => {
    const token = cookies.get('access_token');
    if (token) throw redirect(302, '/');
    return {};
};

export const actions: Actions = {
    default: async ({ request, cookies }) => {
        const form     = await request.formData();
        const username = form.get('username')?.toString().trim() ?? '';
        const password = form.get('password')?.toString() ?? '';
        const mfa_code = form.get('mfa_code')?.toString() ?? undefined;

        if (!username || !password) {
            return fail(400, { error: 'Champs manquants', username });
        }

        let res: Response;
        try {
            res = await fetch(`${API}/api/v1/admin/auth/login`, {
                method:  'POST',
                headers: { 'Content-Type': 'application/json' },
                body:    JSON.stringify({ username, password, mfa_code })
            });
        } catch {
            return fail(503, { error: 'API non disponible', username });
        }

        const data = await res.json();

        if (res.status === 401) {
            const code = data.error?.code ?? 'INVALID_CREDENTIALS';
            return fail(401, { error: code, username, mfa_required: code === 'MFA_REQUIRED' });
        }
        if (res.status === 429) {
            return fail(429, { error: 'RATE_LIMITED', username });
        }
        if (!res.ok) {
            return fail(500, { error: 'Erreur serveur', username });
        }

        cookies.set('access_token',  data.access_token,  { path: '/', httpOnly: true, maxAge: data.expires_in });
        cookies.set('refresh_token', data.refresh_token, { path: '/', httpOnly: true, maxAge: 60 * 60 * 24 * 7 });
        cookies.set('user_role',     data.user.role,     { path: '/', httpOnly: true, maxAge: data.expires_in });
        cookies.set('username',      data.user.username, { path: '/', httpOnly: true, maxAge: data.expires_in });

        throw redirect(302, '/');
    }
};