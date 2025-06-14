<script>
	import { goto } from '$app/navigation';
	import { loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button/button.svelte';
	import IG from '$lib/input_group.svelte';
	import Icon from '$lib/icon.svelte';
	import ShowPassword from '../../account/password_show.svelte';
	import Card from '$lib/card.svelte';

	export let open;
	export let organization;
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
		$loading = 'Deleting Organization . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/organization/${organization.key}`, {
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
			// $organization = resp.organization;
			goto('/');
		} else {
			error = resp;
		}
	};

	let state = 0;
</script>

<Card {open} on:open>
	<svelte:fragment slot="title">Delete Organization</svelte:fragment>

	{#if state == 0}
		<div class="note">
			<div class="title">
				<Icon icon="error" size="2" />
				Warning:
			</div>

			<span>
				Deleting organization's account will permanently remove all data associated with it and
				cannot be undone.
				<br />
				<br />
				Are you sure you want to continue?
			</span>
		</div>
		<Button
			on:click={() => {
				state = 1;
			}}
		>
			<Icon icon="send" />
			Continue
		</Button>
	{:else if state == 1}
		<form on:submit|preventDefault novalidate autocomplete="off">
			{#if error.error}
				<div class="error">
					{error.error}
				</div>
			{/if}

			<div class="note">
				<div class="title">
					<Icon icon="error" size="2" />
					Warning:
				</div>

				<span>
					To proceed with deleting organization's account, please enter your password below to
					confirm your identity.
				</span>
			</div>

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
					<Icon icon="delete" />
					Delete
				</Button>

				<Button
					on:click={() => {
						state = 0;
					}}
				>
					<Icon icon="arrow_back" />
					Back
				</Button>
			</div>
		</form>
	{/if}
</Card>

<style>
	.error {
		margin: var(--sp2) 0;
	}
	.right {
		padding-right: var(--sp2);
	}

	.note {
		padding: var(--sp2);
		margin: var(--sp2) 0;
		background-color: var(--bg2);

		border-radius: var(--sp0);
	}

	.note span {
		font-size: 0.8rem;
	}

	.title {
		display: flex;
		align-items: center;
		gap: var(--sp2);

		margin-bottom: var(--sp2);
		fill: currentColor;
		color: var(--cl2);
		font-weight: 800;
	}

	.line {
		display: flex;
		gap: var(--sp1);
	}
</style>
