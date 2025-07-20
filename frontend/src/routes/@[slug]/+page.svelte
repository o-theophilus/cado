<script>
	import Meta from '$lib/meta.svelte';
	import Org from './org.svelte';

	let { data } = $props();
	let org = data.org;
</script>

<Meta title={org.name} />

<section class="content">
	<Org {org}></Org>
</section>

<style>
	.content {
		position: relative;

		max-width: var(--mobileWidth);
		width: 100%;
		margin: auto;
		padding: var(--sp2);
		padding-bottom: var(--sp5);
	}
</style>
