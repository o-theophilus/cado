<script>
	import { goto } from '$app/navigation';
	import Card from '$lib/card.svelte';
	import None from './none.svelte';
	import New from './new.svelte';
	import New2 from './new2.svelte';
	import Search from './search.svelte';
	import Search2 from './search2.svelte';
	import Pending from './pending.svelte';
	import Pending2 from './pending2.svelte';
	import Org from './org.svelte';
	import Org2 from './org2.svelte';

	export let user;
	console.log(user.organization_status);

	export let open;
	let temp = {};

	let state = 'none';
	if (user.organization_status == 'pending') {
		state = 'pending';
	} else if (user.organization_status == 'approved') {
		state = 'org';
	}
</script>

<Card {open} on:open>
	<svelte:fragment slot="title">Organization</svelte:fragment>
	{#if state == 'none'}
		<None
			on:search={() => {
				state = 'search';
			}}
			on:new={() => {
				state = 'new';
			}}
		/>
	{:else if state == 'new'}
		<New
			on:ok={(e) => {
				temp = e.detail;
				state = 'new2';
			}}
			on:x={() => {
				state = 'none';
			}}
		/>
	{:else if state == 'new2'}
		<New2
			form={temp}
			on:ok={(e) => {
				state = 'org';
				console.log(e.detail.organization.slug);
				console.log(e.detail.organization);
				console.log(e.detail);
				console.log(e);
				
				goto(`/organization/${e.detail.organization.slug}`);
			}}
			on:x={() => {
				state = 'none';
			}}
		/>
	{:else if state == 'search'}
		<Search
			on:ok={(e) => {
				temp = e.detail;
				state = 'search2';
			}}
			on:x={() => {
				state = 'none';
			}}
		/>
	{:else if state == 'search2'}
		<Search2
			{user}
			organization={temp}
			on:ok={(e) => {
				user = e.detail;
				state = 'pending';
			}}
			on:x={() => {
				state = 'search';
			}}
		/>
	{:else if state == 'pending'}
		<Pending
			{user}
			on:x={() => {
				state = 'pending2';
			}}
		/>
	{:else if state == 'pending2'}
		<Pending2
			{user}
			on:ok={(e) => {
				user = e.detail;
				state = 'none';
			}}
			on:x={() => {
				state = 'pending';
			}}
		/>
	{:else if state == 'org'}
		<Org
			{user}
			on:ok={() => {
				state = 'org2';
			}}
		/>
	{:else if state == 'org2'}
		<Org2
			{user}
			on:ok={() => {
				state = 'none';
			}}
			on:x={() => {
				state = 'org';
			}}
		/>
	{/if}
</Card>

<style>
</style>
