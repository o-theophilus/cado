<script>
	import { user, token } from '$lib/store.svelte.js';

	import '$lib/+layout/var.css';
	import '$lib/+layout/main.css';
	import { Nav, Footer, Module, Loading, Notify } from '$lib/+layout';

	let { data, children } = $props();
	user.value = data.locals.user;
	token.value = data.locals.token;
</script>

<main>
	<div class="page">
		<Nav />
		{@render children()}
	</div>
	<Footer />

	<Module />
	<Loading />
	<Notify />
</main>

<style>
	main {
		position: relative;

		color: var(--ft2);
		transition: color var(--trans);
	}

	.page {
		min-height: 100vh;
	}
</style>
