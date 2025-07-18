<script>
	import { goto } from '$app/navigation';
	import { module, loading, token, notify } from '$lib/store.svelte.js';

	import IG from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';

	let form = $state({
		job_title: module.value.job_title,
		firstname: module.value.firstname,
		lastname: module.value.lastname
	});
	let error = $state({});

	const validate = () => {
		error = {};

		if (!form.firstname) {
			error.firstname = 'this field is required';
		}
		if (!form.lastname) {
			error.lastname = 'this field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Loading . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/card`, {
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
			notify.open('Card added successfully');
			module.close();
			goto(`/${resp.card.key}/setting`);
		} else {
			error = resp;
		}
	};
</script>

<form onsubmit={(e) => e.preventDefault()} novalidate autocomplete="off">
	<div class="page_title">Add Card</div>
	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}
	<IG
		name="Firstname"
		icon="person"
		error={error.firstname}
		placeholder="Firstname here"
		type="text"
		bind:value={form.firstname}
		required
	/>
	<IG
		name="Lastname"
		icon="person"
		error={error.lastname}
		placeholder="Lastname here"
		type="text"
		bind:value={form.lastname}
		required
	/>
	<IG
		name="Job Title"
		icon="work"
		error={error.job_title}
		placeholder="Job title here"
		type="text"
		bind:value={form.job_title}
	/>

	<Button onclick={validate}>
		Submit
		<Icon icon="send" />
	</Button>
</form>

<style>
	form {
		padding: var(--sp3);
	}
	.error {
		margin: var(--sp2) 0;
	}
</style>
