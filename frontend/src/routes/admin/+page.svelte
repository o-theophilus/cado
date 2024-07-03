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
	{#if $user.permissions.includes('user:view')}
		<br />
		<Button href="/admin/users" size="wide">Users</Button>
	{/if}
	{#if $user.permissions.includes('admin:manage_photo')}
		<br />
		<Button href="/admin/photo_error" size="wide">Photo Error</Button>
	{/if}
	<br />
	<br />
	<br />
	Todo
	<br />
	home hero image
	<br />
	Update email templates
	<br />
	update admin email sender email
	<br />
	admin menu show for only admin
	<br />
	primary button / button color
	<br />
	verify organization email domain
	<br />
	header photo
	<br />
	organisation info from backend
	<br />
</Content>

<style>
</style>
