<script>
	import { Button } from '$lib/button';
	import Icon from '$lib/icon.svelte';
	import Note from '$lib/note.svelte';
	import NoteOrg from '$lib/note.org.svelte';

	let { card, status } = $props();
</script>

<Note>
	{#snippet title()}
		This card is linked with:
	{/snippet}
	{#snippet note()}
		<NoteOrg org={card.org}></NoteOrg>
	{/snippet}
</Note>

<Button
	onclick={() => {
		status.value = 3;
		status.prev_value = 4;
	}}
>
	Unlink Card
	<Icon icon="close" />
</Button>

<style>
</style>
