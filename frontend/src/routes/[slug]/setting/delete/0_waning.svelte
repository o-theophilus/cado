<script>
	import { Button } from '$lib/button';
	import Icon from '$lib/icon.svelte';
	import Note from '$lib/note.svelte';

	let { type, status } = $props();
</script>

<Note status="400">
	{#snippet title()}
		Warning:
	{/snippet}
	{#snippet note()}
		Deleting this {type == 'org' ? 'organization' : type} is irreversible and will permanently erase
		all associated data.
		<br />
		This action cannot be undone.
		<br />
		<br />
		Are you sure you want to continue?
	{/snippet}
</Note>

<Button
	onclick={() => {
		status.value = 1;
	}}
>
	<Icon icon="send" />
	Continue
</Button>

<style>
</style>
