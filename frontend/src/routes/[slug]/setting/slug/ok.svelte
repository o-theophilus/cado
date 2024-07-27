<script>
	import { createEventDispatcher } from 'svelte';
	import { loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Icon from '$lib/icon.svelte';
	import Button from '$lib/button/button.svelte';
	import ShowPassword from '../../../account/password_show.svelte';
	import IG from '$lib/input_group.svelte';

	let emit = createEventDispatcher();
	export let user_key;
	export let slug;
	let form = {
		slug
	};
	let error = {};
	let show_password = false;

	const validate = async () => {
		error = {};

		if (!form.password) {
			error.password = 'cannot be empty';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'Saving Username . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/slug/${user_key}`, {
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
			emit('ok', false);
		} else if (resp.slug) {
			emit('slug', resp.slug);
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
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

	<div class="line">
		<Button on:click={validate}>
			Submit
			<Icon icon="send" />
		</Button>
		<Button
			on:click={() => {
				emit('ok', true);
			}}
		>
			Cancel
			<Icon icon="close" />
		</Button>
	</div>
</form>

<style>
	.error {
		margin: var(--sp2) 0;
	}

	.right {
		padding-right: var(--sp2);
	}
	.line {
		display: flex;
		gap: var(--sp1);
	}
</style>
