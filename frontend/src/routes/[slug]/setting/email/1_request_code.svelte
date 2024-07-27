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
		$loading = 'Requesting Code . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/email/1`, {
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
<br />

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
</style>
