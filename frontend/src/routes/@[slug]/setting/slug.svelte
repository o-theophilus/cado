<script>
	import { loading, token, notify } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Row } from '$lib/layout';
	import IG from '$lib/input_group.svelte';
	import Icon from '$lib/icon.svelte';
	import ShowPassword from '$lib/auth/password_show.svelte';
	import Card from '$lib/card.svelte';
	import Note from '$lib/note.svelte';

	let { org, active_card, update } = $props();

	let form = $state({});
	let error = $state({});
	let show_password = $state(false);
	let status = $state(0);

	const validate1 = async () => {
		error = {};

		if (!form.slug) {
			error.slug = 'this field is required';
		} else if (form.slug == org.slug) {
			error.slug = 'no change';
		}

		Object.keys(error).length === 0 && submit1();
	};

	const submit1 = async () => {
		loading.open('Checking ID . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/org/slug/1/${org.key}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: token.value
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			status = 1;
		} else {
			error = resp;
		}
	};

	const validate2 = () => {
		error = {};

		if (!form.password) {
			error.password = 'this field is required';
		}

		Object.keys(error).length === 0 && submit2();
	};

	const submit2 = async () => {
		loading.open('Saving ID . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/org/slug/2/${org.key}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: token.value
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			status = 0;
			form = {};

			active_card.close();
			update(resp.org);
			notify.open('ID Changed');
			window.history.replaceState(history.state, '', `/@${org.slug}/setting`);
		} else {
			error = resp;

			if (error.slug) {
				status = 0;
			}
		}
	};

	let name = 'slug';
</script>

<Card open={active_card.value == name} onopen={() => active_card.set(name)}>
	{#snippet title()}
		Change ID
	{/snippet}

	<form onsubmit={(e) => e.preventDefault()} novalidate autocomplete="off">
		{#if error.error}
			<div class="error">
				{error.error}
			</div>
		{/if}

		{#if status == 0}
			<Note status="201">
				{#snippet title()}
					Changing your organization's ID will update all associated links.
				{/snippet}
			</Note>

			<IG
				name="Organization ID"
				icon="link"
				error={error.slug}
				bind:value={form.slug}
				type="text"
				placeholder="Organization ID here"
			/>

			<Button onclick={validate1}
				>Submit
				<Icon icon="send" />
			</Button>
		{:else if status == 1}
			<Note status="201">
				{#snippet title()}
					Changing your organization's ID will update all associated links.
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
				<Button onclick={validate2}>
					<Icon icon="send" />
					Confirm
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
		{/if}
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
