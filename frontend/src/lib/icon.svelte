<script>
	import SVG from './svg.svelte';
	export let icon;
	export let size = 1;
	export let fill = false;
	export let svg = false;
</script>

{#if svg}
	<SVG {icon} {size} />
{:else}
	<span class:fill class="material-symbols-outlined" style:font-size="{size}em"> {icon} </span>
{/if}

<style>
	.material-symbols-outlined {
		pointer-events: none;
	}

	.fill {
		font-variation-settings: 'FILL' 1;
	}
</style>
