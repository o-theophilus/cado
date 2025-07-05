<script>
	import BRound from '$lib/button/round.svelte';
	let { card } = $props();
</script>

<div class="block">
	<img src="/bg2.jpg" alt="" />

	<div class="bottom">
		<div class="right">
			<BRound icon="settings" href="/{card.key}/setting"></BRound>
		</div>
	</div>
</div>

<style>
	.block {
		position: relative;
	}
	img {
		display: block;
		height: 280px;
		width: 100%;

		object-fit: cover;
		background-color: #eae8e9;
		line-height: 0;
		font-size: 0;
	}

	.bottom {
		position: absolute;
		bottom: 0;
		padding: var(--sp2);

		width: 100%;
	}

	.right {
		display: flex;
		justify-content: flex-end;

		max-width: var(--mobileWidth);
		margin: auto;
	}
</style>
