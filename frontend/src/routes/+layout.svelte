<script>
	import { user, organization, to_print } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import './layout/var.css';
	import './layout/main.css';
	import Nav from './layout/nav.svelte';
	import Footer from './layout/footer.svelte';

	import Module from './layout/_module.svelte';
	import Loading from './layout/_loading.svelte';
	import Notification from './layout/_notification.svelte';
	import Icon from './layout/icon.svelte';
	import Print from './[slug]/print.svelte';

	export let data;
	$user = data.locals.user;
	$token = data.locals.token;
	$organization = data.locals.organization;
</script>

<main class:hide={$to_print}>
	<Nav />
	<slot />
	<Footer />

	<Module />
	<Loading />
	<Notification />
	<Icon />
</main>

{#if $to_print}
	<Print user={$to_print} />
{/if}

<style>
	main {
		position: relative;

		background-color: var(--bg1);
		color: var(--ft2);
		transition: background-color var(--trans), color var(--trans);
	}

	.hide {
		display: none;
	}
</style>
