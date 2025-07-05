<script>
	import { token, notify, loading } from '$lib/store.svelte.js';

	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';

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

<div class="note">
	<div class="title">
		<Icon icon="error" size="2" />
		Are you sure you want to cancel request?
	</div>

	{card.org.fullname}
</div>

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

	.note {
		padding: var(--sp2);
		margin: var(--sp2) 0;
		background-color: var(--bg2);

		font-size: 0.8rem;
		border-radius: var(--sp0);
	}

	.title {
		display: flex;
		align-items: center;
		gap: var(--sp2);

		margin-bottom: var(--sp2);
		fill: currentColor;
		color: var(--cl4);
		font-weight: 800;
	}

	.error {
		margin: var(--sp2) 0;
		font-size: small;
	}
</style>
