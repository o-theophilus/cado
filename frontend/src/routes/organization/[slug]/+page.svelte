<script>
	import { user } from '$lib/store.js';

	import Content from '$lib/content.svelte';
	import Meta from '$lib/meta.svelte';
	import Back from '$lib/button/back.svelte';

	import Photo from './photo.svelte';
	import Organization from './organization.svelte';
	import Contact from './contact.svelte';
	import Social from './social.svelte';
	// import Delete from './delete.svelte';

	export let data;
	let organization = data.organization;
	let open = null;

	let types = ['logo', 'icon'];
</script>

<Meta title={organization.name} />

<div class="bg">
	<Content>
		<div class="title">
			<div class="left">
				<Back />
				<strong class="ititle"> Setting </strong>
			</div>
		</div>

		{#each types as type}
			{#if $user.access.includes(`organization:edit_${type}`)}
				<Photo
					{type}
					{organization}
					open={open == type}
					on:open={() => {
						open = type;
					}}
				/>
			{/if}
		{/each}

		{#if $user.access.includes('organization:edit_organization')}
			<Organization
				{organization}
				open={open == 'organization'}
				on:open={() => {
					open = 'organization';
				}}
			/>
		{/if}

		{#if $user.access.includes('organization:edit_contact')}
			<Contact
				{organization}
				open={open == 'contact'}
				on:open={() => {
					open = 'contact';
				}}
			/>
		{/if}

		{#if $user.access.includes('organization:edit_social_media')}
			<Social
				{organization}
				open={open == 'social'}
				on:open={() => {
					open = 'social';
				}}
			/>
		{/if}

		<!-- <br /> -->
		<!-- <strong class="ititle title"> Advanced </strong> -->

		<!-- <Delete
			open={open == 'delete'}
			on:open={() => {
				open = 'delete';
			}}
		/> -->
	</Content>
</div>

<style>
	.title {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: var(--sp3) 0;
	}
	.left {
		display: flex;
		align-items: center;
		gap: var(--sp2);
	}
	.bg {
		background-color: var(--bg2);
		padding-bottom: var(--sp3);
	}
</style>
