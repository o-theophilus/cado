<script>
	import { onMount } from 'svelte';

	let { value = $bindable(), default_value = null, list = ['On', 'Off'], onclick } = $props();

	let btns = $state({});
	let active = $state();

	let x_pos = $derived.by(() => {
		const parentRect = active.parentElement.getBoundingClientRect();
		return active.getBoundingClientRect().left - parentRect.left - 1;
	});

	onMount(() => {
		if (default_value && list.includes(default_value)) {
			value = default_value;
		} else {
			value = list[0];
		}

		active = btns[list.indexOf(value)];
	});
</script>

<div class="gradio" style:--len={list.length}>
	{#each list as x, i}
		<button
			bind:this={btns[i]}
			onclick={(e) => {
				active = e.currentTarget;
				value = x;
				onclick?.(value);
			}}
		>
			{x}
		</button>
	{/each}
	{#if active}
		<div class="active" style:left="{x_pos}px">
			{value}
			<div>
				{value}
			</div>
		</div>
	{/if}
</div>

<style>
	.gradio {
		position: relative;

		display: grid;
		grid-template-columns: repeat(var(--len), 1fr);

		width: min-content;
		border-radius: var(--sp0);
		overflow: hidden;

		gap: 1px;
		outline: 2px solid var(--bg2);
		background: var(--bg2);
		flex-shrink: 0;
	}

	button {
		border: none;
		background-color: var(--bg1);
		cursor: pointer;
		padding: var(--sp2) var(--sp3);
		text-transform: capitalize;
	}

	.active {
		position: absolute;
		top: 0;

		padding: var(--sp2) var(--sp3);

		font-weight: 800;
		text-transform: capitalize;
		color: var(--ft1_b);

		pointer-events: none;
		transition:
			left var(--trans),
			width var(--trans);
	}

	.active div {
		position: absolute;
		inset: 2px;

		display: flex;
		align-items: center;
		justify-content: center;

		border-radius: var(--sp0);
		background-color: var(--cl1);
	}
</style>
