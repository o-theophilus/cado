<script>
	import { loading } from '$lib/store.svelte.js';

	import IG from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';

	let { status } = $props();

	let name = $state('');
	let error = $state({});

	const validate = () => {
		error = {};
		if (!name) {
			error.search = 'this field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Getting Organization . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/org/${name}`);
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			status.value = 1;
			status.org = resp.org;
		} else {
			error = resp;
		}
	};
</script>

<form onsubmit={(e) => e.preventDefault()} novalidate autocomplete="off">
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
		<Button onclick={validate}>
			Submit
			<Icon icon="send" />
		</Button>
	</div>
</form>

<style>
	.error {
		margin: var(--sp2) 0;
		font-size: small;
	}

	.line {
		display: flex;
		gap: var(--sp1);
	}
</style>
