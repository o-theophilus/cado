<script>
	import { loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';
	import { createEventDispatcher } from 'svelte';

	import IG from '$lib/input_group.svelte';
	import Icon from '$lib/icon.svelte';
	import Button from '$lib/button/button.svelte';
	import EmailTemplate from './email_template.svelte';

	let form = {};
	let error = {};
	let email_template;
	let emit = createEventDispatcher();

	const validate = () => {
		error = {};

		if (!form.name) {
			error.name = 'this field is required';
		}

		if (!form.email) {
			error.email = 'this field is required';
		} else if (!/\S+@\S+\.\S+/.test(form.email)) {
			error.email = 'invalid email';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'Requesting Verification Code . . .';
		form.email_template = email_template.innerHTML.replace(/&amp;/g, '&');

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/organization/add/1`, {
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
			emit('ok', form);
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="ititle"> Add Organization </strong>

	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

	<IG
		name="Name"
		icon="corporate_fare"
		error={error.name}
		type="text"
		bind:value={form.name}
		placeholder="Name here"
	/>

	<IG
		name="Email"
		icon="email"
		error={error.email}
		type="email"
		bind:value={form.email}
		placeholder="Email here"
	/>

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

<div bind:this={email_template} style="display: none;">
	<EmailTemplate />
</div>

<style>
	.error {
		margin: var(--sp2) 0;
	}

	.line {
		display: flex;
		gap: var(--sp1);
	}
</style>
