<script>
	import { loading, token } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import IG from '$lib/input_group.svelte';
	import Icon from '$lib/icon.svelte';
	import EmailTemplate from './email_template.svelte';
	import Note from '$lib/note.svelte';

	let { entity, _type, form } = $props();
	let error = $state({});
	let email_template;

	const validate = () => {
		error = {};

		if (!form.email) {
			error.email = 'this field is required';
		} else if (!/\S+@\S+\.\S+/.test(form.email)) {
			// TODO: match the regex to align with that of email_domain
			error.email = 'Please enter a valid email';
		} else if (form.email == entity.email) {
			error.email = 'please use a different email form your current email';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Requesting Verification Code . . .');
		form.email_template = email_template.innerHTML.replace(/&amp;/g, '&');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/email/1/${_type}/${entity.key}`, {
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
			form.state = 1;
		} else {
			error = resp;
		}
	};
</script>

<form onsubmit={(e) => e.preventDefault()} novalidate autocomplete="off">
	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

	<Note>
		{#snippet title()}
			To change the email address associated with this {_type == 'org' ? 'organization' : _type},
			enter a new email address and click the button below.
		{/snippet}
		{#snippet note()}
			A verification code will be sent to that address to confirm your ownership.
		{/snippet}
	</Note>

	<IG
		name="New Email"
		icon="email"
		error={error.email}
		type="email"
		bind:value={form.email}
		placeholder="Email here"
	/>

	<Button onclick={validate}>
		Request Code
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
