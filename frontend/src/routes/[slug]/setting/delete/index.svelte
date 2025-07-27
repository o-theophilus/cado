<script>
	import { Card, Error } from '$lib/layout';
	import Warning from './0_waning.svelte';
	import Password from './1_password.svelte';

	let { entity, type, active_card } = $props();

	let error = $state({});
	let status = $state({ value: 0 });

	let _type = $derived.by(() => {
		let n = type == 'org' ? 'organization' : type;
		return n.charAt(0).toUpperCase() + n.slice(1);
	});

	let name = 'delete';
</script>

<Card open={active_card.value == name} onopen={() => active_card.set(name)}>
	{#snippet title()}
		Delete {_type}
	{/snippet}
	
	<Error error={error.error} block --error-margin-top="0"></Error>

	{#if status.value == 0}
		<Warning {type} {status}></Warning>
	{:else if status.value == 1}
		<Password {entity} {type} {status} bind:error></Password>
	{/if}
</Card>

<style>
</style>
