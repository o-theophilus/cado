<script>
	import { organization } from '$lib/store.js';

	import Link from '$lib/button/link.svelte';
	import Icon from '$lib/icon.svelte';
</script>

{#if $organization.phone}
	<div class="group">
		<Icon icon="call" size="1.3" />
		<div>
			<div class="label">Phone:</div>
			<Link href="tel:{$organization.phone}">{$organization.phone}</Link>
		</div>
	</div>
{/if}

{#if $organization.email}
	<div class="group">
		<Icon icon="email" size="1.3" />
		<div>
			<div class="label">Email:</div>
			<Link href="mailto:{$organization.email}">{$organization.email}</Link>
		</div>
	</div>
{/if}

{#if $organization.website}
	<div class="group">
		<Icon icon="language" size="1.3" />
		<div>
			<div class="label">Website:</div>
			<Link href="https://{$organization.website}" blank>{$organization.website}</Link>
		</div>
	</div>
{/if}

{#if $organization.address.length != 0}
	<div class="group">
		<Icon icon="location_on" size="1.3" />
		<div>
			<div class="label">Address:</div>
			{#each $organization.address as a, i}
				{#if i > 0}
					<div class="gap" />
				{/if}
				<Link href={a.url} blank>{a.address}</Link>
			{/each}
		</div>
	</div>
{/if}

<style>
	.group {
		display: grid;
		grid-template-columns: 1fr 100fr;
		gap: 0 var(--sp2);

		align-items: flex-start;

		margin: var(--sp2) 0;
	}

	.label {
		font-size: 0.8rem;
	}

	.gap {
		grid-column: 1 / 3;
		height: var(--sp1);
	}
</style>
