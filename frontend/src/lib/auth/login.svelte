<script>
	import { page } from '$app/state';
	import { module, loading, token } from '$lib/store.svelte.js';

	import IG from '$lib/input_group.svelte';
	import { Button, Link } from '$lib/button';
	import { Row } from '$lib/layout';
	import Icon from '$lib/icon.svelte';
	import Signup from './signup.svelte';
	import Forgot from './forgot_1.email.svelte';
	import ShowPassword from './password_show.svelte';
	import EmailTemplate from './confirm.template.svelte';
	import Confirm from './confirm.svelte';

	let email_template;
	let show_password = $state(false);
	let form = $state({
		email: module.value.email
	});
	let error = $state({});
	// TODO: fix return url for all auth forms
	let return_url = $state(page.url.pathname);
	if (module.value.return_url) {
		return_url = module.value.return_url;
	}

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
			document.location = return_url;
		} else if (resp.error == 'not confirmed') {
			module.open(Confirm, { email: form.email });
		} else {
			error = resp;
		}
	};
</script>

<form onsubmit={(e) => e.preventDefault()} novalidate autocomplete="off">
	<div class="page_title">Login</div>
	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

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
		type={show_password ? 'text' : 'password'}
		bind:value={form.password}
	>
		{#snippet right()}
			<div class="right">
				<ShowPassword bind:show_password />
			</div>
		{/snippet}
	</IG>

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
	.error {
		margin: var(--sp2) 0;
	}
	.right {
		padding-right: var(--sp2);
	}

	.divider {
		width: 2px;
		height: var(--sp2);
		background-color: var(--bg2);
	}
</style>
