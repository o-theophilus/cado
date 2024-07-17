<script>
	import { module, notification, loading, organization } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import IG from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Dropdown from '$lib/dropdown.svelte';

	let form = {
		...$module.user
	};
	if (form.office_location == null) {
		form.office_location = $organization.address[0].name;
	}

	let error = {};

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
		$loading = 'Saving Post . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/details/${$module.user.key}`, {
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
			window.history.replaceState(history.state, '', `/${resp.user.slug}`);
			$module.update(resp.user);
			$module = null;
			$notification = {
				message: 'Details Saved'
			};
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="ititle"> Edit Information </strong>
	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

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

	<IG
		name="Role"
		icon="work"
		error={error.role}
		placeholder="Role here"
		type="text"
		bind:value={form.role}
	/>

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

	<IG
		name="About Me"
		error={error.about_me}
		type="textarea"
		placeholder="About me here"
		bind:value={form.about_me}
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

<style>
	form {
		padding: var(--sp3);
	}
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
