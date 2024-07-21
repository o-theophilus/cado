<script>
	import { notification, loading, organization } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import IG from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Card from './card.svelte';

	export let user;
	export let open;
	let form = {
		...user
	};
	if (form.office_location == null) {
		form.office_location = $organization.address[0].name;
	}

	let error = {};

	const validate = () => {
		error = {};

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'Saving Post . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/organization/${user.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			user = resp.user;
			open = false;
			$notification = {
				message: 'Details Saved'
			};
		} else {
			error = resp;
		}
	};
</script>

<Card {open} on:open>
	<svelte:fragment slot="title">Organization</svelte:fragment>

	<form on:submit|preventDefault novalidate autocomplete="off">
		{#if error.error}
			<div class="error">
				{error.error}
			</div>
		{/if}

		<IG
			name="Role"
			icon="work"
			error={error.role}
			placeholder="Role here"
			type="text"
			bind:value={form.role}
		/>

		<IG
			name="Manager's Email"
			icon="email"
			error={error.manager_email}
			type="email"
			bind:value={form.manager_email}
			placeholder="Email here"
		/>

		<Button on:click={validate}>
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
