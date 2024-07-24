<script>
	import { createEventDispatcher } from 'svelte';
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';

	import Fold from '$lib/button/fold.svelte';

	let emit = createEventDispatcher();
	export let open = false;
</script>

<div class="block">
	<div
		class="line title"
		role="presentation"
		on:click={() => {
			emit('open', !open);
		}}
	>
		<div class="line">
			<strong class="ititle">
				<slot name="title" />
			</strong>
		</div>
		<Fold {open} />
	</div>

	{#if open}
		<div class="content" transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
			<slot />
		</div>
	{/if}
</div>

<style>
	.block {
		margin: var(--sp1) 0;
		border-radius: var(--sp0);

		/* border: 1px solid var(--bg2); */
		box-shadow: 0px 0px 10px rgba(126, 126, 126, 0.1);

		background-color: var(--bg1);
	}

	.line {
		display: flex;
		align-items: center;
		gap: var(--sp2);
	}

	.title {
		justify-content: space-between;
		padding: var(--sp2);
	}

	.ititle {
		font-size: 1.1rem;
	}

	.content {
		border-top: 1px solid var(--bg2);
		padding: var(--sp2);
		padding-top: 0;
	}

	@media screen and (min-width: 500px) {
		.title {
			padding: var(--sp3);
		}
		.content {
			padding: var(--sp3);
			padding-top: 0;
		}
	}
</style>
