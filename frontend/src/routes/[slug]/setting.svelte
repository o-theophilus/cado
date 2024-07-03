<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { module } from '$lib/store.js';

	import Icon from '$lib/icon.svelte';
	import Link from '$lib/button/link.svelte';
	import Fold from '$lib/button/fold.svelte';

	import Detail from './_detail.svelte';
	import Social from './_social.svelte';

	import Photo from './_photo.svelte';
	import Email from './_email_1.svelte';
	import Delete from './_delete.svelte';
	import Password from './_password_1_email.svelte';

	export let user;
	export let update;
	export let update_photo;

	let open = false;
</script>

<hr />
<div class="settings">
	<div class="line gap">
		<div class="line">
			<Icon icon="settings" size="1.2" />
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

<style>
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
