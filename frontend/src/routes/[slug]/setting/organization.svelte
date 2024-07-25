<script>
	import { createEventDispatcher } from 'svelte';
	import { notification, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';
	import { onMount } from 'svelte';

	import IG from '$lib/input_group.svelte';
	import Dropdown from '$lib/dropdown.svelte';
	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Card from '$lib/card.svelte';

	let emit = createEventDispatcher();
	export let user;
	export let open;
	let orgs = [];
	let form = {
		...user
	};

	let error = {};

	const validate = () => {
		error = {};

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'Saving Organization . . .';
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
			emit('open', false);
			$notification = {
				message: 'Organization Saved'
			};
		} else {
			error = resp;
		}
	};

	onMount(async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/organizations/2`);
		resp = await resp.json();
		if (resp.status == 200) {
			orgs = resp.organizations;
			orgs.unshift({
				key: 'None',
				value: ''
			});
		}
	});
</script>

<Card {open} on:open>
	<svelte:fragment slot="title">Organization</svelte:fragment>

	<form on:submit|preventDefault novalidate autocomplete="off">
		{#if error.error}
			<div class="error">
				{error.error}
			</div>
		{/if}

		<!-- <IG name="Organization" icon="corporate_fare" error={error.role}>
			<Dropdown
				list={orgs}
				default_value={user.organization_key}
				wide
				on:change={(e) => {
					form.organization_key = e.target.value;
				}}
			/>
		</IG> -->

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
