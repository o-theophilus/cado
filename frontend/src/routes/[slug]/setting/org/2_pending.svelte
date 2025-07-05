<script>
	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';

	let { card, status } = $props();
</script>

<br />
Your request to join
{card.org.fullname}
is waiting for approval

<div class="line">
	<Button
		onclick={() => {
			status.value = 3;
		}}
	>
		Cancel Request
		<Icon icon="close" />
	</Button>
</div>

<style>
	.line {
		margin-top: var(--sp2);
		display: flex;
		gap: var(--sp1);
	}
</style>
