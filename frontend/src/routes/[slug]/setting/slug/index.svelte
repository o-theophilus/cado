<script>
	import { createEventDispatcher } from 'svelte';
	import { user as me, notification } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import Slug from './slug.svelte';
	import Ok from './ok.svelte';

	let emit = createEventDispatcher();
	export let user;
	export let open;
	let slug = user.slug;
	let state = 0;
	let error = {};
</script>

<Card {open} on:open>
	<svelte:fragment slot="title">Change Username</svelte:fragment>

	{#if state == 0}
		<Slug
			{slug}
			{error}
			user_key={user.key}
			on:ok={(e) => {
				slug = e.detail;
				state = 1;
			}}
		/>
	{:else if state == 1}
		<Ok
			user_key={user.key}
			{slug}
			on:ok={(e) => {
				if (!e.detail) {
					$notification = {
						message: 'Username Saved'
					};
					user.slug = slug;
					if ($me.key == user.key) {
						$me.slug = slug;
					}
					emit('back', `/${slug}`);
					window.history.replaceState(history.state, '', `/${slug}/setting`);
				}
				state = 0;
				emit('open', e.detail);
			}}
			on:slug={(e) => {
				state = 0;
				error.slug = e.detail;
			}}
		/>
	{/if}
</Card>
