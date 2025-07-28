<script>
	import { onMount } from 'svelte';
	import { notify, loading, token } from '$lib/store.svelte.js';

	import { IG, Dropdown } from '$lib/input';
	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';
	import { Card, Error } from '$lib/layout';

	let { card, active_card, update } = $props();

	let error = $state({});
	let form = $state({
		phone: card.phone,
		email: card.email,
		manager_card_key: card.manager_card_key,
		office_location_id: card.office_location_id
	});

	let emails = $state([]);

	let list = $state([{ key: 'none', value: -1 }]);
	if (card.org.address.length > 0) {
		for (const i in card.org.address) {
			list.push({ key: card.org.address[i].address, value: parseInt(i) });
		}
	}

	onMount(async () => {
		if (card.status == 'live') {
			let resp = await fetch(`${import.meta.env.VITE_BACKEND}/org/emails/${card.key}`);
			resp = await resp.json();
			if (resp.status == 200) {
				emails.push({
					key: 'none',
					value: null
				});
				for (const i of resp.emails) {
					emails.push({
						key: `${i.firstname} ${i.lastname}: ${i.email}`,
						value: i.key
					});
				}
			}
		}
	});

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
		<Error error={error.error} block --error-margin-top="0"></Error>

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
			{#if emails?.length > 0}
				<IG name="Manager's Email" error={error.manager_card_key}>
					{#snippet input(id)}
						<Dropdown list={emails} bind:value={form.manager_card_key} {id} wide></Dropdown>
					{/snippet}
				</IG>
			{/if}
			<IG name="Office Location" error={error.office_location_id}>
				{#snippet input(id)}
					<Dropdown {list} bind:value={form.office_location_id} {id} wide></Dropdown>
				{/snippet}
			</IG>
		{/if}

		<br />

		<Button onclick={validate}>
			Save
			<Icon icon="save" />
		</Button>
	</form>
</Card>

<style>
</style>
