<script>
	import { module, notification, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import IG from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';

	let form = {
		...$module.user
	};

	let error = {};

	const validate = () => {
		error = {};
		if (!form.firstname) {
			error.firstname = 'cannot be empty';
		}

		if (!form.lastname) {
			error.lastname = 'cannot be empty';
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
				message: 'Name Changed'
			};
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="ititle"> Edit Name </strong>
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
		icon="phone"
		error={error.phone}
		placeholder="Phone number here"
		type="tel"
		bind:value={form.phone}
	/>

	<IG
		name="Manager's Email"
		icon="email"
		error={error.manager_email}
		type="email"
		bind:value={form.manager_email}
		placeholder="Email here"
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

<style>
	form {
		padding: var(--sp3);
	}
	.error {
		margin: var(--sp2) 0;
	}
</style>
