<script>
	import { scale } from 'svelte/transition';
	import { backInOut } from 'svelte/easing';

	import { module } from '$lib/store.js';
	import BRound from '$lib/button/round.svelte';
</script>

<!-- TODO: module should always me maximum width -->
{#if $module}
	<section>
		<div class="block" transition:scale|local={{ delay: 0, duration: 200, easing: backInOut }}>
			<div class="close">
				<BRound
					icon="close"
					extra="hover_red"
					large
					on:click={() => {
						$module = null;
					}}
				/>
			</div>
			<div class="content">
				<svelte:component this={$module.module} />
			</div>
		</div>
	</section>
{/if}

<style>
	section {
		display: grid;
		align-items: center;
		justify-content: center;

		position: fixed;
		inset: 0;

		padding: var(--sp4) var(--sp3);
		overflow-y: auto;

		color: var(--ft1);
		background-color: var(--overlay);
	}

	.close {
		position: absolute;
		--pos: -10px;
		top: var(--pos);
		right: var(--pos);
	}

	.block {
		position: relative;
	}
	.content {
		background-color: var(--bg1);
		box-shadow: var(--shad1);
		border-radius: var(--sp1);

		overflow: hidden;
	}
</style>
