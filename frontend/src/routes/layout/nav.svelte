<script>
	import { page } from '$app/state';
	import { module, user } from '$lib/store.svelte.js';

	import Link from './nav.btn.svelte';
	import User from './nav.user.svelte';
	import Login from '../account/login.svelte';
	import Signup from '../account/signup.svelte';

	let home = $derived(page.url.pathname == '/');
</script>

<nav class:home>
	<div class="block">
		<a href="/">
			<img
				src={'/logo.png'}
				alt="logo"
				onerror={(e) => {
					const img = e.currentTarget;
					img.onerror = null;
					img.src = '/logo.png';
				}}
			/>
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
