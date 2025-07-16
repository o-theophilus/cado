<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { page } from '$app/state';

	import { user } from '$lib/store.svelte.js';

	import Link from './nav.btn.svelte';
	import Logout from '../account/logout.svelte';
	import Avatar from '$lib/avatar.svelte';
	import Icon from '$lib/icon.svelte';

	let open = false;
	let self = false;
</script>

<svelte:window
	onclick={() => {
		if (open && !self) {
			open = false;
		}
		self = false;
	}}
/>

<div class="user">
	<button
		onclick={() => {
			open = !open;
			self = true;
		}}
	>
		<Avatar
			name="{user.value.firstname} {user.value.lastname}"
			photo={user.value.photo}
			size="32"
		/>
		<div class="detail">
			<span class="name">
				{user.value.firstname}
				{user.value.lastname}
			</span>
			<span class="email">
				{user.value.email}
			</span>
		</div>
	</button>

	{#if open}
		<div class="menu" transition:slide={{ delay: 0, duration: 200, easing: cubicInOut }}>
			{#if page.url.pathname != `/profile`}
				<Link href="/profile">Profile</Link>
			{/if}
			{#if page.url.pathname != '/admin' && user.value.access.length != 0}
				<Link href="/admin">Admin</Link>
			{/if}

			<Logout />
		</div>
	{/if}
</div>

<style>
	.user {
		position: relative;
		display: flex;
	}

	button {
		display: flex;
		align-items: center;
		gap: var(--sp1);

		padding: var(--sp1);

		border-radius: var(--sp0);

		background-color: transparent;
		border: none;
		cursor: pointer;

		transition: background-color var(--trans);
	}

	button:hover {
		background-color: var(--bg2);
	}

	.detail {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
	}
	.name {
		font-size: 0.8em;
		font-weight: 600;
	}
	.email {
		font-size: 0.6em;
	}

	.menu {
		position: absolute;
		right: 0;
		top: 50px;
		z-index: 1;

		display: flex;
		flex-direction: column;
		gap: var(--sp2);

		background-color: var(--bg1);

		padding: var(--sp2);
		border-radius: var(--sp0);
		box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
	}
</style>
