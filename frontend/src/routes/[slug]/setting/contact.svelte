<script>
	import { notify, loading, token } from '$lib/store.svelte.js';

	import IG from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Card from '$lib/card.svelte';
	import Dropdown from '$lib/dropdown.svelte';

	let { card, active_card, update } = $props();

	let error = $state({});
	let form = $state({
		phone: card.phone,
		email: card.email,
		office_location_id: card.office_location_id
	});

	let list = [
		{
			key: 'none',
			value: 0
		}
	];
	if (card.org.address.length > 0) {
		for (let x = 0; x < card.org.address.length; x++) {
			list.push({
				key: card.org.address[x].address,
				value: x + 1
			});
		}
	}

	const validate = () => {
		error = {};

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Saving Contact . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/card/${card.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: token.value
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			update(resp.card);
			active_card.close();
			notify.open('Contact Saved');
		} else {
			error = resp;
		}
	};

	let name = 'contact';
</script>

<Card open={active_card.value == name} onopen={() => active_card.set(name)}>
	{#snippet title()}
		Contact
	{/snippet}

	<form onsubmit={(e) => e.preventDefault()} novalidate autocomplete="off">
		{#if error.error}
			<div class="error">
				{error.error}
			</div>
		{/if}

		<IG
			name="Phone Number"
			icon="call"
			error={error.phone}
			placeholder="Phone number here"
			type="tel"
			bind:value={form.phone}
		/>

		<IG
			name="Email"
			icon="email"
			error={error.email}
			type="email"
			bind:value={form.email}
			placeholder="Email here"
			disabled
		/>

		{#if card.status == 'live'}
			<IG name="Office Location" error={error.office_location_id}>
				{#snippet input(id)}
					<Dropdown
						{list}
						bind:value={form.office_location_id}
						default_value={list.length >= card.office_location_id - 1 ? card.office_location_id : 0}
						{id}
						wide
					></Dropdown>
				{/snippet}
			</IG>
		{/if}

		<br />

		<Button onclick={validate}>
			Submit
			<Icon icon="send" />
		</Button>
	</form>
</Card>

<style>
	.error {
		margin: var(--sp2) 0;
	}
</style>
