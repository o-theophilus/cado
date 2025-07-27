<script>
	import { module, loading } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import Icon from '$lib/icon.svelte';
	import { Button } from '$lib/button';

	import { Dialogue } from '$lib/modal';
	import Login from './login.svelte';

	let form = $state({ email: module.value.email });
	let error = $state({});

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
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/confirm`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			module.open(Dialogue, {
				title: 'Signup Complete',
				message: 'Your email has been confirmed successfully.',
				buttons: [
					{
						name: 'Login',
						icon: 'login',
						fn: () => {
							module.open(Login, { email: form.email });
						}
					}
				]
			});
		} else {
			error = resp;
		}
	};
</script>

<form onsubmit={(e) => e.preventDefault()} novalidate autocomplete="off">
	<div class="page_title">Confirm Email</div>
	<br />
	A Verification Code has been sent to your email.
	<br />
	<!-- FIXME: remove this br -->

	<Error error={error.error} block></Error>

	<IG name="Verification Code" bind:value={form.code} type="code" error={error.code}></IG>

	<Button onclick={validate}>
		Submit <Icon icon="send" />
	</Button>
</form>

<style>
	form {
		padding: var(--sp3);
	}
</style>
