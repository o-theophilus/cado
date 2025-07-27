<script>
	import { Card } from '$lib/layout';

	import Request from './0_request_code.svelte';
	import Check from './1_check_code.svelte';
	import Password from './2_password.svelte';
	import { Error } from '$lib/layout';

	let { active_card } = $props();
	let form = $state({});
	let status = $state({ value: 0 });
	let error = $state({});
	let name = 'password';
</script>

<Card open={active_card.value == name} onopen={() => active_card.set(name)}>
	{#snippet title()}
		Change Password
	{/snippet}

	<Error error={error.error} block --error-margin-top="0"></Error>

	{#if status.value == 0}
		<Request {status} bind:error />
	{:else if status.value == 1}
		<Check {form} {status} bind:error />
	{:else if status.value == 2}
		<Password {form} {status} bind:error bind:active_card />
	{/if}
</Card>
