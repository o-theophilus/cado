<script>
	import { user } from '$lib/store.svelte.js';

	import { Meta } from '$lib/macro';
	import { Button } from '$lib/button';
</script>

<Meta title="Admin Dashboard" description="This contains this website settings" />

<div class="page">
	<div class="page_title">Admin Dashboard</div>

	<div class="buttons">
		{#if user.value.access.includes('user:view')}
			<Button href="/admin/users">Users</Button>
		{/if}
		{#if user.value.access.includes('user:edit_access')}
			<Button href="/admin/admin_users">Admin Users</Button>
		{/if}
		{#if user.value.access.includes('admin:view_photo_error')}
			<Button href="/admin/photo_error">Photo Error</Button>
		{/if}
		{#if user.value.access.includes('organization:view')}
			<Button href="/organization">Organizations</Button>
		{/if}
		{#if user.value.organization_key && user.value.access.some( (x) => ['organization:edit_logo', 'organization:edit_icon', 'organization:edit_organization', 'organization:edit_contact', 'organization:edit_social_media', 'organization:delete'].includes(x) )}
			<Button href="/admin/org/{user.value.organization_key}">Organization Setting</Button>
		{/if}
	</div>
</div>

<style>
	.page {
		max-width: var(--mobileWidth);
		width: 100%;
		margin: auto;
		padding: var(--sp2);
	}

	.buttons {
		display: flex;
		flex-direction: column;
		gap: var(--sp1);

		max-width: 400px;
		margin: var(--sp3) 0;
	}
</style>
