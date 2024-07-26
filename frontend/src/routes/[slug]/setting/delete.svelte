<script>
	import { loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button/button.svelte';
	import IG from '$lib/input_group.svelte';
	import Icon from '$lib/icon.svelte';
	import ShowPassword from '../../account/password_show.svelte';
	import Card from '$lib/card.svelte';

	export let user;
	export let open;
	let form = {};
	let error = {};
	let show_password = false;

	const validate = () => {
		error = {};

		if (!form.password) {
			error.password = 'this field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'Deleting Account . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/${user.key}`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$token = resp.token;
			document.location = '/';
		} else {
			error = resp;
		}
	};
</script>

<Card {open} on:open>
	<svelte:fragment slot="title">Delete Account</svelte:fragment>

	<form on:submit|preventDefault novalidate autocomplete="off">
		<br />
		Are you sure you want to delete account?

		{#if error.error}
			<div class="error">
				{error.error}
			</div>
		{/if}

		<IG
			name="Password"
			icon="key"
			error={error.password}
			bind:value={form.password}
			type={show_password ? 'text' : 'password'}
			placeholder="Password here"
		>
			<svelte:fragment slot="right">
				<div class="right">
					<ShowPassword bind:show_password />
				</div>
			</svelte:fragment>
		</IG>

		<Button on:click={validate}>
			<Icon icon="delete" />
			Delete
		</Button>
	</form>
</Card>

<style>
	.error {
		margin: var(--sp2) 0;
	}
	.right {
		padding-right: var(--sp2);
	}
</style>
