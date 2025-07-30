<script>
	import { onMount } from 'svelte';
	import { user } from '$lib/store.svelte.js';
	import { Meta } from '$lib/macro';
	import Property from './property.svelte';
	import Guidelines from './guidelines.svelte';
	import Tools from './tools.svelte';
	import Layer from './layer.svelte';

	let elem;
	let fabric = $state();
	let canvas = $state();

	onMount(async () => {
		fabric = window.fabric;
		// fabric.Object.customProperties = ['id', 'name'];

		canvas = new fabric.Canvas(elem, {
			width: 500,
			height: 500,
			preserveObjectStacking: true,
			backgroundColor: '#aaaaaa'
		});
		canvas.renderAll();
		canvas.on('object:added', (e) => {
			if (e.target._type == 'guideline') return;
			canvas.setActiveObject(e.target);
		});

		return () => {
			canvas.dispose();
		};
	});
</script>

<svelte:head>
	<script src="https://cdn.jsdelivr.net/npm/fabric@latest/dist/index.min.js"></script>
</svelte:head>

<Meta title={user.value?.firstname} />

<div class="page">
	<div class="page_title">ID Design</div>

	<br />

	<canvas id="myChart" bind:this={elem}></canvas>

	{#if canvas}
		<Tools {fabric} {canvas}></Tools>
		<Property {canvas}></Property>
		<Guidelines {fabric} {canvas}></Guidelines>
		<Layer {fabric} {canvas}></Layer>
	{/if}
</div>

<style>
	.page {
		max-width: var(--mobileWidth);
		width: 100%;
		margin: auto;
		padding: var(--sp2);
		padding-bottom: var(--sp4);
	}
</style>
