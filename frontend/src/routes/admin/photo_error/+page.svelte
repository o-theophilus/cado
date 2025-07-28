<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';

	import { Meta } from '$lib/macro';
	import { BackButton, FoldButton } from '$lib/button';
	import { Row } from '$lib/layout';

	export let data;
	let { users } = data;

	let open_users = users.length > 0;
</script>

<Meta title="Manage Photos" description="Here you will find missing or excess images" />

<div class="page">
	<Row>
		<BackButton />
		<div class="page_title">Photo Error</div>
	</Row>

	<div class="fold">
		<Row>
			User{users.length > 1 ? 's' : ''} ({users.length})
			<FoldButton
				open={open_users}
				onclick={() => {
					open_users = !open_users;
				}}
			/>
		</Row>

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
