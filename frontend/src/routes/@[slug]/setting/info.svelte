<script>
	import { notify, loading, token } from '$lib/store.svelte.js';

	import IG from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Card from '$lib/card.svelte';

	let { org, active_card, update } = $props();

	let form = $state({
		name: org.name,
		fullname: org.fullname,
		slogan: org.slogan,
		about: org.about
	});
	let error = $state({});

	const validate = () => {
		error = {};
		if (!form.name) {
			error.name = 'this field is required';
		}

		if (!form.fullname) {
			error.fullname = 'this field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Saving Information . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/org/${org.key}`, {
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
			update(resp.org);
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
			name="Name"
			icon="person"
			error={error.name}
			placeholder="name here"
			type="text"
			bind:value={form.name}
			required
		/>

		<IG
			name="Fullname"
			icon="person"
			error={error.fullname}
			placeholder="fullname here"
			type="text"
			bind:value={form.fullname}
		/>

		<IG
			name="Slogan"
			icon="work"
			error={error.slogan}
			placeholder="Slogan here"
			type="text"
			bind:value={form.slogan}
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
