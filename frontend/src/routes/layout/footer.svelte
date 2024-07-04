<script>
	import { organization } from '$lib/store.js';

	import Contact from './footer.contact.svelte';
	import Socials from './socials.svelte';
</script>

<footer class="footer block">
	<hr />

	<div class="ititle"><strong> Contact Wragby </strong></div>
	<br />
	<Contact />
	<div class="social">
		<Socials links={$organization} />
	</div>
</footer>

<div class="copyright">
	<div class="block">© 2024 Wragby Business Solutions and Technologies Limited.</div>
</div>

<style>
	.block {
		max-width: var(--mobileWidth);
		width: 100%;
		margin: auto;
		padding: 0 var(--sp2);
	}

	hr {
		margin-bottom: var(--sp4);
	}

	.copyright {
		padding: var(--sp4) 0;

		text-align: center;
		color: var(--ft1_b);
		font-size: 0.8rem;
		background-color: var(--ft1_d);
	}

	.social {
		margin: var(--sp4) 0;
	}
</style>
