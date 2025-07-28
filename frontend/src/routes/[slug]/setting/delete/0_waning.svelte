<script>
	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';
	import { FormNote } from '$lib/layout';

	let { type, status } = $props();
</script>

<FormNote status="400">
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
</FormNote>

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
