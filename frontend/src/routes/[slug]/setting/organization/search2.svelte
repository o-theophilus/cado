<script>
	import { createEventDispatcher } from 'svelte';
	import { notification, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';

	let emit = createEventDispatcher();
	export let user;
	export let organization;

	let error = {};

	const submit = async () => {
		$loading = 'Sending Request . . .';
		let resp = await fetch(
			`${import.meta.env.VITE_BACKEND}/organization/join/${user.key}`,
			{
				method: 'post',
				headers: {
					'Content-Type': 'application/json',
					Authorization: $token
				},
				body: JSON.stringify({ key: organization.key })
			}
		);
		resp = await resp.json();
		console.log(resp);

		$loading = false;

		if (resp.status == 200) {
			emit('ok', resp.user);
			$notification = {
				message: 'Request Sent to Organization'
			};
		} else {
			error = resp;
		}
	};
</script>

<div class="note">
	<div class="title">
		<Icon icon="error" size="2" />
		Are you sure?
	</div>

	{organization.fullname}
</div>

<div class="line">
	<Button on:click={submit}>
		Submit
		<Icon icon="send" />
	</Button>
	<Button
		on:click={() => {
			emit('x');
		}}
	>
		Cancel
		<Icon icon="close" />
	</Button>
</div>

<style>
	.line {
		display: flex;
		gap: var(--sp1);
	}

	.note {
		padding: var(--sp2);
		margin: var(--sp2) 0;
		background-color: var(--bg2);

		font-size: 0.8rem;
		border-radius: var(--sp0);
	}

	.title {
		display: flex;
		align-items: center;
		gap: var(--sp2);

		margin-bottom: var(--sp2);
		fill: currentColor;
		color: var(--cl4);
		font-weight: 800;
	}
</style>
