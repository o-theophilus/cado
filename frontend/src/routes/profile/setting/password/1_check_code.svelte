<script>
	import { loading, user, token } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Row } from '$lib/layout';
	import { IG } from '$lib/input';
	import Icon from '$lib/icon.svelte';
	import Note from '$lib/note.svelte';

	let { form, error = $bindable(), status } = $props();

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
		loading.open('Verifying Code . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/password/2`, {
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
			status.value = 2;
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
				{user.value.email}
			</span>
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
				form.code = null;
				form.password = null;
				form.confirm_password = null;
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
