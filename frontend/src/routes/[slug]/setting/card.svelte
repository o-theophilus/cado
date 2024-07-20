<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { module } from '$lib/store.js';

	import Icon from '$lib/icon.svelte';
	import Fold from '$lib/button/fold.svelte';

	let open = false;
</script>

<div class="block">
	<div class="line gap">
		<div class="line">
			<Icon icon="settings" size="1.2" />
			<strong class="ititle">
				<slot name="title" />
			</strong>
		</div>
		<Fold
			{open}
			on:click={() => {
				open = !open;
			}}
		/>
	</div>
	{#if open}
		<div class="links" transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
			<slot />
		</div>
	{/if}
</div>

<style>
	.block {
		margin: var(--sp1) 0;
		padding: var(--sp2);
		border-radius: var(--sp1);
		
		border: 2px solid var(--bg2);
	}
	@media screen and (min-width: 500px) {
		.block {
			padding: var(--sp3);
			border-radius: var(--sp2);
		}
	}

	.line {
		display: flex;
		align-items: center;
		gap: var(--sp2);
	}

	.gap {
		justify-content: space-between;
	}

	.ititle {
		font-size: 1.2rem;
	}
</style>
