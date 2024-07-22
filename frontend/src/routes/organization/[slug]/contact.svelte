<script>
	import { notification, loading, organization as org } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import IG from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import BRound from '$lib/button/round.svelte';
	import Icon from '$lib/icon.svelte';
	import Dropdown from '$lib/dropdown.svelte';
	import Card from '$lib/card.svelte';
	import Address from './contact.address.svelte';

	export let organization;
	export let open;
	let form = {
		...organization
	};

	let error = {};

	const validate = () => {
		error = {};

		if (!form.email) {
			error.email = 'this field is required';
		} else if (!/\S+@\S+\.\S+/.test(form.email)) {
			error.email = 'Please enter a valid email';
		} else if (
			$org.email_domains.length > 0 &&
			!$org.email_domains.some((x) => form.email.endsWith(x))
		) {
			error.email = `invalid ${$org.name} email`;
		}

		for (const i in form.address) {
			if (!form.address[i].name) {
				if (!error[i]) {
					error[i] = {};
				}
				error[i].name = 'this field is required';
			}
			if (!form.address[i].address) {
				if (!error[i]) {
					error[i] = {};
				}
				error[i].address = 'this field is required';
			}
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'Saving Post . . .';
		let resp = await fetch(
			`${import.meta.env.VITE_BACKEND}/organization/contact/${organization.key}`,
			{
				method: 'put',
				headers: {
					'Content-Type': 'application/json',
					Authorization: $token
				},
				body: JSON.stringify(form)
			}
		);
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			organization = resp.organization;
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

		<IG
			name="Email"
			icon="email"
			error={error.email}
			type="email"
			bind:value={form.email}
			placeholder="Email here"
		/>

		<IG
			name="Website"
			icon="language"
			error={error.website}
			type="text"
			bind:value={form.website}
			placeholder="Website here"
		/>

		<div class="line">
			<label>Address</label>
			<BRound
				icon="add"
				on:click={() => {
					form.address.push({
						name: '',
						address: '',
						url: ''
					});
					form = form;
				}}
			/>
		</div>

		{#each form.address as one, i}
			<Address
				bind:one
				{error}
				{i}
				on:remove={() => {
					form.address.splice(i, 1);
					form = form;
				}}
			/>
		{/each}

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

	.line {
		display: flex;
		align-items: center;
		justify-content: space-between;
	}
</style>
