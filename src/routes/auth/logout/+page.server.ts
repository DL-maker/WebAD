import type { PageServerLoad } from './$types';
import { redirect } from '@sveltejs/kit';

const API = 'http://127.0.0.1:4444';

export const load: PageServerLoad = async ({ cookies, fetch }) => {
    const refresh_token = cookies.get('refresh_token');

    if (refresh_token) {
        try {
            await fetch(`${API}/api/v1/admin/auth/logout`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ refresh_token })
            });
        } catch {
            return
        }
    }

    cookies.delete('access_token', { path: '/' });
    cookies.delete('refresh_token', { path: '/' });
    cookies.delete('user_role', { path: '/' });
    cookies.delete('username', { path: '/' });

    throw redirect(302, '/auth/login');
};