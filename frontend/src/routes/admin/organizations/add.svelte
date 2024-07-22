<script>
	import { goto } from '$app/navigation';
	import { module, loading, notification } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import IG from '$lib/input_group.svelte';
	import Icon from '$lib/icon.svelte';
	import Button from '$lib/button/button.svelte';

	let form = {};
	let error = {};

	const validate = () => {
		error = {};

		if (!form.name) {
			error.name = 'this field is required';
		}

		if (!form.email) {
			error.email = 'this field is required';
		} else if (!/\S+@\S+\.\S+/.test(form.email)) {
			error.email = 'invalid email';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'Creating Organization . . .';

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/organization`, {
			method: 'post',
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
				message: 'Organization Created'
			};
			goto(`/organization/${resp.organization.slug}`);
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="ititle"> Add Organization </strong>

	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

	<IG
		name="Name"
		icon="email"
		error={error.name}
		type="text"
		bind:value={form.name}
		placeholder="Name here"
	/>

	<IG
		name="Email"
		icon="email"
		error={error.email}
		type="email"
		bind:value={form.email}
		placeholder="Email here"
	/>

	<Button primary on:click={validate}
		>Submit
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
