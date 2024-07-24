<script>
	import { createEventDispatcher } from 'svelte';
	import { onMount } from 'svelte';

	import Card from '$lib/card.svelte';
	import Access from './access.svelte';
	import Ok from './ok.svelte';

	let emit = createEventDispatcher();
	export let user;
	export let open;
	let raw_access = {};
	let access = [];
	let state = 0;

	onMount(async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/admin/access`);
		resp = await resp.json();
		if (resp.status == 200) {
			raw_access = resp.access;
		}
	});
</script>

<Card {open} on:open>
	<svelte:fragment slot="title">User Access</svelte:fragment>

	{#if state == 0}
		<Access
			{raw_access}
			user_access={[...user.access]}
			on:ok={(e) => {
				access = e.detail;
				state = 1;
			}}
		/>
	{:else if state == 1}
		<Ok
			user_key={user.key}
			{access}
			on:ok={(e) => {
				state = 0;

				if (!e.detail) {
					user.access = access;
				}
				emit('open', e.detail);
			}}
		/>
	{/if}
</Card>

<style>
</style>
