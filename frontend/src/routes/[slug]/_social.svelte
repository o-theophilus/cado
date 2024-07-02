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

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'Saving Post . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/links/${$module.user.key}`, {
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
	<strong class="ititle"> Edit Social Links </strong>
	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

	<IG
		type="text"
		icon="person"
		placeholder="Whatsapp here"
		error={error.whatsapp}
		bind:value={form.whatsapp}
	/>

	<IG
		type="text"
		icon="person"
		placeholder="Linkedin here"
		error={error.linkedin}
		bind:value={form.linkedin}
	/>

	<IG
		type="text"
		icon="person"
		placeholder="Twitter here"
		error={error.twitter}
		bind:value={form.twitter}
	/>

	<IG
		type="text"
		icon="person"
		placeholder="Facebook here"
		error={error.facebook}
		bind:value={form.facebook}
	/>

	<IG
		type="text"
		icon="person"
		placeholder="Instagram here"
		error={error.instagram}
		bind:value={form.instagram}
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
