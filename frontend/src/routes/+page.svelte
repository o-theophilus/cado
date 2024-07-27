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

<div class="frame">
	<img src="/bg1.jpg" alt="hero" />
	<div class="block">
		<div class="content">
			<div class="copy">All Your Contacts <br /> in One Place</div>
			<div class="divider" />
			<div class="sub_copy">
				Store and manage all your essential contact information and social media links. Share your
				profile with a simple QR code scan, making networking and staying in touch easier than ever.
			</div>
		</div>
	</div>
</div>

<style>
	.frame {
		position: relative;
	}
	.block {
		position: absolute;
		inset: 0;

		display: flex;
		align-items: center;

		padding: var(--sp3);
		max-width: var(--mobileWidth);
		margin: auto;
	}

	.copy,
	.sub_copy {
		color: var(--bg1);
		max-width: 300px;

		text-shadow: 0 0 10px #0e141b;
	}

	.copy {
		font-size: 2rem;
		font-weight: 700;
	}

	.divider {
		background-color: var(--cl1);
		height: 4px;
		max-width: 100px;
		margin: var(--sp3) 0;
	}

	img {
		display: block;

		height: 480px;
		width: 100%;

		object-fit: cover;
		background-color: #0e141b;
	}

	@media screen and (min-width: 900px) {
		img {
			object-fit: contain;
		}
	}
</style>
