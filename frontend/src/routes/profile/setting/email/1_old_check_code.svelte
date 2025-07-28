<script>
	import { loading, user, token } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Row, FormNote } from '$lib/layout';
	import { IG } from '$lib/input';
	import { Icon } from '$lib/macro';

	let { form, error = $bindable(), status } = $props();

	const validate = () => {
		error = {};

		if (!form.code_1) {
			error.code_1 = 'this field is required';
		} else if (form.code_1.length != 6) {
			error.code_1 = 'invalid verification code';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Verifying Code . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/email/2`, {
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
			status.value = 2;
		} else {
			error = resp;
		}
	};
</script>

<form onsubmit={(e) => e.preventDefault()} novalidate autocomplete="off">
	<FormNote>
		{#snippet note()}
			Verification Code has been sent to:

			<span>
				{user.value.email}
			</span>

			.
		{/snippet}
	</FormNote>

	<IG name="Verification Code" bind:value={form.code_1} type="code" error={error.code_1}></IG>

	<Row --row-gap="8px">
		<Button primary onclick={validate}>
			Submit
			<Icon icon="send" />
		</Button>

		<Button
			onclick={() => {
				error = {};
				form.code_1 = null;
				form.code_2 = null;
				status.value = 0;
			}}
		>
			Cancel
			<Icon icon="close" />
		</Button>
	</Row>
</form>

<style>
	span {
		font-weight: 800;
	}
</style>
