<script>
	import { user, module } from '$lib/store.js';
	import { page } from '$app/stores';

	import Link from './nav.btn.svelte';
	import User from './nav.user.svelte';
	import Login from '../account/login.svelte';
	import Signup from '../account/signup.svelte';

	$: home = $page.url.pathname == '/';
</script>

<nav class:home>
	<div class="block">
		<a href="/">
			<img src="/logo.png" alt="Wragby Logo" />
		</a>
		<div class="links">
			{#if $user && $user.login}
				<User />
			{:else}
				<Link
				
					on:click={() => {
						$module = {
							module: Login
						};
					}}
				>
					Login
				</Link>

				<Link
				
					on:click={() => {
						$module = {
							module: Signup
						};
					}}
				>
					Signup
				</Link>
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

	img {
		height: 32px;
		display: block;
	}

	.links {
		display: flex;
		gap: var(--sp2);
	}

	.block,
	.links {
		flex-wrap: wrap;
	}

	.home a {
		color: var(--bg1);
	}
</style>
