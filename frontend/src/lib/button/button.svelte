<script>
	let {
		children,
		border = false,
		capitalize = false,
		disabled = false,
		onclick,
		onmouseenter,
		href = null
	} = $props();
</script>

{#if href}
	<a {href} class:border class:capitalize {onmouseenter}>
		{@render children()}
	</a>
{:else if onclick}
	<button {onclick} class:border class:capitalize {disabled} {onmouseenter}>
		{@render children()}
	</button>
{:else}
	<div class="tag" class:border class:capitalize>
		{@render children()}
	</div>
{/if}

<style>
	a,
	.tag,
	button {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		gap: 8px;

		width: var(--button-width, unset);
		height: var(--button-height, 40px);
		border-radius: var(--button-border-radius, 4px);
		padding: 0 var(--button-padding-x, 16px);

		font-size: var(--button-font-size, 1rem);
		font-weight: var(--button-font-weight, 700);
		background-color: var(--button-background-color, hsl(0, 0%, 90%));

		color: var(--button-color, hsl(0, 0%, 0%));
		fill: currentColor;
	}

	a,
	button {
		transition:
			color 0.2s ease-in-out,
			background-color 0.2s ease-in-out;
	}
	a {
		text-decoration: none;
	}

	button {
		border: none;
		cursor: pointer;
	}

	a:hover,
	button:hover {
		background-color: var(--button-background-color-hover, hsl(0, 0%, 85%));
		color: var(--button-color-hover, hsl(0, 0%, 0%));
	}

	button:disabled {
		opacity: 0.4;
		pointer-events: none;
	}

	.border {
		border: 2px solid var(--button-border-color, hsl(0, 0%, 85%));
	}
	.capitalize {
		text-transform: capitalize;
	}
</style>
