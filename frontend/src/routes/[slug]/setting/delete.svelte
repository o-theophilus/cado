<script>
	import { goto } from '$app/navigation';
	import { loading, token, notify } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Row } from '$lib/layout';
	import IG from '$lib/input_group.svelte';
	import Icon from '$lib/icon.svelte';
	import ShowPassword from '$lib/auth/password_show.svelte';
	import Card from '$lib/card.svelte';
	import Note from '$lib/note.svelte';

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

	let _type_name = $state('org' ? 'organization' : _type);
	let name = 'delete';
</script>

<Card open={active_card.value == name} onopen={() => active_card.set(name)}>
	{#snippet title()}
		Delete {_type_name.charAt(0).toUpperCase() + _type_name.slice(1)}
	{/snippet}

	{_type}

	{#if status == 0}
		<Note status="400">
			{#snippet title()}
				Warning:
			{/snippet}
			{#snippet note()}
				Deleting this {_type == 'org' ? 'organization' : _type} is irreversible and will permanently
				erase all associated data.
				<br />
				This action cannot be undone.
				<br />
				<br />
				Are you sure you want to continue?
			{/snippet}
		</Note>

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

			<Note status="400">
				{#snippet title()}
					Warning:
				{/snippet}
				{#snippet note()}
					To proceed with deleting this card, please enter your password below to confirm your
					identity.
				{/snippet}
			</Note>

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

			<Row --row-gap="8px">
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
			</Row>
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
</style>
