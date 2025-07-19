<script>
	import { token, notify, loading } from '$lib/store.svelte.js';

	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Note from '$lib/note.svelte';
	import NoteOrg from '$lib/note.org.svelte';

	let { card, status, update, active_card } = $props();

	let error = $state({});

	const submit = async () => {
		error = {};
		loading.open('Sending Request . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/org/card/cancel/${card.key}`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: token.value
			}
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			status.value = 0;
			notify.open('Request Canceled');
			update(resp.card);
			active_card.close();
		} else {
			error = resp;
		}
	};
</script>

<Note status="400">
	{#snippet title()}
		Are you sure you want to cancel your request to be a member of this organization?
	{/snippet}
	{#snippet note()}
		<NoteOrg org={card.org}></NoteOrg>
	{/snippet}
</Note>

{#if error.error}
	<div class="error">
		{error.error}
	</div>
{/if}

<div class="line">
	<Button onclick={submit}>
		Cancel Request
		<Icon icon="send" />
	</Button>
	<Button
		onclick={() => {
			status.value = 2;
		}}
	>
		back
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
