<script>
	import { token, notify, loading } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Row, FormNote } from '$lib/layout';
	import { Icon } from '$lib/macro';
	import NoteOrg from './_org.svelte';

	let { card, status, error = $bindable(), update, active_card } = $props();

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

<FormNote status="400">
	{#snippet title()}
		Are you sure you want to
		{#if card.status == 'pending'}
			cancel your request to become a member of
		{:else if card.status == 'live'}
			unlink this card from
		{/if}
		this organization?
	{/snippet}
	{#snippet note()}
		<NoteOrg org={card.org}></NoteOrg>
	{/snippet}
</FormNote>

<Row --row-gap="8px">
	<Button onclick={submit}>
		Cancel Request
		<Icon icon="send" />
	</Button>
	<Button
		onclick={() => {
			error = {};
			status.value = 2;
		}}
	>
		back
		<Icon icon="close" />
	</Button>
</Row>

<style>
</style>
