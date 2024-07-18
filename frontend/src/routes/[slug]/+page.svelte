<script>
	import { page } from '$app/stores';
	import { user as me, organization } from '$lib/store.js';
	import * as htmlToImage from 'html-to-image';

	import Meta from '$lib/meta.svelte';
	import Icon from '$lib/icon.svelte';
	import Link from '$lib/button/link.svelte';

	import Header from './header.svelte';
	import NameRole from './name_role.svelte';

	import Socials from '../layout/socials.svelte';

	import BusinessCard from './business_card.svelte';
	import Button from '$lib/button/button.svelte';
	import Setting from './setting.svelte';

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
</script>

{#key `${$page.url.pathname}${$page.url.search}`}
	<Meta title={user?.firstname || data.error} />
{/key}

<Header />
<NameRole {user} />

<section class="content">
	{#if user.about_me}
		<div class="group">
			<Icon icon="person" size="1.2" />
			<div>
				<div class="label">About me:</div>
				<div class="about">
					{user.about_me}
				</div>
			</div>
		</div>
	{/if}

	{#if user.phone}
		<span class="group">
			<Icon icon="call" size="1.2" />
			<div>
				<div class="label">Phone:</div>
				<Link href="tel:{user.phone}">{user.phone}</Link>
			</div>
		</span>
	{/if}

	<div class="group">
		<Icon icon="email" size="1.2" />
		<div>
			<div class="label">Email:</div>
			<Link href="mailto:{user.email}">
				{user.email}
			</Link>
		</div>
	</div>

	{#if user.office_location}
		<div class="group">
			<Icon icon="location_on" size="1.2" />
			<div>
				<div class="label">Location:</div>
				{#each $organization.address as a}
					<Link href="https://maps.app.goo.gl/{a.url}">
						{#if a.name == user.office_location}
							{a.address}
						{/if}
					</Link>
				{/each}
			</div>
		</div>
	{/if}

	<div class="social">
		<Socials links={{ ...user, name: user.firstname }} />

		<BusinessCard {user} />
		<Button
			size="small"
			on:click={() => {
				htmlToImage.toPng(document.getElementById('to_print')).then(function (dataUrl) {
					var a = document.createElement('a');
					a.download = `${user.firstname} ${user.lastname} business card.png`;
					a.href = dataUrl;
					a.click();
				});
			}}
		>
			Save Business Card
		</Button>
	</div>

	{#if user.key == $me.key}
		<Setting {user} {update} {update_photo} />
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

	.group {
		display: flex;
		gap: 0 var(--sp2);
		align-items: flex-start;
		margin: var(--sp2) 0;
	}
	.about {
		margin-top: var(--sp0);
		line-height: 1.5;
	}
	.label {
		font-size: 0.8rem;
	}

	.social {
		display: flex;
		flex-direction: column;
		margin: var(--sp4) 0;
		gap: var(--sp1);
	}
</style>
