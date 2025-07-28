<script>
	import { Card, Error } from '$lib/layout';
	import RequestCode from './0_request_code.svelte';
	import CheckCode from './1_check_code.svelte';

	let { entity, type, active_card, update } = $props();
	let form = $state({});
	let status = $state({ value: 0 });
	let error = $state({});
	let name = 'email';
</script>

<Card open={active_card.value == name} onopen={() => active_card.set(name)}>
	{#snippet title()}
		Change Email
	{/snippet}

	<Error error={error.error} block --error-margin-top="0"></Error>

	{#if status.value == 0}
		<RequestCode {entity} {type} {form} {status} bind:error />
	{:else if status.value == 1}
		<CheckCode {entity} {type} {form} {status} bind:error bind:active_card {update} />
	{/if}
</Card>
