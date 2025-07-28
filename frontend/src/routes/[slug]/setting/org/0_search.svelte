<script>
	import { loading } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';
	import { FormNote } from '$lib/layout';

	let { status, error = $bindable() } = $props();

	let name = $state('');

	const validate = () => {
		error = {};
		if (!name) {
			error.search = 'this field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Getting Organization . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/org/${name}`);
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			status.value = 1;
			status.org = resp.org;
		} else if (resp.error == 'not found') {
			error.search = 'No organization found with this ID. please contact the admin.';
		} else {
			error = resp;
		}
	};
</script>

<form onsubmit={(e) => e.preventDefault()} novalidate autocomplete="off">
	<FormNote>
		{#snippet title()}
			This card is not linked to any organization
		{/snippet}
		{#snippet note()}
			In order to link your business card to an organization, you need to search for the
			organization by its ID.
		{/snippet}
	</FormNote>

	<IG
		name="Organization ID"
		icon="corporate_fare"
		error={error.search}
		placeholder="Organization ID here"
		type="text"
		bind:value={name}
	/>

	<Button onclick={validate}>
		Search
		<Icon icon="send" />
	</Button>
</form>

<style>
</style>
