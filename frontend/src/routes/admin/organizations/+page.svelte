<script>
	import { flip } from 'svelte/animate';
	import { module, loading, user } from '$lib/store.js';

	import { cubicInOut } from 'svelte/easing';

	import UpdateUrl from '$lib/update_url.svelte';
	import Content from '$lib/content.svelte';
	import Back from '$lib/button/back.svelte';
	import Icon from '$lib/icon.svelte';
	import Button from '$lib/button/button.svelte';
	import Meta from '$lib/meta.svelte';
	import Pagination from '$lib/pagination.svelte';
	import DropPlus from '$lib/dropdown_plus.svelte';
	import Search from '$lib/search.svelte';

	import Org from './org.svelte';
	import Add from './add.svelte';

	export let data;
	$: organizations = data.organizations;
	$: total_page = data.total_page;
	let { order_by } = data;
	// let { _status } = data;
</script>

<UpdateUrl />
<Meta title="All Organizations" />

<Content>
	<div class="title">
		<div class="left">
			<Back />
			<strong class="ititle">
				Organization{organizations.length > 1 ? 's' : ''}
			</strong>
		</div>

		{#if $user.access.includes('organization:add')}
			<Button
				size="small"
				on:click={() => {
					$module = {
						module: Add
					};
				}}
			>
				<Icon icon="add" />
				Add</Button
			>
		{/if}
		<!-- <DropPlus name="status" list={['all', ..._status]} default_value="all" /> -->
	</div>

	<div class="search_bar">
		<Search />
		<DropPlus name="order" list={order_by} icon="sort" />
	</div>

	{#each organizations as x (x.key)}
		<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
			<Org org={x} />
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

	.search_bar {
		margin: var(--sp2) 0;
		display: flex;
		gap: var(--sp1);
		align-items: center;
	}
</style>
