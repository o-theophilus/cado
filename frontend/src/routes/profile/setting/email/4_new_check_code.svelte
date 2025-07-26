<script>
	import { loading, token, notify } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Row } from '$lib/layout';
	import IG from '$lib/input_group.svelte';
	import Icon from '$lib/icon.svelte';
	import Code from '$lib/input_code.svelte';
	import Note from '$lib/note.svelte';

	let { form, active_card, update } = $props();
	let error = $state({});

	const validate = () => {
		error = {};

		if (!form.code_2) {
			error.code_2 = 'this field is required';
		} else if (form.code_2.length != 6) {
			error.code_2 = 'invalid verification code';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Verifying Code / Saving Email . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/email/4`, {
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
			update(resp.user);

			form.state = 0;
			form.code_1 = null;
			form.code_2 = null;

			active_card.close();
			notify.open('Email changed');
		} else {
			error = resp;
		}
	};
</script>

<form onsubmit={(e) => e.preventDefault()} novalidate autocomplete="off">
	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

	<Note>
		{#snippet note()}
			Verification Code has been sent to:
			<span>
				{form.email}
			</span>
			.
		{/snippet}
	</Note>

	<IG name="Verification Code" error={error.code_2}>
		{#snippet input()}
			<Code bind:value={form.code_2} />
		{/snippet}
	</IG>

	<Row --row-gap="8px">
		<Button primary onclick={validate}>
			Submit
			<Icon icon="send" />
		</Button>

		<Button
			onclick={() => {
				form.state = 0;
				form.code_1 = null;
				form.code_2 = null;
			}}
		>
			Cancel
			<Icon icon="close" />
		</Button>
	</Row>
</form>

<style>
	.error {
		margin: var(--sp2) 0;
	}

	span {
		font-weight: 800;
	}
</style>
