<script>
	import { user, loading, organization } from '$lib/store.js';
	import { token } from '$lib/cookie.js';
	import { createEventDispatcher } from 'svelte';

	import Button from '$lib/button/button.svelte';
	import IG from '$lib/input_group.svelte';
	import Icon from '$lib/icon.svelte';
	import EmailTemplate from './email_template.svelte';

	let emit = createEventDispatcher();
	export let code_1;
	let form = {
		code_1: code_1
	};
	let error = {};
	let email_template;

	const validate = () => {
		error = {};

		if (!form.email) {
			error.email = 'this field is required';
		} else if (!/\S+@\S+\.\S+/.test(form.email)) {
			error.email = 'Please enter a valid email';
		} else if (form.email == $user.email) {
			error.email = 'please use a different email form your current email';
		} else if (
			$organization.email_domains.length > 0 &&
			!$organization.email_domains.some((x) => form.email.endsWith(x))
		) {
			error.email = `invalid ${$organization.name} email`;
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'Requesting Code . . .';
		form.email_template = email_template.innerHTML.replace(/&amp;/g, '&');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/email/3`, {
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
			emit('ok', form.email);
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

	<IG
		name="New Email"
		icon="email"
		error={error.email}
		type="email"
		bind:value={form.email}
		placeholder="Email here"
	/>

	<Button primary on:click={validate}>
		Submit
		<Icon icon="send" />
	</Button>
</form>

<div bind:this={email_template} style="display: none;">
	<EmailTemplate />
</div>

<style>
	.error {
		margin: var(--sp2) 0;
	}
</style>
