<script>
	import { user } from '$lib/store.js';

	import Meta from '$lib/meta.svelte';
	import Content from '$lib/content.svelte';
	import Button from '$lib/button/button.svelte';
</script>

<Meta title="Admin Dashboard" description="This contains this website settings" />

<Content>
	<strong class="ititle"> Admin Dashboard</strong>

	<div class="buttons">
		{#if $user.access.includes('user:view')}
			<Button href="/admin/users" size="wide">Users</Button>
		{/if}
		{#if $user.access.includes('user:edit_access')}
			<Button href="/admin/admin_users" size="wide">Admin Users</Button>
		{/if}
		{#if $user.access.includes('admin:view_photo_error')}
			<Button href="/admin/photo_error" size="wide">Photo Error</Button>
		{/if}
		{#if $user.access.includes('organization:view')}
			<Button href="/admin/organizations" size="wide">Organizations</Button>
		{/if}
	</div>

	<br />
	<br />
	<br />
	Todo
	<br />
	<br />
	module should always me maximum width
	<br />
	use company info from db
	<br />
	loading and notification messages
	<br />
	auto clean photo
	<br />
	delete organization
	<br />
</Content>

<style>
	.buttons {
		display: flex;
		flex-direction: column;
		gap: var(--sp1);

		max-width: 400px;
		margin: var(--sp3) 0;
	}
</style>
