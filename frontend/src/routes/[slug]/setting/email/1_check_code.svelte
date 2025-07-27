<script>
	import { loading, token, notify } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Row } from '$lib/layout';
	import { IG } from '$lib/input';
	import Icon from '$lib/icon.svelte';
	import Note from '$lib/note.svelte';

	let { entity, type, form, error = $bindable(), status, active_card, update } = $props();

	const validate = () => {
		error = {};

		if (!form.code) {
			error.code = 'this field is required';
		} else if (form.code.length != 6) {
			error.code = 'invalid verification code';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Verifying Code / Saving Email . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/email/2/${type}/${entity.key}`, {
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
			form.email = null;
			status.value = 0;

			active_card.close();
			update(resp[type]);
			notify.open('Email changed');
		} else {
			error = resp;
		}
	};
</script>

<form onsubmit={(e) => e.preventDefault()} novalidate autocomplete="off">
	<Note>
		{#snippet note()}
			Verification Code has been sent to:
			<span>
				{form.email}
			</span>
			.
		{/snippet}
	</Note>

	<IG name="Verification Code" bind:value={form.code} type="code" error={error.code}></IG>

	<Row --row-gap="8px">
		<Button primary onclick={validate}>
			Submit
			<Icon icon="send" />
		</Button>

		<Button
			onclick={() => {
				error = {};
				status.value = 0;
			}}
		>
			Cancel
			<Icon icon="close" />
		</Button>
	</Row>
</form>

<style>
	span {
		font-weight: 800;
	}
</style>
