<script>
	import { token, notify, loading } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Row, Error, FormNote } from '$lib/layout';
	import { Icon } from '$lib/macro';
	import NoteOrg from './_org.svelte';

	let { card, status, error = $bindable(), update } = $props();

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

<Error error={error.error} --error-margin-bottom="16px"></Error>

<FormNote>
	{#snippet title()}
		Are you sure you want to link this card to the Organization below?
	{/snippet}
	{#snippet note()}
		<NoteOrg org={status.org}></NoteOrg>
	{/snippet}
</FormNote>

<Row --row-gap="8px">
	<Button onclick={submit}>
		Link
		<Icon icon="send" />
	</Button>
	<Button
		onclick={() => {
			error = {};
			status.value = 0;
		}}
	>
		Cancel
		<Icon icon="close" />
	</Button>
</Row>

<style>
</style>
