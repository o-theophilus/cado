<script>
	import { Card } from '$lib/layout';

	import OldRequest from './0_old_request_code.svelte';
	import OldCheck from './1_old_check_code.svelte';
	import NewRequest from './2_new_request_code.svelte';
	import NewCheck from './3_new_check_code.svelte';
	import { Error } from '$lib/layout';

	let { active_card, update } = $props();
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
		<OldRequest bind:error {status} />
	{:else if status.value == 1}
		<OldCheck {form} bind:error {status} />
	{:else if status.value == 2}
		<NewRequest {form} bind:error {status} />
	{:else if status.value == 3}
		<NewCheck {form} bind:error bind:active_card {update} {status} />
	{/if}
</Card>
