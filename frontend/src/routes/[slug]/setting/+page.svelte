<script>
	import { user as me } from '$lib/store.js';

	import Content from '$lib/content.svelte';
	import Meta from '$lib/meta.svelte';
	import Back from '$lib/button/back.svelte';

	import Photo from './photo.svelte';
	import Personal from './personal.svelte';
	import Organization from './organization.svelte';
	import Contact from './contact.svelte';
	import Social from './social.svelte';
	import Email from './email/index.svelte';
	import Password from './password/index.svelte';
	import Delete from './delete.svelte';

	export let data;
	let user = data.user;
	let open = null;
</script>

<Meta title={user?.firstname || data.error} />

<div class="bg">
	<Content>
		<div class="title">
			<div class="left">
				<Back />
				<strong class="ititle"> Setting </strong>
			</div>
		</div>

		{#if $me.key == user.key || $me.access.includes('user:edit_photo')}
			<Photo
				{user}
				open={open == 'photo'}
				on:open={() => {
					open = 'photo';
				}}
			/>
		{/if}

		{#if $me.key == user.key || $me.access.includes('user:edit_personal')}
			<Personal
				{user}
				open={open == 'personal'}
				on:open={() => {
					open = 'personal';
				}}
			/>
		{/if}

		{#if $me.key == user.key || $me.access.includes('user:edit_organization')}
			<Organization
				{user}
				open={open == 'organization'}
				on:open={() => {
					open = 'organization';
				}}
			/>
		{/if}

		{#if $me.key == user.key || $me.access.includes('user:edit_contact')}
			<Contact
				{user}
				open={open == 'contact'}
				on:open={() => {
					open = 'contact';
				}}
			/>
		{/if}

		{#if $me.key == user.key || $me.access.includes('user:edit_social_media')}
			<Social
				{user}
				open={open == 'social'}
				on:open={() => {
					open = 'social';
				}}
			/>
		{/if}

		<br />
		<strong class="ititle title"> Advanced </strong>

		{#if $me.key == user.key}
			<Email
				open={open == 'email'}
				on:open={() => {
					open = 'email';
				}}
			/>
		{/if}

		{#if $me.key == user.key}
			<Password
				open={open == 'password'}
				on:open={() => {
					open = 'password';
				}}
			/>
		{/if}

		{#if $me.key == user.key || $me.access.includes('user:delete')}
			<Delete
				{user}
				open={open == 'delete'}
				on:open={() => {
					open = 'delete';
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
