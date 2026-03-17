<!-- src/routes/auth/login/+page.svelte -->
<script lang="ts">
    import type { PageProps } from './$types';

    let { form }: PageProps = $props();
    let showMfa = $derived(form?.mfa_required === true);
</script>

<h1>LinuxAD — Login</h1>

<form method="POST">
    <div>
        <label for="username">Username</label>
        <input
            id="username"
            name="username"
            type="text"
            value={form?.username ?? ''}
            required
            autocomplete="username"
        />
    </div>

    <div>
        <label for="password">Password</label>
        <input
            id="password"
            name="password"
            type="password"
            required
            autocomplete="current-password"
        />
    </div>

    {#if showMfa}
        <div>
            <label for="mfa_code">Code MFA (6 chiffres)</label>
            <input
                id="mfa_code"
                name="mfa_code"
                type="text"
                inputmode="numeric"
                maxlength="6"
                placeholder="123456"
            />
        </div>
    {/if}

    {#if form?.error}
        <p>
            {#if form.error === 'INVALID_CREDENTIALS'}
                Identifiants incorrects.
            {:else if form.error === 'MFA_REQUIRED'}
                Code MFA requis.
            {:else if form.error === 'INVALID_MFA'}
                Code MFA invalide.
            {:else if form.error === 'RATE_LIMITED'}
                Trop de tentatives. Réessayez dans 1 minute.
            {:else if form.error === 'API non disponible'}
                Le serveur est inaccessible. Vérifiez que relay.py tourne.
            {:else}
                Erreur : {form.error}
            {/if}
        </p>
    {/if}

    <button type="submit">Se connecter</button>
</form>