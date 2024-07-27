<script>
	import { createEventDispatcher } from 'svelte';

	import IG from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';

	let emit = createEventDispatcher();
	export let slug;
	export let error = {};
	let form = {
		slug
	};

	const validate = () => {
		error = {};
		if (!form.slug) {
			error.slug = 'this field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		emit('ok', form.slug);
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<IG
		name="Username"
		icon="language"
		error={error.slug}
		placeholder="Username here"
		type="text"
		bind:value={form.slug}
		required
	/>

	<Button on:click={validate}>
		Submit
		<Icon icon="send" />
	</Button>
</form>
