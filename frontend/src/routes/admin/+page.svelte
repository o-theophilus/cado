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

	<br />
	<br />
	<br />
	Todo
	<br />
	<br />
	form should always me maximum width
	<br />
	email delivery is slow
	<br />
	auto manage_photo
	<br />
	admin edit company info
	<br />
</Content>

<style>
</style>
