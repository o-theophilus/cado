<script>
	import { notification, loading, organization } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import IG from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Dropdown from '$lib/dropdown.svelte';
	import Card from './card.svelte';

	export let user;
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
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/contact/${user.key}`, {
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
			$notification = {
				message: 'Details Saved'
			};
		} else {
			error = resp;
		}
	};
</script>

<Card>
	<svelte:fragment slot="title">Contact</svelte:fragment>

	<form on:submit|preventDefault novalidate autocomplete="off">
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

		<label for="location">Office Location</label>
		<div class="dropdown">
			<Dropdown
				list={$organization.address.map((a) => a.name)}
				id="location"
				icon="location_on"
				wide
				default_value={form.office_location}
				on:change={(e) => {
					form.office_location = e.target.value;
				}}
			/>

			<div>
				{#each $organization.address as a}
					{#if a.name == form.office_location}
						{a.address}
					{/if}
				{/each}
			</div>
		</div>

		<br />

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
	label {
		font-size: 0.8em;
	}
	.dropdown {
		margin-top: var(--sp1);
	}
	.dropdown div {
		padding: var(--sp2);
		font-size: 0.8rem;
		background-color: var(--bg2);

		border-radius: var(--sp0);
	}
</style>
