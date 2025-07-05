<script>
	import { goto } from '$app/navigation';
	import { module, loading, token, notify } from '$lib/store.svelte.js';

	import IG from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';

	let form = $state({});
	let error = $state({});

	const validate = () => {
		error = {};

		if (!form.name) {
			error.name = 'this field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Loading . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/org`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: token.value
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			notify.open('Card added successfully');
			module.close();
			goto(`/@${resp.org.slug}/setting`);
		} else {
			error = resp;
		}
	};
</script>

<form onsubmit={(e) => e.preventDefault()} novalidate autocomplete="off">
	<strong class="ititle"> Add Card </strong>
	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}
	<IG
		name="Name"
		icon="corporate_fare"
		error={error.name}
		placeholder="name here"
		type="text"
		bind:value={form.name}
		required
	/>

	<Button onclick={validate}>
		Submit
		<Icon icon="send" />
	</Button>

	<br />
</form>

<style>
	form {
		padding: var(--sp3);
	}
	.error {
		margin: var(--sp2) 0;
	}
</style>
