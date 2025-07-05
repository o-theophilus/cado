<script>
	let {
		href = '',
		blank = false,
		disabled = false,

		small = false,

		onclick,
		onmouseenter,

		children
	} = $props();
</script>

<svelte:element
	this={href ? 'a' : 'button'}
	{href}
	target={blank ? '_blank' : ''}
	{onclick}
	{onmouseenter}
	{disabled}
	role="presentation"
	class:small
>
	{@render children()}
</svelte:element>

<style>
	button,
	a {
		color: var(--ft1);
		font-weight: 700;
		text-decoration: none;
		text-align: left;
		border: none;
		background: none;
		cursor: pointer;
		fill: currentColor;

		transition: color var(--trans);
	}
	.small {
		font-size: 0.8rem;
	}

	:hover {
		color: var(--cl1);
		text-decoration: none;
	}
</style>
