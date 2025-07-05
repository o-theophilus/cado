<script>
	import Card from '$lib/card.svelte';

	import Request from './1_request_code.svelte';
	import Check from './2_check_code.svelte';
	import Password from './3_password.svelte';

	let { active_card } = $props();
	let form = $state({ state: 0 });
	let name = 'password';
</script>

<Card open={active_card.value == name} onopen={() => active_card.set(name)}>
	{#snippet title()}
		Change Password
	{/snippet}

	{#if form.state == 0}
		<Request bind:form />
	{:else if form.state == 1}
		<Check bind:form />
	{:else if form.state == 2}
		<Password bind:form bind:active_card />
	{/if}
</Card>
