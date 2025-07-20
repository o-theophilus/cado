<script>
	import { page } from '$app/state';
	import { user } from '$lib/store.svelte.js';
	import Icon from '$lib/icon.svelte';
	import Link from '$lib/button/link.svelte';
	import Socials from '../[slug]/socials.svelte';
	import BRound from '$lib/button/round.svelte';

	let { org } = $props();

	let width = $state(100);
	let height = $state(100);
	const calc_ = () => {
		if (!org.photo) {
			return;
		}
		let match = org.photo.match(/_(\d+)x(\d+)\./);
		if (!match) {
			return;
		}

		let ar = match[1] / match[2];
		width = Math.sqrt(width * height * ar);
		height = width / ar;
	};
	calc_();

	console.log(org);
</script>

<div class="hline">
	{#if page.route.id == '/@[slug]'}
		<div class="page_title">Organization</div>
	{:else if org.user_key == user.value.key}
		<div></div>
	{/if}

	{#if org.user_key == user.value.key}
		<div class="hline">
			<BRound icon="card" tooltip="settings" href="/@{org.slug}/card" large></BRound>
			<BRound icon="settings" tooltip="settings" href="/@{org.slug}/setting" large></BRound>
		</div>
	{/if}
</div>

<br />

{#if org.photo}
	<img src={org.photo || '/no_photo.png'} alt={org.name} style:max-width="{width}px" />
{:else}
	<div class="img" style:max-width="{width}px">
		<Icon icon="corporate_fare" size="4" />
	</div>
{/if}

<br />
<br />

<div class="name">
	{org.fullname || org.name}
</div>
{#if org.slogan}
	<div class="slogan">
		{org.slogan}
	</div>
{/if}

{#if org.about}
	<div class="group">
		{org.about}
	</div>
{/if}

<br />

{#if org.phone}
	<span class="group">
		<Icon icon="call" size="1.2" />
		<div>
			<div class="label">Phone:</div>
			<Link href="tel:{org.phone}">{org.phone}</Link>
		</div>
	</span>
{/if}

<div class="group">
	<Icon icon="email" size="1.2" />
	<div>
		<div class="label">Email:</div>
		<Link href="mailto:{org.email}">
			<span class="email">
				{org.email}
			</span>
		</Link>
	</div>
</div>

{#if org.website}
	<div class="group">
		<Icon icon="language" size="1.3" />
		<div>
			<div class="label">Website:</div>
			<Link href="https://{org.website}" blank>{org.website}</Link>
		</div>
	</div>
{/if}

{#if org.address?.length != 0}
	<div class="group address">
		<Icon icon="location_on" size="1.3" />
		<div>
			<div class="label">Address:</div>
			{#each org.address as a, i}
				{#if i > 0}
					<div class="gap"></div>
				{/if}
				<Link href={a.url} blank>{a.address}</Link>
			{/each}
		</div>
	</div>
{/if}

<Socials links={org.social_links} name={org.firstname} />

<style>
	.hline {
		gap: var(--sp1);
	}

	img {
		object-fit: contain;
		width: 100%;
	}
	.img {
		display: flex;
		align-items: center;
		justify-content: center;

		width: 100%;
		aspect-ratio: 1;

		border-radius: var(--sp1);
		border: 2px solid var(--bg2);
		padding: var(--sp2);

		fill: var(--ft2);
	}
	.group {
		display: flex;
		gap: 0 var(--sp2);
		align-items: flex-start;
		margin: var(--sp2) 0;
	}

	.name {
		font-size: 2rem;
		font-weight: 700;
		color: var(--ft1);
	}

	.label,
	.slogan {
		font-size: 0.9rem;
	}

	.address {
		max-width: 500px;
	}

	.gap {
		height: var(--sp1);
	}

	.email {
		word-break: break-all;
		overflow-wrap: anywhere;
	}
</style>
