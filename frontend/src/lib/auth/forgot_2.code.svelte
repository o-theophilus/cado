<script>
	import { module, loading, token } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Icon } from '$lib/macro';
	import { Button } from '$lib/button';
	import { FormNote, Error } from '$lib/layout';

	import Password from './forgot_3.password.svelte';

	let form = $state({ ...module.value });
	let error = $state({});

	const validate_submit = async () => {
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
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/forgot/2`, {
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
			module.open(Password, form);
		} else {
			error = resp;
		}
	};
</script>

<form onsubmit={(e) => e.preventDefault()} novalidate autocomplete="off">
	<div class="page_title">Forgot Password</div>

	<Error error={error.error} block></Error>

	<FormNote status="200" --note-margin-top="16px" --note-margin-bottom="16px">
		{#snippet note()}
			Verification Code has been sent to:
			<b> {form.email} </b>
		{/snippet}
	</FormNote>

	<IG name="Verification Code" bind:value={form.code} type="code" error={error.code}></IG>

	<Button onclick={validate_submit}
		>Submit
		<Icon icon="send" />
	</Button>
</form>

<style>
	form {
		padding: var(--sp3);
	}
</style>
