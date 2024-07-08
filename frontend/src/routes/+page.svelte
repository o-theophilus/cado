<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { module } from '$lib/store.js';

	import Meta from '$lib/meta.svelte';
	import Dialogue from '$lib/dialogue.svelte';

	onMount(() => {
		if ($page.url.searchParams.has('module')) {
			let _module = {};
			switch ($page.url.searchParams.get('module')) {
				case 'dialogue':
					_module.module = Dialogue;
					break;
			}

			for (const x of ['title', 'status', 'message']) {
				if ($page.url.searchParams.has(x)) {
					_module[x] = $page.url.searchParams.get(x);
				}
			}

			$module = _module;
			window.history.replaceState(history.state, '', '/');
		}
	});
</script>

<Meta title="Home" description="Welcome to my personal portfolio website." />

<img src="/bg1.jpg" alt="" />

<style>
	img {
		height: 480px;
		width: 100%;

		object-fit: cover;
		background-color: #eae8e9;
	}
	
	@media screen and (min-width: 900px) {
		img {
			object-fit: contain;
		}
	}
</style>
