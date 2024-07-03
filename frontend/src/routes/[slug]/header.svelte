<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
</script>

<div class="header">
	<div class="block">
		<!-- <canvas bind:this={canvas} /> -->
	</div>
</div>

<style>
	.header {
		background-color: red;
		print-color-adjust: exact;
	}

	.block {
		display: flex;
		justify-content: flex-end;
		align-items: flex-end;

		height: 280px;
		max-width: var(--mobileWidth);
		width: 100%;
		margin: auto;
		padding: var(--sp2);
	}
</style>
