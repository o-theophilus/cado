<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';

	import Content from '$lib/content.svelte';
	import Meta from '$lib/meta.svelte';
	import ButtonFold from '$lib/button/fold.svelte';
	import Back from '$lib/button/back.svelte';

	export let data;
	let { users } = data;

	let open_users = users.length > 0;
</script>

<Meta title="Manage Photos" description="Here you will find missing or excess images" />

<Content>
	<br />
	<div class="left">
		<Back />
		<strong class="ititle"> Photo Error </strong>
	</div>

	<hr />

	<div class="fold">
		<div class="title">
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
</Content>

<style>
	.left {
		display: flex;
		align-items: center;
		gap: var(--sp2);
	}

	.fold {
		margin: var(--sp2) 0;
	}
	.title {
		font-weight: 900;
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin: var(--sp2) 0;
	}
</style>
