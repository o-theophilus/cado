<script>
	import { page } from '$app/stores';
	import { organization } from '$lib/store.js';

	import Contact from './footer.contact.svelte';
	import Socials from './socials.svelte';
</script>

<footer class="footer block">
	{#if $page.url.pathname != '/'}
		<hr />
	{/if}

	<div class="ititle"><strong> Contact Wragby </strong></div>
	<Contact />
	<div class="social">
		<Socials links={$organization} />
	</div>
</footer>

<style>
	.block {
		max-width: var(--mobileWidth);
		width: 100%;
		margin: auto;
		padding: 0 var(--sp2);
	}

	.ititle {
		margin-top: var(--sp4);
		margin-bottom: var(--sp3);
	}

	.social {
		margin: var(--sp4) 0;
	}
</style>
