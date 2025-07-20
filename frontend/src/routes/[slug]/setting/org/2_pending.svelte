<script>
	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Note from '$lib/note.svelte';
	import NoteOrg from '$lib/note.org.svelte';

	let { card, status } = $props();
</script>

<Note status="200">
	{#snippet title()}
		Your request to join the organization is waiting for approval
	{/snippet}
	{#snippet note()}
		<NoteOrg org={card.org}></NoteOrg>
	{/snippet}
</Note>

<Button
	onclick={() => {
		status.value = 3;
		status.prev_value = 2;
	}}
>
	Cancel Request
	<Icon icon="close" />
</Button>

<style>
</style>
