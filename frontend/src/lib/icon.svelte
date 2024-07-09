<script>
	import { icon_loaded } from '$lib/store.js';

	import SVG from './svg.svelte';
	export let icon;
	export let size = 1;
	export let fill = false;
	export let svg = false;
</script>

{#if svg}
	<SVG {icon} {size} />
{:else if $icon_loaded}
<span class:fill class="material-symbols-outlined" style:font-size="{size}em"> {icon} </span>
{:else}
<span></span>
{/if}

<style>
	.material-symbols-outlined {
		pointer-events: none;
	}

	.fill {
		font-variation-settings: 'FILL' 1;
	}
</style>
