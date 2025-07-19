<script>
	import Icon from '$lib/icon.svelte';
	import { onMount } from 'svelte';

	let {
		icon = null,
		wide = false,
		button = false,
		id = null,

		list = [],
		value = $bindable(),
		default_value = null,

		onchange
	} = $props();

	onMount(() => {
		if (default_value && list.includes(default_value)) {
			value = default_value;
		} else if (list[0] instanceof Object) {
			value = list[0]['value'];
		} else {
			value = list[0];
		}
	});

	export const set = (n) => {
		value = n;
	};
</script>

{#if button}
	<button class="button" class:wide>
		<div class="icon">
			<Icon {icon} size="1.2" />
		</div>
		<select
			bind:value
			onchange={() => {
				onchange?.(value);
			}}
			{id}
		>
			{#each list as x}
				<option value={x instanceof Object ? x.value : x}>
					{x instanceof Object ? x.key : x}
				</option>
			{/each}
		</select>
	</button>
{:else}
	<button class="select" class:wide>
		{#if icon}
			<div class="icon">
				<Icon {icon} size="1.2" />
			</div>
		{/if}
		<select
			bind:value
			class:has_icon={icon}
			onchange={() => {
				onchange?.(value);
			}}
			{id}
		>
			{#each list as x}
				<option value={x instanceof Object ? x.value : x}>
					{x instanceof Object ? x.key : x}
				</option>
			{/each}
		</select>
	</button>
{/if}

<style>
	button {
		position: relative;
		display: block;
		border: none;
		background-color: unset;

		width: fit-content;
	}
	button.wide {
		width: 100%;
	}
	select {
		width: 100%;
		height: 100%;
	}
	.icon {
		display: flex;
		justify-content: center;
		align-items: center;
		pointer-events: none;

		color: var(--ft2);
	}

	.select select {
		padding: var(--sp2);
		border-radius: var(--sp0);
		outline: 2px solid var(--input);

		border: none;
		color: var(--ft2);
		cursor: pointer;

		transition: outline-color var(--trans);
		text-transform: capitalize;
	}

	.select select:hover {
		outline-color: var(--cl1);
		color: var(--ft1);
	}

	.select .has_icon {
		padding-left: 48px;
	}

	.select .icon {
		position: absolute;
		height: 100%;
		aspect-ratio: 1;
	}

	.button {
		--size: 50px;
		width: var(--size);
		height: var(--size);
		border-radius: var(--sp0);

		outline: 2px solid transparent;
		background-color: var(--input);
		color: var(--ft2);

		transition:
			color var(--trans),
			outline-color var(--trans);
	}
	.button:hover:not(:disabled) {
		color: var(--ft1);
		outline-color: var(--ft1);
	}

	.button .icon {
		position: absolute;
		inset: 0;
	}

	.button select {
		opacity: 0;
	}

	option {
		color: var(--ft1_d);
	}
</style>
