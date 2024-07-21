<script>
	import { notification, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import IG from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Card from './card.svelte';

	export let organization;
	export let open;
	let form = {
		...organization
	};

	let error = {};

	const validate = () => {
		error = {};

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'Saving Post . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/organization/org/${organization.key}`, {
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
	<svelte:fragment slot="title">Organization</svelte:fragment>

	<form on:submit|preventDefault novalidate autocomplete="off">
		{#if error.error}
			<div class="error">
				{error.error}
			</div>
		{/if}

		<IG
			name="Name"
			icon="work"
			error={error.name}
			placeholder="Name here"
			type="text"
			bind:value={form.name}
		/>

		<IG
			name="Fullname"
			icon="work"
			error={error.fullname}
			placeholder="Fullname here"
			type="text"
			bind:value={form.fullname}
		/>

		<IG
			name="Slogan"
			icon="work"
			error={error.slogan}
			placeholder="Slogan here"
			type="text"
			bind:value={form.slogan}
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
