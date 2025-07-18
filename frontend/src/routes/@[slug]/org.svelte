<script>
	import Icon from '$lib/icon.svelte';
	import Link from '$lib/button/link.svelte';
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

{#if org.photo}
	<img
		src={org.photo || '/no_photo.png'}
		alt={org.name}
		style:width="{width}px"
		style:height="{height}px"
	/>
	<br />
	<br />
{/if}

<div class="name">
	{org.fullname}
</div>

{#if org.slogan}
	<div class="group slogan">
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
			{org.email}
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
	img {
		object-fit: contain;
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
</style>
