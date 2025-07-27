<script>
	import { module, loading, token } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import Icon from '$lib/icon.svelte';
	import { Button } from '$lib/button';

	import { Dialogue } from '$lib/modal';
	import Login from './login.svelte';

	let form = $state({ ...module.value });
	let error = $state({});
	let show_password = $state(false);

	const validate = async () => {
		error = {};

		if (!form.password) {
			error.password = 'this field is required';
		} else if (
			!/[a-z]/.test(form.password) ||
			!/[A-Z]/.test(form.password) ||
			!/[0-9]/.test(form.password) ||
			form.password.length < 8 ||
			form.password.length > 18
		) {
			error.password =
				'must include at least 1 lowercase letter, 1 uppercase letter, 1 number and must contain 8 - 18 characters';
		}

		if (!form.confirm_password) {
			error.confirm_password = 'this field is required';
		} else if (form.password && form.password != form.confirm_password) {
			error.confirm_password = 'Password and confirm password does not match';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Saving Password . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/forgot/3`, {
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
			module.open(Dialogue, {
				message: 'Password Successfully changed',
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
	<div class="page_title">Forgot Password</div>

	<Error error={error.error} block></Error>

	<IG
		name="Password"
		icon="key"
		error={error.password}
		bind:value={form.password}
		type="password++"
		placeholder="Password here"
	></IG>

	<IG
		name="Confirm Password"
		icon="key"
		error={error.confirm_password}
		bind:value={form.confirm_password}
		type={show_password ? 'text' : 'password'}
		placeholder="Password here"
	/>

	<Button onclick={validate}>
		Submit
		<Icon icon="send" />
	</Button>
</form>

<style>
	form {
		padding: var(--sp3);
	}
</style>
