<script>
	import { notify, loading } from '$lib/store.svelte.js';
	import { token } from '$lib/store.svelte.js';

	import IG from '$lib/input_group.svelte';
	import { Button } from '$lib/button';
	import Icon from '$lib/icon.svelte';
	import Card from '$lib/card.svelte';

	let { user, active_card, update } = $props();

	let error = $state({});
	let form = $state({
		phone: user.value.phone
	});

	const validate = () => {
		error = {};

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Saving Contact . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user`, {
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
			update(resp.user);
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
			bind:value={user.value.email}
			placeholder="Email here"
			disabled
		/>

		<br />

		<Button onclick={validate}>
			Save
			<Icon icon="save" />
		</Button>
	</form>
</Card>

<style>
	.error {
		margin: var(--sp2) 0;
	}
</style>
