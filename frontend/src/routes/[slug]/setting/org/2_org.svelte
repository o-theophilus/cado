<script>
	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';
	import { FormNote } from '$lib/layout';
	import NoteOrg from './_org.svelte';

	let { card, status } = $props();
</script>

<FormNote status={card.status == 'pending' ? '200' : ''}>
	{#snippet title()}
		{#if card.status == 'pending'}
			Your request to join the organization is waiting for approval
		{:else}
			This card is linked with:
		{/if}
	{/snippet}
	{#snippet note()}
		<NoteOrg org={card.org}></NoteOrg>
	{/snippet}
</FormNote>

<Button
	onclick={() => {
		status.value = 3;
	}}
>
	{#if card.status == 'pending'}
		Cancel Request
	{:else}
		Unlink Card
	{/if}
	<Icon icon="close" />
</Button>

<style>
</style>
