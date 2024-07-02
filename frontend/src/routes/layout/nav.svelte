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
			{home}
			on:click={() => {
				$module = {
					module: Login
				};
			}}
				>
				Login
			</Link>
			
			<Link
				{home}
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
		height: 40px;
	}

	.links {
		display: flex;
		gap: var(--sp2);
	}
	a {
		display: flex;
		align-items: center;
		gap: var(--sp1);

		color: var(--ft1);
		fill: var(--cl1);
		font-size: large;
		font-weight: 800;

		text-decoration: none;

		transition: color var(--trans);
	}

	.block,
	.links {
		flex-wrap: wrap;
	}

	.home a {
		color: var(--bg1);
	}
</style>
