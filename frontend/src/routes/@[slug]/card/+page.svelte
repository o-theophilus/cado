<script>
	import { loading, notify, token } from '$lib/store.svelte.js';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';

	import Meta from '$lib/meta.svelte';

	import Pagination from '$lib/pagination+.svelte';
	import Search from '$lib/search+.svelte';
	import Dropdown from '$lib/dropdown+.svelte';
	import Gradio from '$lib/gradio+.svelte';

	import BRound from '$lib/button/round.svelte';
	import One from './one.svelte';

	let { data } = $props();

	let org = data.org;
	let cards = $derived(data.cards);
	let total_page = $derived(data.total_page);
	let status = $derived(data._status);
	let order = $derived(data.order_by);
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

	const card_status = async (n) => {
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
	<div class="hline">
		<div class="hline">
			<BRound icon="arrow_back" href="/@{org.slug}" />
			<h1>Organization Cards</h1>
		</div>

		<Dropdown icon="sort" list={order}></Dropdown>
	</div>

	<div class="hline v2">
		<Gradio list={status}></Gradio>
		<div class="search">
			<Search placeholder="Search Cards"></Search>
		</div>
	</div>

	{#each cards as card (card.key)}
		<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
			<One {card} {selected} {card_status}></One>
		</div>
	{:else}
		Nothing
	{/each}

	<br />
	<Pagination {total_page}></Pagination>
</section>

<style>
	.page {
		position: relative;

		max-width: var(--mobileWidth);
		width: 100%;
		min-width: 100px;
		margin: auto;
		padding: var(--sp2);
	}
	.v2 {
		margin: var(--sp2) 0;
	}

	@media screen and (min-width: 400px) {
		.v2 {
			flex-wrap: nowrap;
		}
	}

	.search {
		width: 100%;
	}
</style>
