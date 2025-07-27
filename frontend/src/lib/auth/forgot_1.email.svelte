<script>
	import { module, loading, token } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import Icon from '$lib/icon.svelte';
	import { Button, Link } from '$lib/button';

	import Login from './login.svelte';
	import Code from './forgot_2.code.svelte';
	import EmailTemplate from './forgot.template.svelte';

	let form = $state({ email: module.value.email });
	let error = $state({});
	let email_template;

	const validate = () => {
		error = {};

		if (!form.email) {
			error.email = 'this field is required';
		} else if (!/\S+@\S+\.\S+/.test(form.email)) {
			error.email = 'invalid email';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Requesting Verification Code . . .');
		form.email_template = email_template.innerHTML.replace(/&amp;/g, '&');

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/forgot/1`, {
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
			module.open(Code, form);
		} else {
			error = resp;
		}
	};
</script>

<form onsubmit={(e) => e.preventDefault()} novalidate autocomplete="off">
	<div class="page_title">Forgot Password</div>

	<Error error={error.error} block></Error>

	<IG
		name="Email"
		icon="email"
		error={error.email}
		type="email"
		bind:value={form.email}
		placeholder="Email here"
	/>

	<Button onclick={validate}>
		Submit
		<Icon icon="send" />
	</Button>

	<br />
	<br />

	<Link
		onclick={() => {
			module.open(Login, { email: form.email });
		}}
	>
		Login
	</Link>
</form>

<div bind:this={email_template} style="display: none;">
	<EmailTemplate />
</div>

<style>
	form {
		padding: var(--sp3);
	}
</style>
