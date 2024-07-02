<script>
	import { organization } from '$lib/store.js';

	import Link from '$lib/button/link.svelte';
	import Icon from '$lib/icon.svelte';
</script>

<span class="grid">
	<Icon icon="call" />
	Phone:
	<span />
	<Link href="tel:{$organization.phone}">{$organization.phone}</Link>
</span>

<span class="grid">
	<Icon icon="email" />
	Email:
	<span />
	<Link href="mailto:{$organization.email}">{$organization.email}</Link>
</span>

<span class="grid">
	<Icon icon="language" />
	Website:
	<span />
	<Link href="https://{$organization.website}" blank>{$organization.website}</Link>
</span>

<span class="grid">
	<Icon icon="location_on" />
	Address:

	{#each $organization.address as a, i}
		{#if i > 0}
			<span class="gap" />
		{/if}

		<span />
		<Link href="https://maps.app.goo.gl/{a.url}" blank>{a.address}</Link>
	{/each}
</span>

<style>
	.grid {
		display: grid;
		grid-template-columns: 1fr 100fr;
		gap: 0 var(--sp2);

		align-items: center;
		margin: var(--sp2) 0;
	}

	.gap {
		grid-column: 1 / 3;
		height: var(--sp2);
	}
</style>
