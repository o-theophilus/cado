<script>
	import { notify, loading, token } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';
	import { Card, Error } from '$lib/layout';
	import Social from './social.add.svelte';
	import View from './social.view.svelte';

	let { entity, _type, active_card, update } = $props();

	let form = $state({
		social_links: entity.social_links
	});
	let error = $state({});

	const validate = () => {
		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Saving Social Links . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/${_type}/${entity.key}`, {
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
			update(resp[_type]);
			notify.open('Social Links Saved');
		} else {
			error = resp;
		}
	};

	let list = ['whatsapp', 'linkedin', 'twitter', 'facebook', 'instagram', 'other'];
	let name = 'social';
</script>

<Card open={active_card.value == name} onopen={() => active_card.set(name)}>
	{#snippet title()}
		Social Links
	{/snippet}

	<form onsubmit={(e) => e.preventDefault()} novalidate autocomplete="off">
		<Error error={error.error} block --error-margin-top="0"></Error>

		<Social bind:value={form.social_links} {list}></Social>
		<View bind:value={form.social_links} {list}></View>
		<br />

		<Button onclick={validate}>
			Save
			<Icon icon="save" />
		</Button>
	</form>
</Card>

<style>
</style>
