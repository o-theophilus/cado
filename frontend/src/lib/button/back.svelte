<script>
	import { goto } from '$app/navigation';
	import Icon from '$lib/icon.svelte';
	import { BRound } from './';

	let { href = '' } = $props();
	let disabled = $state(false);
</script>

<BRound
	onclick={() => {
		if (href) {
			goto(href);
		} else {
			window.history.back();
			disabled = true;
		}
	}}
	{disabled}
>
	<Icon icon="arrow_back"></Icon>
</BRound>
