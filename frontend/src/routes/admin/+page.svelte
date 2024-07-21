<script>
	import { user } from '$lib/store.js';

	import Meta from '$lib/meta.svelte';
	import Content from '$lib/content.svelte';
	import Button from '$lib/button/button.svelte';
</script>

<Meta title="Admin Dashboard" description="This contains this website settings" />

<Content>
	<strong class="ititle"> Admin Dashboard</strong>
	<br />
	{#if $user.access.includes('user:view')}
		<br />
		<Button href="/admin/users" size="wide">Users</Button>
	{/if}
	{#if $user.access.includes('user:edit_access')}
		<br />
		<Button href="/admin/admin_users" size="wide">Admin Users</Button>
	{/if}
	{#if $user.access.includes('admin:view_photo_error')}
		<br />
		<Button href="/admin/photo_error" size="wide">Photo Error</Button>
	{/if}
	{#if $user.access.includes('organization:view')}
		<br />
		<Button href="/admin/organizations" size="wide">Organizations</Button>
	{/if}

	<br />
	<br />
	<br />
	Todo
	<br />
	<br />
	form should always me maximum width
	<br />
	admin edit company info
	<br />
	loading and notification messages
	<br />
</Content>

<style>
</style>
