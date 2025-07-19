<script>
	import Card from '$lib/card.svelte';

	import OldRequest from './1_old_request_code.svelte';
	import OldCheck from './2_old_check_code.svelte';
	import NewRequest from './3_new_request_code.svelte';
	import NewCheck from './4_new_check_code.svelte';

	let { active_card, update } = $props();
	let form = $state({ state: 0 });
	let name = 'email';
</script>

<Card open={active_card.value == name} onopen={() => active_card.set(name)}>
	{#snippet title()}
		Change Email
	{/snippet}

	{#if form.state == 0}
		<OldRequest bind:form />
	{:else if form.state == 1}
		<OldCheck bind:form />
	{:else if form.state == 2}
		<NewRequest bind:form />
	{:else if form.state == 3}
		<NewCheck bind:form bind:active_card {update} />
	{/if}
</Card>
