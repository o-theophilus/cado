<script>
	import Gradio from './gradio_.svelte';
	let { value = $bindable(), ...props } = $props();
</script>

{#if props.list.length}
	<Gradio bind:value {...props}></Gradio>
{/if}
