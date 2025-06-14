<script>
	import { createEventDispatcher } from 'svelte';

	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';

	let emit = createEventDispatcher();
	export let user;
</script>

{user.organization.fullname}

<Button
	on:click={() => {
		emit('ok');
	}}
>
	Exit
	<Icon icon="close" />
</Button>

<style>
</style>
