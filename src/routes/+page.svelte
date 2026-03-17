<!-- svelte-ignore state_referenced_locally -->
<!-- svelte-ignore state_referenced_locally -->
<!-- src/routes/+page.svelte -->
<!-- Dashboard principal -->
<script lang="ts">
    import type { PageProps } from './$types';
    let { data }: PageProps = $props();
    let stats = $derived(data.stats);
</script>

<h1>Dashboard</h1>

<section>
    <h2>Machines</h2>
    <table border="1" cellpadding="4">
        <thead>
            <tr>
                <th>Total</th>
                <th>Active</th>
                <th>Inactive</th>
                <th>Pending</th>
                <th>Revoked</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>{stats.machines.total}</td>
                <td>{stats.machines.active}</td>
                <td>{stats.machines.inactive}</td>
                <td>{stats.machines.pending}</td>
                <td>{stats.machines.revoked}</td>
            </tr>
        </tbody>
    </table>
</section>

<section>
    <h2>Agents</h2>
    <table border="1" cellpadding="4">
        <thead>
            <tr>
                <th>Online</th>
                <th>Offline</th>
                <th>Error</th>
                <th>Updating</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>{stats.agents.online}</td>
                <td>{stats.agents.offline}</td>
                <td>{stats.agents.error}</td>
                <td>{stats.agents.updating}</td>
            </tr>
        </tbody>
    </table>
</section>

<section>
    <h2>Résumé</h2>
    <table border="1" cellpadding="4">
        <thead>
            <tr>
                <th>Users LDAP</th>
                <th>Groupes</th>
                <th>GPO total</th>
                <th>GPO actives</th>
                <th>GPO draft</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>{stats.users.total}</td>
                <td>{stats.groups.total}</td>
                <td>{stats.gpo.total}</td>
                <td>{stats.gpo.active}</td>
                <td>{stats.gpo.draft}</td>
            </tr>
        </tbody>
    </table>
</section>

<section>
    <h2>Compliance</h2>
    <table border="1" cellpadding="4">
        <thead>
            <tr>
                <th>Conformes</th>
                <th>Partiels</th>
                <th>Non conformes</th>
                <th>Taux</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>{stats.compliance.fully_compliant_machines}</td>
                <td>{stats.compliance.partially_compliant}</td>
                <td>{stats.compliance.non_compliant}</td>
                <td>{stats.compliance.compliance_rate_percent}%</td>
            </tr>
        </tbody>
    </table>
</section>

<section>
    <h2>Activité récente</h2>
    {#if stats.recent_activity.length === 0}
        <p>Aucune activité récente.</p>
    {:else}
        <table border="1" cellpadding="4">
            <thead>
                <tr>
                    <th>Type</th>
                    <th>Message</th>
                    <th>Timestamp</th>
                </tr>
            </thead>
            <tbody>
                {#each stats.recent_activity as activity}
                    <tr>
                        <td>{activity.type}</td>
                        <td>{activity.message}</td>
                        <td>{activity.timestamp}</td>
                    </tr>
                {/each}
            </tbody>
        </table>
    {/if}
</section>

<p>
    Généré le {stats.generated_at}
</p>