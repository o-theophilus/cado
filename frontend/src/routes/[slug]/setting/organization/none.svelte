<script>
	import { createEventDispatcher } from 'svelte';

	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';

	let emit = createEventDispatcher();
</script>

<div class="line">
	<Button
		on:click={() => {
			emit('search');
		}}
	>
		Search existing
		<Icon icon="search" />
	</Button>
	<Button
		on:click={() => {
			emit('new');
		}}
	>
		Add new
		<Icon icon="add" />
	</Button>
</div>

<style>
	.line {
		margin-top: var(--sp2);
		display: flex;
		gap: var(--sp1);
	}
</style>
