<script>
	import { loading, token } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import Icon from '$lib/icon.svelte';
	import EmailTemplate from './email_template.svelte';
	import Note from '$lib/note.svelte';

	let email_template;
	let { error = $bindable(), status } = $props();

	const submit = async () => {
		error = {};
		loading.open('Requesting Verification Code . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/email/1`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: token.value
			},
			body: JSON.stringify({
				email_template: email_template.innerHTML.replace(/&amp;/g, '&')
			})
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			status.value = 1;
		} else {
			error = resp;
		}
	};
</script>

<Note>
	{#snippet title()}
		To change the email address associated with this account, please click the button below to
		request a verification code.
	{/snippet}
	{#snippet note()}
		This code will be sent to your current email address to confirm that you are the owner of this
		account.
	{/snippet}
</Note>

<Button onclick={submit}>
	Request Code
	<Icon icon="send" />
</Button>

<div bind:this={email_template} style="display: none;">
	<EmailTemplate />
</div>

<style>
</style>
