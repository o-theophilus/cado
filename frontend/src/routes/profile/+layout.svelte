<script>
	import { page } from '$app/state';
	import Icon from '$lib/icon.svelte';

	let { children } = $props();
</script>

<div class="page">
	<div class="nav">
		<a href="/profile" class:active={page.route.id == '/profile'}>
			<Icon icon="person" size="2" />
		</a>
		<a href="/profile/card" class:active={page.route.id == '/profile/card'}>
			<Icon icon="card" size="2" />
		</a>
		<a href="/profile/org" class:active={page.route.id == '/profile/org'}>
			<Icon icon="corporate_fare" size="2" />
		</a>
	</div>

	<div class="content">
		{@render children()}
	</div>
</div>

<style>
	.page {
		display: flex;
		gap: var(--sp2);

		max-width: var(--mobileWidth);
		width: 100%;
		min-height: calc(100vh - var(--headerHeight));
		margin: auto;
		padding: 0 var(--sp2);
	}

	.nav {
		display: flex;
		flex-direction: column;

		padding-right: var(--sp2);
		padding-top: var(--sp2);
		border-right: 1px solid var(--bg2);
	}

	.content {
		padding: var(--sp2) 0;
		width: 100%;
	}

	a {
		display: flex;
		align-items: center;
		justify-content: center;

		width: 4rem;
		height: 4rem;

		background-color: transparent;
		border: none;
		border-radius: var(--sp0);
		cursor: pointer;

		transition: background-color var(--trans);
	}

	a:hover,
	.active {
		background-color: var(--bg2);
	}
</style>
