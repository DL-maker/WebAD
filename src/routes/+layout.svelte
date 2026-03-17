<script lang="ts">
    import type { LayoutProps } from './$types';

    let { data, children }: LayoutProps = $props();
    let isAuthPage = $derived(!data.user);

    const navLinks = [
        { href: '/',          label: 'Dashboard' },
        { href: '/machines',  label: 'Machines'  },
        { href: '/users',     label: 'Users'     },
        { href: '/groups',    label: 'Groups'    },
        { href: '/gpo',       label: 'GPO'       },
        { href: '/logs',      label: 'Logs'      },
        { href: '/settings',  label: 'Settings'  },
    ];
</script>

{#if isAuthPage}
    <!-- Pages auth : pas de sidebar -->
    {@render children()}
{:else}
    <!-- Layout avec sidebar -->
    <div>

        <!-- Sidebar -->
        <nav>
            <p><strong>LinuxAD</strong></p>
            <p>
                {data.user?.username} ({data.user?.role})
            </p>
            <hr />
            <ul>
                {#each navLinks as link}
                    <li>
                        <a href={link.href}>{link.label}</a>
                    </li>
                {/each}
            </ul>
            <hr />
            <a href="/auth/logout">Déconnexion</a>
        </nav>

        <!-- Contenu principal -->
        <main>
            {@render children()}
        </main>

    </div>
{/if}