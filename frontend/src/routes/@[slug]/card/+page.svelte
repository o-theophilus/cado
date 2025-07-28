<script>
	import { loading, notify, token } from '$lib/store.svelte.js';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';

	import { Meta, Pagination, Search, Dropdown, Radio } from '$lib/page';
	import { BackButton } from '$lib/button';
	import { Row, Br, PageNote } from '$lib/layout';
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

	// TODO: improve accept / reject card process
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

<Meta title="{org.fullname || org.name} - Cards" />

<section class="page">
	<Row space>
		<Row>
			<BackButton href="/@{org.slug}" />
			<div class="page_title">Organization Cards</div>
		</Row>

		<Dropdown icon="sort" list={order} caps></Dropdown>
	</Row>
	<Br />

	<div class="row">
		<Radio list={status}></Radio>
		<div class="search">
			<Search placeholder="Search Cards"></Search>
		</div>
	</div>
	<Br />

	{#each cards as card (card.key)}
		<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
			<One {card} {selected} {card_status}></One>
		</div>
	{:else}
		<PageNote>No Card Found</PageNote>
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

	.row {
		display: flex;
		gap: var(--sp2);
		flex-wrap: wrap;
		align-items: center;
	}

	@media screen and (min-width: 400px) {
		.row {
			flex-wrap: nowrap;
		}
	}

	.search {
		width: 100%;
	}
</style>
