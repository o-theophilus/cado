<script>
	import { loading, token } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { IG } from '$lib/input';
	import { Row } from '$lib/layout';
	import Icon from '$lib/icon.svelte';
	import Note from '$lib/note.svelte';

	let { user, error = $bindable(), status } = $props();

	let form = $state({});

	const validate = () => {
		error = {};

		if (!form.password) {
			error.password = 'this field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Deleting Account . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/${user.key}`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: token.value
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			token.value = resp.token;
			document.location = '/';
		} else {
			error = resp;
		}
	};
</script>

<form onsubmit={(e) => e.preventDefault()} novalidate autocomplete="off">
	<Note status="400">
		{#snippet title()}
			Warning
		{/snippet}
		{#snippet note()}
			To proceed with deleting your account, please enter your password below to confirm your
			identity.
		{/snippet}
	</Note>

	<IG
		name="Password"
		icon="key"
		error={error.password}
		bind:value={form.password}
		type="password+"
		placeholder="Password here"
	></IG>

	<Row --row-gap="8px">
		<Button --button-background-color="var(--cl1)" --button-color="var(--ft1_b)" onclick={validate}>
			<Icon icon="delete" />
			Delete
		</Button>

		<Button
			onclick={() => {
				error = {};
				status.value = 0;
			}}
		>
			<Icon icon="arrow_back" />
			Back
		</Button>
	</Row>
</form>

<style>
</style>
