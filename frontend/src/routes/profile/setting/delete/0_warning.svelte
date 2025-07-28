<script>
	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';
	import { FormNote } from '$lib/layout';

	let { status } = $props();
</script>

<FormNote status="400">
	{#snippet title()}
		Warning
	{/snippet}
	{#snippet note()}
		Deleting your account irreversible and will permanently erase all associated data.
		<br />
		This action cannot be undone.
		<br />
		<br />
		Are you sure you want to continue?
	{/snippet}
</FormNote>

<Button
	--button-background-color="var(--cl1)"
	--button-color="var(--ft1_b)"
	onclick={() => {
		status.value = 1;
	}}
>
	<Icon icon="send" />
	Continue
</Button>

<style>
</style>
