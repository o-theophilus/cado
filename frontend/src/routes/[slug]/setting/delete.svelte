<script>
	import { goto } from '$app/navigation';
	import { loading, token, notify } from '$lib/store.svelte.js';

	import Button from '$lib/button/button.svelte';
	import IG from '$lib/input_group.svelte';
	import Icon from '$lib/icon.svelte';
	import ShowPassword from '../../account/password_show.svelte';
	import Card from '$lib/card.svelte';

	let { entity, _type, active_card } = $props();

	let form = $state({});
	let error = $state({});
	let show_password = $state(false);
	let status = $state(0);

	const validate = () => {
		error = {};

		if (!form.password) {
			error.password = 'this field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Deleting Account . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/delete/${_type}/${entity.key}`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: token.value
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			notify.open(`${_type == 'org' ? 'organization' : _type} Deleted`);
			goto(`/profile/${_type}`);
		} else {
			error = resp;
		}
	};

	let name = 'delete';
</script>

<Card open={active_card.value == name} onopen={() => active_card.set(name)}>
	{#snippet title()}
		<!-- TODO: Capitalize first letter -->
		Delete {_type == 'org' ? 'organization' : _type}
	{/snippet}

	{#if status == 0}
		<div class="note">
			<div class="title">
				<Icon icon="error" size="2" />
				Warning:
			</div>

			<span>
				Deleting
				{#if entity.key == entity.key}
					your
				{:else}
					this
				{/if}
				account will permanently remove all {#if entity.key == entity.key}
					your
				{:else}
					this
				{/if} data associated with it and cannot be undone.
				<br />
				<br />
				Are you sure you want to continue?
			</span>
		</div>
		<Button
			onclick={() => {
				status = 1;
			}}
		>
			<Icon icon="send" />
			Continue
		</Button>
	{:else if status == 1}
		<form onsubmit={(e) => e.preventDefault()} novalidate autocomplete="off">
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
					To proceed with deleting
					{#if entity.key == entity.key}
						your
					{:else}
						this
					{/if}
					account, please enter your password below to confirm your identity.
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
				{#snippet right()}
					<div class="right">
						<ShowPassword bind:show_password />
					</div>
				{/snippet}
			</IG>

			<div class="line">
				<Button onclick={validate}>
					<Icon icon="delete" />
					Delete
				</Button>

				<Button
					onclick={() => {
						status = 0;
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
