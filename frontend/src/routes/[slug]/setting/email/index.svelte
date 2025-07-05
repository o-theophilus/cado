<script>
	import Card from '$lib/card.svelte';

	import RequestCode from './1_request_code.svelte';
	import CheckCode from './2_check_code.svelte';

	let { entity, _type, active_card, update } = $props();
	let form = $state({ state: 0 });
	let name = 'email';
</script>

<Card open={active_card.value == name} onopen={() => active_card.set(name)}>
	{#snippet title()}
		Change Email
	{/snippet}

	{#if form.state == 0}
		<RequestCode {entity} {_type} bind:form />
	{:else if form.state == 1}
		<CheckCode {entity} {_type} bind:form bind:active_card {update} />
	{/if}
</Card>
