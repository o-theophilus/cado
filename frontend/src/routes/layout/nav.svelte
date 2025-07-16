<script>
	import { page } from '$app/state';
	import { module, user } from '$lib/store.svelte.js';

	import Link from './nav.btn.svelte';
	import User from './nav.user.svelte';
	import Login from '../account/login.svelte';
	import Signup from '../account/signup.svelte';
	import Icon from '$lib/icon.svelte';

	let home = $derived(page.url.pathname == '/');
</script>

<nav class:home>
	<div class="block">
		<a href="/">
			<Icon icon="logo" size="1.5"></Icon>

			URLinks
		</a>
		<div class="links">
			{#if user.value.login}
				<User />
			{:else}
				<Link onclick={() => module.open(Login)}>Login</Link>
				<Link onclick={() => module.open(Signup)}>Signup</Link>
			{/if}
		</div>
	</div>
</nav>

<style>
	.block {
		display: flex;
		height: var(--headerHeight);

		justify-content: space-between;
		align-items: center;

		max-width: var(--mobileWidth);
		width: 100%;
		margin: auto;
		padding: 0 var(--sp2);
	}
	a {
		display: flex;
		align-items: center;
		gap: var(--sp1);

		font-size: 1.5em;
		font-weight: 800;

		text-decoration: none;
		color: var(--ft1);
	}

	.links {
		display: flex;
		gap: var(--sp2);
	}

	.block,
	.links {
		flex-wrap: wrap;
	}
</style>
