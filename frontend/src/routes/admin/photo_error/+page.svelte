<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';

	import Meta from '$lib/meta.svelte';
	import ButtonFold from '$lib/button/fold.svelte';
	import Back from '$lib/button/back.svelte';

	export let data;
	let { users } = data;

	let open_users = users.length > 0;
</script>

<Meta title="Manage Photos" description="Here you will find missing or excess images" />

<div class="page">
	<div class="hline">
		<div class="hline">
			<Back />
			<div class="page_title">Photo Error</div>
		</div>
	</div>

	<hr />

	<div class="fold">
		<div class="hline">
			User{users.length > 1 ? 's' : ''} ({users.length})
			<ButtonFold
				open={open_users}
				onclick={() => {
					open_users = !open_users;
				}}
			/>
		</div>

		{#if open_users}
			<div transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
				{#each users as x}
					<a href="/profile?user={x.key}">{x.name}</a>

					<br />
				{:else}
					no user here
				{/each}
			</div>
		{/if}
	</div>

	<hr />
</div>

<style>
	.page {
		max-width: var(--mobileWidth);
		width: 100%;
		margin: auto;
		padding: var(--sp2);
	}
	.fold {
		margin: var(--sp2) 0;
	}
</style>
