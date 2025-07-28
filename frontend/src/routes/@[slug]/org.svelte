<script>
	import { page } from '$app/state';
	import { user } from '$lib/store.svelte.js';
	import { Icon } from '$lib/macro';
	import { Link, RoundButton } from '$lib/button';
	import { Row } from '$lib/layout';
	import Socials from '../[slug]/socials.svelte';

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
</script>

{#if page.route.id == '/[slug]' && org.user_key == user.value.key}
	<Row space>
		<div></div>

		<Row --row-gap="8px">
			<RoundButton tooltip="settings" href="/@{org.slug}/card">
				<Icon icon="card"></Icon>
			</RoundButton>
			<RoundButton tooltip="settings" href="/@{org.slug}/setting">
				<Icon icon="settings"></Icon>
			</RoundButton>
		</Row>
	</Row>
{/if}

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
	<div class="group">
		<Icon icon="location_on" size="1.3" />
		<div>
			<div class="label">Address:</div>
			<div class="address">
				{#each org.address as a, i}
					{#if i > 0}
						<div class="gap"></div>
					{/if}

					{#if a.url}
						<Link href={a.url} blank>{a.address}</Link>
					{:else}
						{a.address}
					{/if}
				{/each}
			</div>
		</div>
	</div>
{/if}

<Socials links={org.social_links} name={org.firstname} />

<style>
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
		font-weight: 800;
	}

	.gap {
		height: var(--sp1);
	}

	.email {
		word-break: break-all;
		overflow-wrap: anywhere;
	}
</style>
