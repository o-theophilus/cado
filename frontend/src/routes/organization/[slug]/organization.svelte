<script>
	import { notification, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import IG from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Card from '$lib/card.svelte';

	export let organization;
	export let open;
	let form = {
		...organization,
		email_domains: organization.email_domains.join(', ')
	};

	let error = {};

	const validate = () => {
		error = {};

		if (!form.name) {
			error.name = 'this field is required';
		}

		let domains = form.email_domains
			.split(',')
			.map((item) => item.trim())
			.filter(Boolean);

		for (const x of domains) {
			if (!/@\S+\.\S+/.test(x)) {
				if (!error.email_domains) {
					error.email_domains = `invalid domain: ${x}`;
				} else {
					error.email_domains = `${error.email_domains}, ${x}`;
				}
			}
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'Saving Post . . .';

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/organization/org/${organization.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({
				...form,
				email_domains: form.email_domains
					.split(',')
					.map((item) => item.trim())
					.filter(Boolean)
			})
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			organization = resp.organization;
			open = false;
			$notification = {
				message: 'Details Saved'
			};
		} else {
			error = resp;
		}
	};
</script>

<Card {open} on:open>
	<svelte:fragment slot="title">Organization</svelte:fragment>

	<form on:submit|preventDefault novalidate autocomplete="off">
		{#if error.error}
			<div class="error">
				{error.error}
			</div>
		{/if}

		<IG
			name="Name"
			icon="work"
			error={error.name}
			placeholder="Name here"
			type="text"
			bind:value={form.name}
		/>

		<IG
			name="Fullname"
			icon="work"
			error={error.fullname}
			placeholder="Fullname here"
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
			name="Email Domains"
			icon="email"
			error={error.email_domains}
			placeholder="Email Domains here"
			type="text"
			bind:value={form.email_domains}
		/>

		<Button on:click={validate}>
			Submit
			<Icon icon="send" />
		</Button>
	</form>
</Card>

<style>
	.error {
		margin: var(--sp2) 0;
	}
</style>
