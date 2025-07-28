<script>
	import { user, loading, token } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Row, FormNote } from '$lib/layout';
	import { IG } from '$lib/input';
	import { Icon } from '$lib/macro';
	import EmailTemplate from './email_template.svelte';

	let { form, error = $bindable(), status } = $props();
	let email_template;

	const validate = () => {
		error = {};

		if (!form.email) {
			error.email = 'this field is required';
		} else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
			error.email = 'Please enter a valid email';
		} else if (form.email == user.value.email) {
			error.email = 'please use a different email form your current email';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Requesting Verification Code . . .');
		form.email_template = email_template.innerHTML.replace(/&amp;/g, '&');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/email/3`, {
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
			status.value = 3;
		} else {
			error = resp;
		}
	};
</script>

<form onsubmit={(e) => e.preventDefault()} novalidate autocomplete="off">
	<FormNote>
		{#snippet title()}
			Enter your new email address and click the button below.
		{/snippet}
		{#snippet note()}
			A verification code will be sent to that address to confirm your ownership.
		{/snippet}
	</FormNote>

	<IG
		name="New Email"
		icon="email"
		error={error.email}
		type="email"
		bind:value={form.email}
		placeholder="Email here"
	/>

	<Row --row-gap="8px">
		<Button primary onclick={validate}>
			Request Code
			<Icon icon="send" />
		</Button>

		<Button
			onclick={() => {
				error = {};
				form.code_1 = null;
				form.code_2 = null;
				status.value = 0;
			}}
		>
			Cancel
			<Icon icon="close" />
		</Button>
	</Row>
</form>

<div bind:this={email_template} style="display: none;">
	<EmailTemplate />
</div>

<style>
</style>
