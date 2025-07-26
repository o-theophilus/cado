<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';

	import UpdateUrl from '$lib/update_url.svelte';

	import { BackButton } from '$lib/button';
	import { Row } from '$lib/layout';
	import Meta from '$lib/meta.svelte';
	import Pagination from '$lib/pagination.svelte';
	import DropPlus from '$lib/dropdown.svelte';
	import Search from '$lib/search.svelte';
	import User from './user.svelte';

	export let data;
	$: users = data.users;
	$: total_page = data.total_page;
	let { order_by } = data;
	// let { _status } = data;
</script>

<UpdateUrl />
<Meta title="All Users" />

<div class="page">
	<Row>
		<BackButton />
		<div class="page_title">
			User{users.length > 1 ? 's' : ''}
		</div>

		<!-- <DropPlus name="status" list={['all', ..._status]} default_value="all" /> -->
	</Row>

	<div class="search_bar">
		<Search />
		<DropPlus name="order" list={order_by} icon="sort" />
	</div>

	{#each users as x (x.key)}
		<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
			<User user={x} />
		</div>
	{:else}
		no item here
	{/each}

	<Pagination {total_page} />
</div>

<style>
	.page {
		max-width: var(--mobileWidth);
		width: 100%;
		margin: auto;
		padding: var(--sp2);
	}
	.search_bar {
		margin: var(--sp2) 0;
		display: flex;
		gap: var(--sp1);
		align-items: center;
	}
</style>
