<script>
	
	import { loading, notification } from '$lib/store.js';
	import { token } from '$lib/cookie.js';
	import { createEventDispatcher } from 'svelte';

	import IG from '$lib/input_group.svelte';
	import Icon from '$lib/icon.svelte';
	import Button from '$lib/button/button.svelte';
	import Code from '$lib/input_code.svelte';

	export let form;
	let error = {};
	let emit = createEventDispatcher();

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
		$loading = 'Verifying Code . . .';

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/organization/add/2`, {
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
			$notification = {
				message: 'Organization Created'
			};
			emit('ok', resp.user);
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="ititle"> Add Organization </strong>
	<br />
	Verification Code has been sent to: {form.email}.

	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

	<IG name="Verification Code" error={error.code}>
		<Code bind:value={form.code} />
	</IG>

	<div class="line">
		<Button primary on:click={validate}
			>Submit
			<Icon icon="send" />
		</Button>

		<Button
			on:click={() => {
				emit('x');
			}}
		>
			back
			<Icon icon="close" />
		</Button>
	</div>
</form>

<style>
	.error {
		margin: var(--sp2) 0;
	}

	.line {
		display: flex;
		gap: var(--sp1);
	}
</style>
