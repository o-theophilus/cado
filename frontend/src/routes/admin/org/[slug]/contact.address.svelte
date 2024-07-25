<script>
	import IG from '$lib/input_group.svelte';
	import Icon from '$lib/icon.svelte';
	import BRound from '$lib/button/round.svelte';
	import { createEventDispatcher } from 'svelte';

	let emit = createEventDispatcher();
	export let one;
	export let i;
	export let error;
</script>

<div class="block">
	<div class="line">
		<div class="line">
			<Icon icon="location_on" />
			<span class="name">
				Address {i + 1}
			</span>
		</div>
		<BRound
			icon="close"
			on:click={() => {
				emit('remove');
			}}
		/>
	</div>

	<IG
		name="Name"
		type="text"
		bind:value={one.name}
		placeholder="Name here"
		error={error[i]?.name}
	/>
	<IG
		name="Address"
		type="textarea"
		bind:value={one.address}
		placeholder="Address here"
		error={error[i]?.address}
	/>
	<IG name="URL" type="text" bind:value={one.url} placeholder="URL here" />
</div>

<style>
	.block {
		border: 2px solid var(--bg2);
		padding: var(--sp2);
		padding-bottom: 0;

		margin: var(--sp1) 0;
		border-radius: var(--sp1);

		transition: border-color var(--trans);
	}

	.block:hover {
		border-color: var(--ft1);
	}

	.line {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: var(--sp1);
	}

	.name {
		font-weight: 800;
	}
</style>
