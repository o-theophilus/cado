<script>
	import { notification, loading, organization } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import IG from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
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
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/personal/${user.key}`, {
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
			window.history.replaceState(history.state, '', `/${resp.user.slug}/setting`);
		} else {
			error = resp;
		}
	};
</script>

<Card>
	<svelte:fragment slot="title">Personal</svelte:fragment>

	<form on:submit|preventDefault novalidate autocomplete="off">
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
			name="About Me"
			error={error.about_me}
			type="textarea"
			placeholder="About me here"
			bind:value={form.about_me}
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
