<script>
	import { notify } from '$lib/store.svelte.js';

	import Icon from '$lib/icon.svelte';
	import { RoundButton } from '$lib/button';
	import { Row } from '$lib/layout';

	let { one } = $props();

	setTimeout(() => {
		notify.close(one.key);
	}, 5000);

	let to_zero = $state(false);
	setTimeout(() => {
		to_zero = true;
	});
</script>

<div class="notify" class:bad={one.status == 400} class:caution={one.status == 201}>
	<div class="padding">
		<Row>
			<Icon
				size="2"
				icon={one.status == 201 ? 'error' : one.status == 400 ? 'cancel' : 'check_circle'}
			/>
			{one.message || 'no message'}
			<RoundButton onclick={() => notify.close(one.key)}>
				<!-- TODO: fill black -->
				<Icon icon="close"></Icon>
			</RoundButton>
		</Row>
	</div>

	<div class="progress" class:to_zero></div>
</div>

<style>
	.notify {
		width: fit-content;
		max-width: 300px;

		display: flex;
		flex-direction: column;
		align-items: end;

		background-color: var(--cl3);
		border-radius: var(--sp0);
		color: var(--ft1_b);
		fill: currentColor;

		pointer-events: all;
	}

	.padding {
		padding: var(--sp2);
	}

	.progress {
		width: 100%;
		height: 2px;
		background-color: var(--bg1);

		transition: width 5s linear;
	}

	.to_zero {
		width: 0;
	}

	.bad {
		background-color: var(--cl2);
	}
	.caution {
		background-color: var(--cl4);
	}
</style>
