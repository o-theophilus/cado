<script>
	import { loading, token } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { IG } from '$lib/input';
	import Icon from '$lib/icon.svelte';
	import Note from '$lib/note.svelte';

	let { org, form, status, error = $bindable() } = $props();

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
			status.value = 1;
		} else {
			error = resp;
		}
	};
</script>

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

<style>
</style>
