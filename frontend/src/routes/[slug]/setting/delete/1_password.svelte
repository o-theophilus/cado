<script>
	import { goto } from '$app/navigation';
	import { loading, token, notify } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Row, FormNote } from '$lib/layout';
	import { IG } from '$lib/input';
	import { Icon } from '$lib/macro';

	let { entity, type, status, error = $bindable() } = $props();

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
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/delete/${type}/${entity.key}`, {
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
			notify.open(`${type == 'org' ? 'organization' : type} Deleted`);
			goto(`/profile/${type}`);
		} else {
			error = resp;
		}
	};
</script>

<form onsubmit={(e) => e.preventDefault()} novalidate autocomplete="off">
	<FormNote status="400">
		{#snippet title()}
			Warning:
		{/snippet}
		{#snippet note()}
			To proceed with deleting this card, please enter your password below to confirm your identity.
		{/snippet}
	</FormNote>

	<IG
		name="Password"
		icon="key"
		error={error.password}
		bind:value={form.password}
		type="password+"
		placeholder="Password here"
	></IG>

	<Row --row-gap="8px">
		<Button onclick={validate}>
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
