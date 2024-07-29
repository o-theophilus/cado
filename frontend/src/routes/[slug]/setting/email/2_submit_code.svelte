<script>
	import { module, loading, user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';
	import { createEventDispatcher } from 'svelte';

	import Button from '$lib/button/button.svelte';
	import IG from '$lib/input_group.svelte';
	import Icon from '$lib/icon.svelte';
	import Code from '$lib/input_code.svelte';

	let emit = createEventDispatcher();
	let form = {};
	let error = {};

	const validate = () => {
		error = {};

		if (!form.code_1) {
			error.code_1 = 'this field is required';
		} else if (form.code_1.length != 6) {
			error.code_1 = 'invalid verification code';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'Verifying Code . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/email/2`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			emit('ok', form.code_1);
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

	<div class="note">
		Verification Code has been sent to:

		<span>
			{$user.email}
		</span>

		.
	</div>

	<IG name="Verification Code" error={error.code_1}>
		<Code bind:value={form.code_1} />
	</IG>

	<Button primary on:click={validate}>
		Submit
		<Icon icon="send" />
	</Button>
</form>

<style>
	.error {
		margin: var(--sp2) 0;
	}

	.note {
		padding: var(--sp2);
		margin: var(--sp2) 0;
		background-color: var(--bg2);
		font-size: 0.8rem;

		border-radius: var(--sp0);
	}

	.note span {
		font-weight: 800;
	}
</style>
