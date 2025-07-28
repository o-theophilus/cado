<script>
	import { onMount } from 'svelte';
	import { notify, loading, token } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';
	import { Card, Error } from '$lib/layout';

	let { org, active_card, update } = $props();

	let form = $state({
		email_domains: org.email_domains
	});
	let error = $state({});
	let domain = $state('');

	const clean_value = () => {
		domain = domain.replace(/\r?\n/g, ',');
		domain = domain.replace(/\s+/g, ' ');
		domain = domain.toLowerCase();
		domain = domain.split(',');
		domain = domain.map((i) => i.trim());
		domain = domain.filter(Boolean);
		form.email_domains = domain.filter((v, i, l) => l.indexOf(v) === i);
		domain = form.email_domains.join(', ');
	};

	const validate = () => {
		error = {};

		let err = [];
		for (const x of form.email_domains) {
			if (!/^@[^\s]+\.[^\s]+$/.test(x)) {
				err.push(x);
			}
		}
		if (err.length > 0) {
			error.email_domains = `Invalid format: ${err.join(', ')}. Each domain must start with '@', contain no spaces, and be in the format '@domain.tld'.`;
		}
		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Saving Social Links . . .');
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
			notify.open('Social Links Saved');
		} else {
			error = resp;
		}
	};

	onMount(() => {
		domain = form.email_domains.join(', ');
		clean_value();
	});

	let name = 'domain';
</script>

<Card open={active_card.value == name} onopen={() => active_card.set(name)}>
	{#snippet title()}
		Email Domain
	{/snippet}

	<form onsubmit={(e) => e.preventDefault()} novalidate autocomplete="off">
		<Error error={error.error} block --error-margin-top="0"></Error>

		<IG
			name="Email Domain"
			bind:value={domain}
			error={error.email_domains}
			type="textarea"
			placeholder="Email Domain here"
			onblur={() => {
				clean_value();
			}}
		/>

		<Button onclick={validate}>
			Save
			<Icon icon="save" />
		</Button>
	</form>
</Card>

<style>
</style>
