<script>
	import { page } from '$app/stores';
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { user as me, module, to_print } from '$lib/store.js';

	import Meta from '$lib/meta.svelte';
	import Icon from '$lib/icon.svelte';
	import Link from '$lib/button/link.svelte';
	import Fold from '$lib/button/fold.svelte';
	import Header from './header.svelte';
	import NameRole from './name_role.svelte';

	import Socials from '../layout/socials.svelte';

	import Detail from './_detail.svelte';
	import Social from './_social.svelte';

	import Photo from './_photo.svelte';
	import Email from './_email_1.svelte';
	import Delete from './_delete.svelte';
	import Password from './_password_1_email.svelte';

	import Print from './print.svelte';

	export let data;
	$: user = data.user;

	const update = (data) => {
		user = data;
		if (user.key == $me.key) {
			$me = user;
		}
	};

	const update_photo = (data) => {
		user.photo = data;
		if (user.key == $me.key) {
			$me = user;
		}
	};

	let open = false;
</script>

{#key `${$page.url.pathname}${$page.url.search}`}
	<Meta title={user?.firstname || data.error} />
{/key}

<Header />
<NameRole {user} />

<section class="content">
	{#if user.about_me}
		<div class="grid">
			<Icon icon="person" />
			About Me:
			<span />
			{user.about_me}
		</div>
	{/if}

	{#if user.phone}
		<span class="grid">
			<Icon icon="call" />
			phone:
			<span />
			<Link href="tel:+234{user.phone}">{user.phone}</Link>
		</span>
	{/if}

	<div class="grid">
		<Icon icon="email" size="20" />
		Email:
		<span />
		<Link href="mailto:{user.email}">
			{user.email}
		</Link>
	</div>

	<Socials links={{ ...user, name: user.firstname }} />

	<Link
		on:click={() => {
			// $to_print = user;
			// setTimeout(() => {
			// 	window.print();
			// });
		}}
	>
		Print
	</Link>

	<Print {user} />

	{#if user.key == $me.key}
		<hr />
		<div class="settings">
			<div class="line gap">
				<div class="line">
					<Icon icon="settings" size="20" />
					Settings
				</div>
				<Fold
					{open}
					on:click={() => {
						open = !open;
					}}
				/>
			</div>
			{#if open}
				<div class="links" transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
					<br />
					<Link
						on:click={() => {
							$module = {
								module: Detail,
								user,
								update
							};
						}}
					>
						Edit Details
					</Link>

					|

					<Link
						on:click={() => {
							$module = {
								module: Photo,
								user,
								update: update_photo
							};
						}}
					>
						Edit Photo
					</Link>

					<br />

					<Link
						on:click={() => {
							$module = {
								module: Email,
								update
							};
						}}
					>
						Edit Email
					</Link>

					|

					<Link
						on:click={() => {
							$module = {
								module: Social,
								user,
								update
							};
						}}
					>
						Edit Social Links
					</Link>

					<br />

					<Link
						on:click={() => {
							$module = {
								module: Password
							};
						}}
					>
						Change Password
					</Link>

					|

					<Link
						on:click={() => {
							$module = {
								module: Delete,
								user
							};
						}}
					>
						Delete Account
					</Link>
				</div>
			{/if}
		</div>
	{/if}
</section>

<style>
	.content {
		position: relative;

		max-width: var(--mobileWidth);
		width: 100%;
		margin: auto;
		padding: 0 var(--sp2);
	}

	.grid {
		display: grid;
		grid-template-columns: 1fr 100fr;
		gap: 0 var(--sp2);

		align-items: center;
		margin: var(--sp2) 0;
	}

	.settings {
		margin: var(--sp4) 0;
	}

	.line {
		display: flex;
		align-items: center;
		gap: var(--sp2);
	}

	.gap {
		justify-content: space-between;
	}
</style>
