<script>
	import { module, loading, token } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button, Link } from '$lib/button';
	import { Icon } from '$lib/macro';
	import { Error } from '$lib/layout';
	import Login from './login.svelte';
	import EmailTemplate from './confirm.template.svelte';
	import Confirm from './confirm.svelte';

	let email_template;
	let show_password = $state(false);
	let form = $state({ email: module.value.email });
	let error = $state({});

	const validate = () => {
		error = {};

		if (!form.firstname) {
			error.firstname = 'this field is required';
		}
		if (!form.lastname) {
			error.lastname = 'this field is required';
		}
		if (!form.email) {
			error.email = 'this field is required';
		} else if (!/\S+@\S+\.\S+/.test(form.email)) {
			error.email = 'invalid email';
		}

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
			error.confirm_password = 'does not match password';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		form.email_template = email_template.innerHTML.replace(/&amp;/g, '&');

		loading.open('Loading . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/signup`, {
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
			module.open(Confirm, { email: form.email });
		} else {
			error = resp;
		}
	};
</script>

<form onsubmit={(e) => e.preventDefault()} novalidate autocomplete="off">
	<div class="page_title">Signup</div>

	<Error error={error.error} block></Error>

	<IG
		name="Firstname"
		icon="person"
		error={error.firstname}
		placeholder="Firstname here"
		type="text"
		bind:value={form.firstname}
	/>
	<IG
		name="Lastname"
		icon="person"
		error={error.lastname}
		placeholder="Lastname here"
		type="text"
		bind:value={form.lastname}
	/>
	<IG
		name="Email"
		icon="email"
		error={error.email}
		placeholder="Email here"
		type="text"
		bind:value={form.email}
	/>
	<IG
		name="Password"
		icon="key"
		error={error.password}
		placeholder="Password here"
		type="password++"
		bind:value={form.password}
		bind:show_password
	></IG>
	<IG
		name="Confirm Password"
		icon="key"
		error={error.confirm_password}
		placeholder="Password here"
		type="password"
		bind:value={form.confirm_password}
		bind:show_password
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
