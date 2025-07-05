<script>
	let {
		disabled = false,
		active = false,
		no_grow = false,
		href = '',
		onclick,
		children
	} = $props();
</script>

<svelte:element
	this={href ? 'a' : 'button'}
	class:active
	class:grow={!no_grow}
	{onclick}
	{disabled}
	role="presentation"
>
	{@render children()}
</svelte:element>

<style>
	a,
	button {
		--size: 24px;

		border: none;
		height: var(--size);
		border-radius: calc(var(--size) / 2);
		padding: 0 var(--sp2);

		font-size: 0.6rem;
		cursor: pointer;
		background-color: var(--cl1_l);

		text-decoration: none;
		text-transform: capitalize;
		color: var(--ft2);

		transition:
			color var(--trans),
			background-color var(--trans);
	}
	.grow {
		flex-grow: 1;
	}

	:disabled {
		background-color: var(--bg1);
		color: var(--ft2);
		cursor: unset;
		opacity: 0.4;
	}

	:not(:disabled).active {
		background-color: var(--cl1);
		color: var(--ft1_b);
	}
	:not(:disabled):hover {
		background-color: var(--cl1_d);
		color: var(--ft1_b);
	}
</style>
