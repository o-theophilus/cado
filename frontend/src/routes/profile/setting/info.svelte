<script>
	import { notify, loading } from '$lib/store.svelte.js';
	import { token } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import Icon from '$lib/icon.svelte';
	import { Card, Error } from '$lib/layout';

	let { user, active_card, update } = $props();

	let form = $state({
		firstname: user.value.firstname,
		lastname: user.value.lastname
	});
	let error = $state({});

	const validate = () => {
		error = {};
		if (!form.firstname) {
			error.firstname = 'this field is required';
		}

		if (!form.lastname) {
			error.lastname = 'this field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Saving Information . . .');
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
			notify.open('Information Saved');
		} else {
			error = resp;
		}
	};

	let name = 'personal';
</script>

<Card open={active_card.value == name} onopen={() => active_card.set(name)}>
	{#snippet title()}
		Information
	{/snippet}

	<form onsubmit={(e) => e.preventDefault()} novalidate autocomplete="off">
		<Error error={error.error} block --error-margin-top="0"></Error>

		<IG
			name="Firstname"
			icon="person"
			error={error.firstname}
			placeholder="Firstname here"
			type="text"
			bind:value={form.firstname}
			required
		/>

		<IG
			name="Lastname"
			icon="person"
			error={error.lastname}
			placeholder="Lastname here"
			type="text"
			bind:value={form.lastname}
			required
		/>

		<Button onclick={validate}>
			Save
			<Icon icon="save" />
		</Button>
	</form>
</Card>

<style>
</style>
