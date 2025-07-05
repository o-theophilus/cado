<script>
	import { module, loading, token } from '$lib/store.svelte.js';

	import IG from '$lib/input_group.svelte';
	import Icon from '$lib/icon.svelte';
	import Button from '$lib/button/button.svelte';
	import Code from '$lib/input_code.svelte';

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
	<strong class="ititle"> Forgot Password </strong>

	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

	<div>
		<br />
		Verification Code has been sent to:

		<b>
			{form.email}
		</b>
	</div>

	<IG name="Verification Code" error={error.code}>
		{#snippet input()}
			<Code bind:value={form.code} />
		{/snippet}
	</IG>

	<Button primary onclick={validate_submit}
		>Submit
		<Icon icon="send" />
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
