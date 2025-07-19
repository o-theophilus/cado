<script>
	import BRound from '$lib/button/round.svelte';
	import Button from '$lib/button/button.svelte';
	import IG from '$lib/input_group.svelte';
	import Icon from '$lib/icon.svelte';

	let { value = $bindable(), placeholder = 'Search', non_default = false, onclick } = $props();

	let init = $state('');
</script>

<IG
	type="text"
	{placeholder}
	bind:value
	no_pad
	onkeypress={(e) => {
		if (e.key == 'Enter') {
			init = value;
			onclick?.(value);
		}
	}}
>
	{#snippet right()}
		<div class="right">
			{#if value}
				<div class="close">
					<BRound
						icon="close"
						extra="hover_red"
						onclick={() => {
							value = '';
							init = '';
							onclick?.(value);
						}}
					/>
				</div>
			{/if}

			{#if !non_default}
				<Button
					onclick={() => {
						init = value;
						onclick?.(value);
					}}
					disabled={value == init}
				>
					<Icon icon="search" />
				</Button>
			{/if}
		</div>
	{/snippet}
</IG>

<style>
	.right {
		display: flex;
		align-items: center;
		margin-right: 2px;
		gap: 2px;
	}
	.close {
		margin-right: var(--sp1);
	}
</style>
