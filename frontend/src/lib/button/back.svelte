<script>
	import { goto } from '$app/navigation';
	import BRound from '$lib/button/round.svelte';

	export let back = '';
	let disabled = false;
</script>

<BRound
	icon="arrow_back"
	large
	on:click={() => {
		if (back) {
			goto(back);
		} else {
			window.history.back();
			disabled = true;
		}
	}}
	{disabled}
/>
