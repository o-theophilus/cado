<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';

	import QRCode from 'qrcode';

	onMount(() => {
		QRCode.toCanvas(
			canvas,
			$page.url.href,

			// {
			// 	errorCorrectionLevel: 'H',
			// 	type: 'svg'
			// },

			(error) => {
				if (error) console.error(error);
				// console.log('success!');
			}
		);
	});

	let canvas;
</script>

<div class="header">
	<div class="block">
		<canvas bind:this={canvas} />
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

	canvas {
		border-radius: var(--sp1);
	}
</style>
