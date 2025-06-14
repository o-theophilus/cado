<script>
	import { createEventDispatcher } from 'svelte';

	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';

	export let user;
	let emit = createEventDispatcher();
</script>

<br />
Your request to join
{user.organization.fullname}
is waiting for approval

<div class="line">
	<Button
		on:click={() => {
			emit('x');
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
