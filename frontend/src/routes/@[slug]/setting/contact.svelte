<script>
	import { notify, loading, user as _user, token } from '$lib/store.svelte.js';

	import IG from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Card from '$lib/card.svelte';
	import Address from './contact.address.svelte';

	let { org, active_card } = $props();

	let error = $state({});
	let form = $state({
		phone: org.phone,
		website: org.website,
		address: org.address
	});

	const validate = () => {
		console.log('here');

		error = {};
		for (const i in org.address) {
			if (!org.address[i].address) {
				error[i] = 'this field is required';
			}
		}

		if (form.phone) {
			form.phone = form.phone.replace(/\s+/g, '');
			if (!/^\+?\d+$/.test(form.phone)) {
				error.phone = "Invalid phone number. Phone number may start with a '+' followed by digits";
			}
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Saving Contact . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/org/${org.key}`, {
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
			name="Website"
			icon="language"
			error={error.website}
			placeholder="Website here"
			type="text"
			bind:value={form.website}
		/>

		<Address bind:value={form.address} {error}></Address>

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
