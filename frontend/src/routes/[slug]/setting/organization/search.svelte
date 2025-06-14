<script>
	import { createEventDispatcher } from 'svelte';
	import { loading } from '$lib/store.js';

	import IG from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';

	let emit = createEventDispatcher();
	let name = '';

	let error = {};

	const validate = () => {
		error = {};
		if (!name) {
			error.search = 'this field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'Getting Organization . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/organization/${name}`);
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			emit('ok', resp.organization);
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

	<IG
		name="Organization"
		icon="corporate_fare"
		error={error.search}
		placeholder="Organization here"
		type="text"
		bind:value={name}
	/>

	<div class="line">
		<Button on:click={validate}>
			Submit
			<Icon icon="send" />
		</Button>
		<Button
			on:click={() => {
				emit('x');
			}}
		>
			Cancel
			<Icon icon="close" />
		</Button>
	</div>
</form>

<style>
	.error {
		margin: var(--sp2) 0;
	}

	.line {
		display: flex;
		gap: var(--sp1);
	}
</style>
