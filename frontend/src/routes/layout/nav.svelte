<script>
	import { module, user } from '$lib/store.svelte.js';

	import Link from './nav.btn.svelte';
	import User from './nav.user.svelte';
	import Login from '$lib/auth/login.svelte';
	import Signup from '$lib/auth/signup.svelte';
</script>

<nav>
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
	nav {
		border-bottom: 1px solid var(--bg2);
	}
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
</style>
