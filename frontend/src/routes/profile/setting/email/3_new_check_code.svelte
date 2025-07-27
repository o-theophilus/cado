<script>
	import { loading, token, notify } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Row } from '$lib/layout';
	import { IG } from '$lib/input';
	import Icon from '$lib/icon.svelte';
	import Note from '$lib/note.svelte';

	let { form, error = $bindable(), active_card, update, status } = $props();

	const validate = () => {
		error = {};

		if (!form.code_2) {
			error.code_2 = 'this field is required';
		} else if (form.code_2.length != 6) {
			error.code_2 = 'invalid verification code';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Verifying Code / Saving Email . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/email/4`, {
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
			update(resp.user);

			status.value = 0;
			form.code_1 = null;
			form.code_2 = null;

			active_card.close();
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

	<IG name="Verification Code" bind:value={form.code_2} type="code" error={error.code_2}></IG>

	<Row --row-gap="8px">
		<Button primary onclick={validate}>
			Submit
			<Icon icon="send" />
		</Button>

		<Button
			onclick={() => {
				error = {};
				form.code_1 = null;
				form.code_2 = null;
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
