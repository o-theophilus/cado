<script>
	import { createEventDispatcher } from 'svelte';
	import { notification, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import IG from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Card from '$lib/card.svelte';

	let emit = createEventDispatcher();
	export let user;
	export let open;
	let form = {
		user
	};

	let error = {};

	const validate = () => {
		error = {};

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'Saving Links . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/social/${user.key}`, {
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
				message: 'Links Saved'
			};
		} else {
			error = resp;
		}
	};
</script>

<Card {open} on:open>
	<svelte:fragment slot="title">Social Media Links</svelte:fragment>

	<form on:submit|preventDefault novalidate autocomplete="off">
		{#if error.error}
			<div class="error">
				{error.error}
			</div>
		{/if}

		<IG
			type="text"
			icon="whatsapp"
			icon_size="1"
			placeholder="Whatsapp number"
			error={error.whatsapp}
			bind:value={form.whatsapp}
		/>

		<IG
			type="text"
			icon="linkedin"
			icon_size="1"
			placeholder="Linkedin profile url"
			error={error.linkedin}
			bind:value={form.linkedin}
		/>

		<IG
			type="text"
			icon="twitter"
			icon_size="1"
			placeholder="Twitter profile url"
			error={error.twitter}
			bind:value={form.twitter}
		/>

		<IG
			type="text"
			icon="facebook"
			icon_size="1"
			placeholder="Facebook profile url"
			error={error.facebook}
			bind:value={form.facebook}
		/>

		<IG
			type="text"
			icon="instagram"
			icon_size="1"
			placeholder="Instagram profile url"
			error={error.instagram}
			bind:value={form.instagram}
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
