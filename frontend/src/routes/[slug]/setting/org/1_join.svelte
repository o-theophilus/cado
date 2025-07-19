<script>
	import { token, notify, loading } from '$lib/store.svelte.js';

	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Note from '$lib/note.svelte';
	import NoteOrg from '$lib/note.org.svelte';

	let { card, status, update } = $props();
	let error = $state({});

	const submit = async () => {
		loading.open('Sending Request . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/org/card/join/${card.key}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: token.value
			},
			body: JSON.stringify({
				org_key: status.org.key
			})
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			status.value = 2;
			notify.open('Request Sent to Organization');
			update(resp.card);
		} else {
			error = resp;
		}
	};
</script>

<Note>
	{#snippet title()}
		Are you sure you want to link this card to the Organization below?
	{/snippet}
	{#snippet note()}
		<NoteOrg org={status.org}></NoteOrg>
	{/snippet}
</Note>

{#if error.error}
	<div class="error">
		{error.error}
	</div>
{/if}

<div class="line">
	<Button onclick={submit}>
		Link
		<Icon icon="send" />
	</Button>
	<Button
		onclick={() => {
			status.value = 0;
		}}
	>
		Cancel
		<Icon icon="close" />
	</Button>
</div>

<style>
	.line {
		display: flex;
		gap: var(--sp1);
	}

	.error {
		margin: var(--sp2) 0;
		font-size: small;
	}
</style>
