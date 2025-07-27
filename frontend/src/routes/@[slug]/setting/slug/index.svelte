<script>
	import { Card, Error } from '$lib/layout';
	import Slug from './0_slug.svelte';
	import Password from './1_password.svelte';

	let { org, active_card, update } = $props();

	let form = $state({});
	let error = $state({});
	let status = $state({ value: 0 });

	let name = 'slug';
</script>

<Card open={active_card.value == name} onopen={() => active_card.set(name)}>
	{#snippet title()}
		Change ID
	{/snippet}

	<Error error={error.error} block --error-margin-top="0"></Error>

	{#if status.value == 0}
		<Slug {org} {form} {status} bind:error></Slug>
	{:else if status.value == 1}
		<Password {org} {form} {status} bind:error {active_card} {update}></Password>
	{/if}
</Card>

<style>
</style>
