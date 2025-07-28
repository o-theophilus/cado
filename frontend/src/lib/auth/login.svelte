<script>
	import { page } from '$app/state';
	import { module, loading, token } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button, Link } from '$lib/button';
	import { Row, Error } from '$lib/layout';
	import { Icon } from '$lib/macro';
	import Signup from './signup.svelte';
	import Forgot from './forgot_1.email.svelte';
	import EmailTemplate from './confirm.template.svelte';
	import Confirm from './confirm.svelte';

	let email_template;
	let form = $state({
		email: module.value.email
	});
	let error = $state({});

	const validate = () => {
		error = {};

		if (!form.email) {
			error.email = 'this field is required';
		}
		if (!form.password) {
			error.password = 'this field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		form.email_template = email_template.innerHTML.replace(/&amp;/g, '&');

		loading.open('Loading . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/login`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: token.value
			},
			body: JSON.stringify(form)
		});

		resp = await resp.json();
		if (resp.status != 200) {
			loading.close();
		}

		if (resp.status == 200) {
			token.value = resp.token;
			document.location = page.url.pathname;
		} else if (resp.error == 'not confirmed') {
			module.open(Confirm, { email: form.email });
		} else {
			error = resp;
		}
	};
</script>

<form onsubmit={(e) => e.preventDefault()} novalidate autocomplete="off">
	<div class="page_title">Login</div>

	<Error error={error.error} block></Error>

	<IG
		name="Email"
		icon="email"
		error={error.email}
		type="email"
		bind:value={form.email}
		placeholder="Email here"
	/>

	<IG
		name="Password"
		icon="key"
		error={error.password}
		placeholder="Password here"
		type="password+"
		bind:value={form.password}
	></IG>

	<Button onclick={validate}>
		Submit
		<Icon icon="send" />
	</Button>

	<br />
	<br />
	<Row>
		<Link
			onclick={() => {
				module.open(Signup, { email: form.email });
			}}
		>
			Signup
		</Link>
		<span class="divider"> </span>
		<Link
			onclick={() => {
				module.open(Forgot, { email: form.email });
			}}
		>
			Forgot Password
		</Link>
	</Row>
</form>

<div bind:this={email_template} style="display: none;">
	<EmailTemplate />
</div>

<style>
	form {
		padding: var(--sp3);
	}

	.divider {
		width: 2px;
		height: var(--sp2);
		background-color: var(--bg2);
	}
</style>
