<script>
	import { RoundButton } from '$lib/button';
	import Icon from '$lib/icon.svelte';
	let { card } = $props();
</script>

<div class="block">
	<img src="/bg2.jpg" alt="" />

	<div class="bottom">
		<div class="right">
			<RoundButton href="/{card.key}/setting" >
				<Icon icon="settings" size="1.2"></Icon>
			</RoundButton>
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
