<script>
	import { loading, notify, token } from '$lib/store.svelte.js';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';

	import Meta from '$lib/meta.svelte';

	import BRound from '$lib/button/round.svelte';
	import One from './one.svelte';

	let { data } = $props();

	let org = data.org;
	let cards = $state(data.cards);
	let error = $state({});

	let selected = $state({
		value: [],
		add(n) {
			this.value.push(n);
		},
		remove(n) {
			this.value = this.value.filter((x) => x != n);
		},
		check(n) {
			return selected.value.includes(n);
		}
	});

	const status = async (n) => {
		error = {};
		loading.open('Sending Request . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/org/card/status/${org.key}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: token.value
			},
			body: JSON.stringify({
				card_keys: selected.value,
				status: n
			})
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			selected.value = [];
			notify.open('Request Canceled');
			cards = resp.cards;
		} else {
			error = resp;
		}
	};
</script>

<Meta title={org.name} />

<section class="page">
	<div class="line">
		<BRound icon="arrow_back" href="/@{org.slug}" />
		<h1>Organization Cards</h1>
	</div>
	<br />

	{#each cards as card (card.key)}
		<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
			<One {card} {selected} {status}></One>
		</div>
	{:else}
		Nothing
	{/each}
</section>

<style>
	.page {
		position: relative;

		max-width: var(--mobileWidth);
		width: 100%;
		margin: auto;
		padding: 0 var(--sp2);
	}

	.line {
		display: flex;
		gap: var(--sp2);
		align-items: center;
	}
</style>
