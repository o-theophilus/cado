<script>
	import { user } from '$lib/store.js';

	import Content from '$lib/content.svelte';
	import Meta from '$lib/meta.svelte';
	import Back from '$lib/button/back.svelte';

	import Photo from './photo.svelte';
	import Organization from './organization.svelte';
	import Contact from './contact.svelte';
	import Social from './social.svelte';
	import Delete from './delete.svelte';

	export let data;
	let organization = data.organization;
	let types = ['logo', 'icon'];
	let open = null;

	const set_open = (name, state) => {
		if (state) {
			open = name;
		} else {
			open = null;
		}
	};
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
					on:open={(e) => {
						set_open(type, e.detail);
					}}
				/>
			{/if}
		{/each}

		{#if $user.access.includes('organization:edit_organization')}
			<Organization
				{organization}
				open={open == 'organization'}
				on:open={(e) => {
					set_open('organization', e.detail);
				}}
			/>
		{/if}

		{#if $user.access.includes('organization:edit_contact')}
			<Contact
				{organization}
				open={open == 'contact'}
				on:open={(e) => {
					set_open('contact', e.detail);
				}}
			/>
		{/if}

		{#if $user.access.includes('organization:edit_social_media')}
			<Social
				{organization}
				open={open == 'social'}
				on:open={(e) => {
					set_open('social', e.detail);
				}}
			/>
		{/if}

		{#if $user.access.includes('organization:delete')}
			<!-- TODO: Make functional -->
			<br />
			<strong class="ititle title"> Advanced </strong>

			<Delete
				open={open == 'delete'}
				on:open={(e) => {
					set_open('delete', e.detail);
				}}
			/>
		{/if}
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
