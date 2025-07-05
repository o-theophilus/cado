<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';

	import Content from '$lib/content.svelte';
	import Back from '$lib/button/back.svelte';
	import Meta from '$lib/meta.svelte';
	import User from '../users/user.svelte';
	import Pagination from '$lib/pagination.svelte';
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

<Content>
	<br />
	<div class="title">
		<div class="left">
			<Back />
			<strong class="ititle">
				Admin{users.length > 1 ? 's' : ''}
			</strong>
		</div>
		<DropPlus name="order" list={order_by} />
	</div>

	<Search {access} />

	{#each users as x (x.key)}
		<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
			<User user={x} />
		</div>
	{:else}
		no item here
	{/each}

	<Pagination {total_page} />
</Content>

<style>
	.title {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	.left {
		display: flex;
		align-items: center;
		gap: var(--sp2);
	}
</style>
