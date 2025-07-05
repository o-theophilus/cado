<script>
	import Card from '$lib/card.svelte';
	import { onMount } from 'svelte';
	import Search from './0_search.svelte';
	import Join from './1_join.svelte';
	import Pending from './2_pending.svelte';
	import Cancel from './3_cancel.svelte';
	import Org from './4_org.svelte';

	let { card, active_card } = $props();

	let status = $state({
		value: 0
	});

	const update = (n) => {
		card = n;
	};

	onMount(() => {
		if (card.status == 'pending') {
			status.value = 2;
		} else if (card.status == 'live') {
			status.value = 4;
		}
	});

	let name = 'org';
</script>

<Card open={active_card.value == name} onopen={() => active_card.set(name)}>
	{#snippet title()}
		Organization
	{/snippet}

	{#if status.value == 0}
		<Search {status} />
	{:else if status.value == 1}
		<Join {card} {status} {update} />
	{:else if status.value == 2}
		<Pending {card} {status} />
	{:else if status.value == 3}
		<Cancel {card} {status} {update} {active_card} />
	{:else if status.value == 4}
		<Org {card} {status} />
	{/if}
</Card>

<style>
</style>
