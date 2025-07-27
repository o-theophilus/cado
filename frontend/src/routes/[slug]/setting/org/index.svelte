<script>
	import { Card, Error } from '$lib/layout';
	import { onMount } from 'svelte';
	import Search from './0_search.svelte';
	import Join from './1_join.svelte';
	import Org from './2_org.svelte';
	import Cancel from './3_cancel.svelte';

	let { card, active_card } = $props();

	let status = $state({ value: 0 });
	let error = $state({});

	const update = (n) => {
		card = n;
	};

	onMount(() => {
		if (['pending', 'live'].includes(card.status)) {
			status.value = 2;
		}
	});

	let name = 'org';
</script>

<Card open={active_card.value == name} onopen={() => active_card.set(name)}>
	{#snippet title()}
		Organization
	{/snippet}

	<Error error={error.error} block --error-margin-top="0"></Error>

	{#if status.value == 0}
		<Search {status} bind:error />
	{:else if status.value == 1}
		<Join {card} {status} {update} bind:error />
	{:else if status.value == 2}
		<Org {card} {status} bind:error />
	{:else if status.value == 3}
		<Cancel {card} {status} {update} {active_card} bind:error />
	{/if}
</Card>

<style>
</style>
