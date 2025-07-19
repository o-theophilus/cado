<script>
	import { loading, token, notify } from '$lib/store.svelte.js';

	import Button from '$lib/button/button.svelte';
	import IG from '$lib/input_group.svelte';
	import Icon from '$lib/icon.svelte';
	import Code from '$lib/input_code.svelte';
	import Note from '$lib/note.svelte';

	let { entity, _type, form, active_card, update } = $props();
	let error = $state({});

	const validate = () => {
		error = {};

		if (!form.code) {
			error.code = 'this field is required';
		} else if (form.code.length != 6) {
			error.code = 'invalid verification code';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Verifying Code / Saving Email . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/email/2/${_type}/${entity.key}`, {
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
			form.email = null;
			form.state = 0;

			active_card.close();
			update(resp[_type]);
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

	<IG name="Verification Code" error={error.code}>
		{#snippet input()}
			<Code bind:value={form.code} />
		{/snippet}
	</IG>

	<div class="line">
		<Button primary onclick={validate}>
			Submit
			<Icon icon="send" />
		</Button>

		<Button
			onclick={() => {
				form.state = 0;
			}}
		>
			Cancel
			<Icon icon="close" />
		</Button>
	</div>
</form>

<style>
	.line {
		display: flex;
		gap: var(--sp1);
	}

	.error {
		margin: var(--sp2) 0;
	}

	span {
		font-weight: 800;
	}
</style>
