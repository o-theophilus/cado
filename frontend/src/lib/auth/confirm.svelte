<script>
	import { module, loading } from '$lib/store.svelte.js';

	import IG from '$lib/input_group.svelte';
	import Icon from '$lib/icon.svelte';
	import { Button } from '$lib/button';
	import Code from '$lib/input_code.svelte';

	import Dialogue from '$lib/dialogue.svelte';
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

	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

	<IG name="Verification Code" error={error.code}>
		{#snippet input()}
			<Code bind:value={form.code} />
		{/snippet}
	</IG>

	<Button onclick={validate}>
		Submit <Icon icon="send" />
	</Button>
</form>

<style>
	form {
		padding: var(--sp3);
	}

	.error {
		margin: var(--sp2) 0;
	}
</style>
