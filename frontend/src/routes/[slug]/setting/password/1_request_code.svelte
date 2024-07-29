<script>
	import { loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';
	import { createEventDispatcher } from 'svelte';

	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import EmailTemplate from './email_template.svelte';

	let emit = createEventDispatcher();
	let error = {};
	let email_template;

	const submit = async () => {
		$loading = 'Requesting Verification Code . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/password/1`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({
				email_template: email_template.innerHTML.replace(/&amp;/g, '&')
			})
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			emit('ok');
		} else {
			error = resp;
		}
	};
</script>

{#if error.error}
	<br />
	<div class="error">
		{error.error}
	</div>
{/if}

<div class="note">
	To change your password, please click the button below to request
	a verification code.
	<br />
	<br />
	This code will be sent to your current email address to confirm that you are the owner of this account.
</div>

<Button on:click={submit}>
	Request Code
	<Icon icon="send" />
</Button>

<div bind:this={email_template} style="display: none;">
	<EmailTemplate />
</div>

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
</style>
