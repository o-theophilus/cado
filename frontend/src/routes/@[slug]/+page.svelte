<script>
	import Meta from '$lib/meta.svelte';
	import BRound from '$lib/button/round.svelte';
	import Org from './org.svelte';

	let { data } = $props();
	let org = data.org;
</script>

<Meta title={org.name} />

<section class="content">
	<div class="hline">
		<div class="page_title">Organization</div>

		<div class="hline">
			<BRound icon="card" tooltip="settings" href="/@{org.slug}/card" large></BRound>
			<BRound icon="settings" tooltip="settings" href="/@{org.slug}/setting" large></BRound>
		</div>
	</div>

	<br />

	<Org {org}></Org>
</section>

<style>
	.content {
		position: relative;

		max-width: var(--mobileWidth);
		width: 100%;
		margin: auto;
		padding: 0 var(--sp2);
		padding-bottom: var(--sp5);
	}
</style>
