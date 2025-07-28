<script>
	import { loading, token, notify } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Row, FormNote } from '$lib/layout';
	import { IG } from '$lib/input';
	import { Icon } from '$lib/macro';

	let { org, active_card, update, form, status, error = $bindable() } = $props();

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
			status.value = 0;
			form = {};

			active_card.close();
			update(resp.org);
			notify.open('ID Changed');
			window.history.replaceState(history.state, '', `/@${org.slug}/setting`);
		} else {
			error = resp;

			if (error.slug) {
				status.value = 0;
			}
		}
	};
</script>

<form onsubmit={(e) => e.preventDefault()} novalidate autocomplete="off">
	<FormNote status="201">
		{#snippet title()}
			Changing your organization's ID will update all associated links.
		{/snippet}
	</FormNote>

	<IG
		name="Password"
		icon="key"
		error={error.password}
		bind:value={form.password}
		type="password+"
		placeholder="Password here"
	></IG>

	<Row --row-gap="8px">
		<Button onclick={validate2}>
			<Icon icon="send" />
			Confirm
		</Button>

		<Button
			onclick={() => {
				error = {};
				status.value = 0;
			}}
		>
			<Icon icon="arrow_back" />
			Back
		</Button>
	</Row>
</form>

<style>
</style>
