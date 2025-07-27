<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';

	import { BackButton } from '$lib/button';
	import { Row } from '$lib/layout';
	import { Meta } from '$lib/page';
	import User from '../users/user.svelte';
	import { Pagination } from '$lib/input';
	import Search from './search.svelte';
	import DropPlus from '$lib/dropdown.svelte';
	import UpdateUrl from '$lib/update_url.svelte';

	export let data;
	$: users = data.users;
	$: total_page = data.total_page;
	let { access } = data;
	let { order_by } = data;
</script>

<UpdateUrl />
<Meta title="Admin" description="Users with elevated permission" />

<div class="page">
	<Row space>
		<Row>
			<BackButton />
			<div class="page_title">
				Admin{users.length > 1 ? 's' : ''}
			</div>
			<DropPlus name="order" list={order_by} />
		</Row>
	</Row>

	<Search {access} />

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
</style>
