<script>
	import Pagination from './pagination_.svelte';

	let { pagination = $bindable(), value = $bindable(), ...props } = $props();
</script>

{#if props.total_page > 1}
	<Pagination bind:value {...props} bind:this={pagination}></Pagination>
{/if}
