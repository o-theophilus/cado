<script>
	import Icon from '$lib/icon.svelte';

	let { status, title, note } = $props();

	let _status = $derived.by(() => {
		if (status == 200) {
			return 'check_circle';
		} else if (status == 201) {
			return 'error';
		} else if (status == 400) {
			return 'cancel';
		} else {
			return 'info';
		}
	});
</script>

<div class="block {_status}">
	{#if title}
		<div class="title {_status}">
			<Icon icon={_status} size="2" />
			{@render title()}
		</div>
	{/if}

	{#if title && note}
		<br />
	{/if}

	{#if note}
		{@render note()}
	{/if}
</div>

<style>
	.block {
		padding: var(--sp2);
		margin-bottom: var(--sp2);

		background-color: var(--bg2);
		border-radius: var(--sp0);
		font-size: 0.8rem;
		color: var(--ft2);
	}

	.title {
		display: flex;
		align-items: center;
		gap: var(--sp2);

		fill: currentColor;
		font-weight: 800;
	}

	.block.check_circle {
		background-color: color-mix(in srgb, var(--cl3), transparent 90%);
	}
	.block.error {
		background-color: color-mix(in srgb, var(--cl4), transparent 90%);
	}
	.block.cancel {
		background-color: color-mix(in srgb, var(--cl2), transparent 90%);
	}
	.title.check_circle {
		color: var(--cl3);
	}
	.title.error {
		color: var(--cl4);
	}
	.title.cancel {
		color: var(--cl2);
	}
</style>
