<script>
	import { onMount } from 'svelte';
	import { icon_loaded } from '$lib/store.js';

	onMount(() => {
		const link = document.createElement('link');
		link.href =
			'https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200';
		link.rel = 'stylesheet';
		link.onload = () => {
			setTimeout(() => {
				check();
			}, 100);
		};
		document.head.appendChild(link);
	});

	const check = () => {
		const iconElement = document.getElementById('icon-check');
		const computedStyle = window.getComputedStyle(iconElement, null);
		if (computedStyle.getPropertyValue('font-family').includes('Material Symbols Outlined')) {
			$icon_loaded = true;
		} else {
			$icon_loaded = false;
		}
	};
</script>

<span id="icon-check" class="material-symbols-outlined"> check </span>

<style>
	.material-symbols-outlined {
		/* visibility: hidden; */
		display: none;
	}
</style>
