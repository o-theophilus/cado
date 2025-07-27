<script>
	import { Card, Error } from '$lib/layout';
	import Warning from './0_warning.svelte';
	import Password from './1_password.svelte';

	let { user, active_card } = $props();

	let error = $state({});
	let status = $state({ value: 0 });

	let name = 'delete';
</script>

<Card open={active_card.value == name} onopen={() => active_card.set(name)}>
	{#snippet title()}
		Delete Account
	{/snippet}

	<Error error={error.error} block --error-margin-top="0"></Error>

	{#if status.value == 0}
		<Warning {status}></Warning>
	{:else if status.value == 1}
		<Password {user} bind:error {status}></Password>
	{/if}
</Card>

<style>
</style>
