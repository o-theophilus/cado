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
	import Slug from './slug/index.svelte';
	import Email from './email/index.svelte';
	import Password from './password/index.svelte';
	import Access from './access/index.svelte';
	import Delete from './delete.svelte';

	export let data;
	let user = data.user;
	let open = null;
	let back = '';

	const set_open = (name, state) => {
		if (state) {
			open = name;
		} else {
			open = null;
		}
	};
</script>

<Meta title={user?.firstname || data.error} />

<div class="bg">
	<Content>
		<div class="title">
			<div class="left">
				<Back {back} />
				<strong class="ititle"> Setting </strong>
			</div>
		</div>

		{#if $me.key == user.key || $me.access.includes('user:edit_photo')}
			<Photo
				{user}
				open={open == 'photo'}
				on:open={(e) => {
					set_open('photo', e.detail);
				}}
			/>
		{/if}

		{#if $me.key == user.key || $me.access.includes('user:edit_personal')}
			<Personal
				{user}
				open={open == 'personal'}
				on:open={(e) => {
					set_open('personal', e.detail);
				}}
			/>
		{/if}

		{#if $me.key == user.key || $me.access.includes('user:edit_organization')}
			<Organization
				{user}
				open={open == 'organization'}
				on:open={(e) => {
					set_open('organization', e.detail);
				}}
			/>
		{/if}

		{#if $me.key == user.key || $me.access.includes('user:edit_contact')}
			<Contact
				{user}
				open={open == 'contact'}
				on:open={(e) => {
					set_open('contact', e.detail);
				}}
			/>
		{/if}

		{#if $me.key == user.key || $me.access.includes('user:edit_social_media')}
			<Social
				{user}
				open={open == 'social'}
				on:open={(e) => {
					set_open('social', e.detail);
				}}
			/>
		{/if}

		<br />
		<strong class="ititle title"> Advanced </strong>

		{#if $me.key == user.key || $me.access.includes('user:edit_slug')}
			<Slug
				{user}
				open={open == 'slug'}
				on:open={(e) => {
					set_open('slug', e.detail);
				}}
				on:back={(e) => {
					back = e.detail;
				}}
			/>
		{/if}

		{#if $me.key == user.key}
			<Email
				open={open == 'email'}
				on:open={(e) => {
					set_open('email', e.detail);
				}}
			/>
		{/if}

		{#if $me.key == user.key}
			<Password
				open={open == 'password'}
				on:open={(e) => {
					set_open('password', e.detail);
				}}
			/>
		{/if}

		{#if $me.key != user.key && $me.access.includes('user:edit_access')}
			<Access
				{user}
				open={open == 'access'}
				on:open={(e) => {
					set_open('access', e.detail);
				}}
			/>
		{/if}

		{#if $me.key == user.key || $me.access.includes('user:delete')}
			<Delete
				{user}
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
