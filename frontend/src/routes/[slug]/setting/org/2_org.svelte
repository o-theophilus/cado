<script>
	import { Button } from '$lib/button';
	import Icon from '$lib/icon.svelte';
	import Note from '$lib/note.svelte';
	import NoteOrg from './_org.svelte';

	let { card, status } = $props();
</script>

<Note status={card.status == 'pending' ? '200' : ''}>
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
</Note>

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
