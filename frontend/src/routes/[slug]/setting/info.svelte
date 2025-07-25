<script>
	import { notify, loading, token } from '$lib/store.svelte.js';

	import IG from '$lib/input_group.svelte';
	import { Button } from '$lib/button';
	import Icon from '$lib/icon.svelte';
	import Card from '$lib/card.svelte';

	let { card, active_card, update } = $props();

	let form = $state({
		firstname: card.firstname,
		lastname: card.lastname,
		job_title: card.job_title,
		about: card.about
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
		loading.open('Saving Information . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/card/${card.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: token.value
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			active_card.close();
			update(resp.card);
			notify.open('Information Saved');
		} else {
			error = resp;
		}
	};

	let name = 'info';
</script>

<Card open={active_card.value == name} onopen={() => active_card.set(name)}>
	{#snippet title()}
		Information
	{/snippet}

	<form onsubmit={(e) => e.preventDefault()} novalidate autocomplete="off">
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

		<IG
			name="About Me"
			error={error.about}
			type="textarea"
			placeholder="About me here"
			bind:value={form.about}
		/>

		<Button onclick={validate}>
			Save
			<Icon icon="save" />
		</Button>
	</form>
</Card>

<style>
	.error {
		margin: var(--sp2) 0;
	}
</style>
