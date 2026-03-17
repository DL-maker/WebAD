import type { LayoutServerLoad } from './$types';
import { redirect } from '@sveltejs/kit';

const PUBLIC_ROUTES = ['/auth/login', '/auth/logout'];

export const load: LayoutServerLoad = async ({ cookies, url }) => {
    const path  = url.pathname;
    const token = cookies.get('access_token');

    if (PUBLIC_ROUTES.some(r => path.startsWith(r))) {
        return {};
    }

    if (!token) {
        throw redirect(302, '/auth/login');
    }

    return {
        user: {
            username: cookies.get('username') ?? 'admin',
            role:     cookies.get('user_role') ?? 'viewer',
            token
        }
    };
};