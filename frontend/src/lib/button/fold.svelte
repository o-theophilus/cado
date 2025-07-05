<script>
	import BRound from '$lib/button/round.svelte';
	let { open, onclick } = $props();
</script>

<div class="fold" class:open>
	<BRound {onclick} icon="keyboard_arrow_up" />
</div>

<style>
	.fold {
		transition: transform var(--trans);
		transform: rotate(180deg);
	}
	.open {
		transform: rotate(0deg);
	}
</style>
