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

<div class="user_menu">
	<button
		class="mobile_button"
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
	</button>

	<div class="full_button">
		<a href="/profile" class="goto_profile">
			<Avatar
				name="{user.value.firstname} {user.value.lastname}"
				photo={user.value.photo}
				size="32"
			/>

			<div class="info_1">
				<span class="name">
					{user.value.firstname}
					{user.value.lastname}
				</span>
				<span class="email">
					{user.value.email}
				</span>
			</div>
		</a>

		<button
			class="open_menu"
			onclick={() => {
				open = !open;
				self = true;
			}}
		>
			<Icon icon="keyboard_arrow_down"></Icon>
		</button>
	</div>

	{#if open}
		<div class="menu" transition:slide={{ delay: 0, duration: 200, easing: cubicInOut }}>
			<a href="/profile" class="info_2">
				<span class="name">
					{user.value.firstname}
					{user.value.lastname}
				</span>
				<span class="email">
					{user.value.email}
				</span>
			</a>

			<div class="menu_btn">
				{#if page.url.pathname != '/admin' && user.value.access.length != 0}
					<Link href="/admin">Admin</Link>
				{/if}

				<Logout />
			</div>
		</div>
	{/if}
</div>

<style>
	.user_menu {
		position: relative;
		display: flex;
	}

	a {
		text-decoration: none;
		color: var(--ft1);
	}

	.mobile_button {
		border-radius: 50%;
		outline: 8px solid transparent;
	}
	.mobile_button:hover {
		outline-color: var(--bg2);
	}

	.mobile_button,
	.open_menu,
	.goto_profile,
	.info_2 {
		border: none;
		background: transparent;
		cursor: pointer;
		transition:
			background-color var(--trans),
			outline-color var(--trans);
	}

	.full_button {
		display: none;
	}

	.open_menu {
		display: flex;
		align-items: center;
		padding: var(--sp1);
		border-radius: var(--sp0);
	}

	.goto_profile {
		display: flex;
		align-items: center;
		gap: var(--sp1);
		padding: var(--sp1);
		border-radius: var(--sp0);
	}

	.open_menu:hover,
	.goto_profile:hover,
	.info_2:hover {
		background-color: var(--bg2);
	}

	.info_1,
	.info_2 {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
	}

	.name {
		font-size: small;
		font-weight: 600;
	}
	.email {
		font-size: x-small;
	}

	.menu {
		position: absolute;
		right: 0;
		top: 50px;
		z-index: 1;

		display: flex;
		flex-direction: column;

		overflow: hidden;
		background-color: var(--bg1);
		border-radius: var(--sp0);
		box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
	}

	.menu_btn {
		display: flex;
		flex-direction: column;
		gap: var(--sp1);
		align-items: center;
		padding: var(--sp2);
	}

	.info_2 {
		padding: var(--sp2);
		border-bottom: 1px solid var(--bg2);
		align-items: center;
	}

	@media (min-width: 600px) {
		.mobile_button {
			display: none;
		}
		.full_button {
			display: flex;
		}
		.info_1 {
			display: flex;
		}
		.info_2 {
			display: none;
		}
	}
</style>
