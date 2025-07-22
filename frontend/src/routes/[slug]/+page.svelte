<script>
	import * as htmlToImage from 'html-to-image';

	import Log from '$lib/log.svelte';
	import Meta from '$lib/meta.svelte';
	import Icon from '$lib/icon.svelte';
	import Link from '$lib/button/link.svelte';

	import Header from './header.svelte';
	import NameJobPhoto from './name_job_photo.svelte';

	import Socials from './socials.svelte';

	import BusinessCard from './business_card.svelte';
	import Button from '$lib/button/button.svelte';
	import Org from '../@[slug]/org.svelte';

	let { data } = $props();
	let card = data.card;
	console.log(card);
</script>

<Log action={'viewed'} entity_key={card.key} entity_type={'card'} />

<Meta title={card.firstname} />
<Header {card} />
<NameJobPhoto {card} />

<section class="content">
	{#if card.about}
		<div class="group">
			<Icon icon="person" size="1.2" />
			<div>
				<div class="label">About me:</div>
				<div class="about">
					{card.about}
				</div>
			</div>
		</div>
	{/if}

	{#if card.phone}
		<span class="group">
			<Icon icon="call" size="1.2" />
			<div>
				<div class="label">Phone:</div>
				<Link href="tel:{card.phone}">{card.phone}</Link>
			</div>
		</span>
	{/if}

	<div class="group">
		<Icon icon="email" size="1.2" />
		<div>
			<div class="label">Email:</div>
			<Link href="mailto:{card.email}">
				<span class="email">
					{card.email}
				</span>
			</Link>
		</div>
	</div>

	{#if card.office_location_id >= 0 && card.status == 'live'}
		<div class="group address">
			<Icon icon="location_on" size="1.2" />
			<div>
				<div class="label">Location:</div>
				<Link href={card.org.address[card.office_location_id].url}>
					{card.org.address[card.office_location_id].address}
				</Link>
			</div>
		</div>
	{/if}

	<Socials links={card.social_links} name={card.firstname} />

	<Button
		size="small"
		onclick={() => {
			htmlToImage.toPng(document.getElementById('to_print')).then(function (dataUrl) {
				var a = document.createElement('a');
				a.download = `${card.firstname} ${card.lastname} business card.png`;
				a.href = dataUrl;
				a.click();
			});
		}}
	>
		Save Business Card
	</Button>

	<br />

	<BusinessCard {card} />

	{#if card.status == 'live'}
		<br /><br />
		<hr />
		<br /><br />
		<Org org={card.org}></Org>
	{/if}
</section>

<style>
	.content {
		position: relative;

		max-width: var(--mobileWidth);
		width: 100%;
		margin: auto;
		padding: 0 var(--sp2);
		padding-bottom: var(--sp5);
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

	.address {
		max-width: 500px;
	}
	.email {
		word-break: break-all;
		overflow-wrap: anywhere;
	}
</style>
