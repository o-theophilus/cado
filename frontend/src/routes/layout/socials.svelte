<script>
	import Icon from '$lib/icon.svelte';
	export let links = {};
</script>

{#if links.whatsapp || links.linkedin || links.twitter || links.facebook || links.instagram}
	<div class="block">
		{#if links.whatsapp}
			<a href="https://wa.me/{links.whatsapp}/?text=Hello%20{links.name}">
				<Icon svg icon="whatsapp" />
			</a>
		{/if}

		{#if links.linkedin}
			<a
				href={links.linkedin}
				target="_blank"
				rel="noopener noreferrer"
			>
				<Icon svg icon="linkedin" />
			</a>
		{/if}

		{#if links.twitter}
			<a href={links.twitter} target="_blank" rel="noopener noreferrer">
				<Icon svg icon="twitter" />
			</a>
		{/if}

		{#if links.facebook}
			<a href={links.facebook} target="_blank" rel="noopener noreferrer">
				<Icon svg icon="facebook" />
			</a>
		{/if}

		{#if links.instagram}
			<a
				href={links.instagram}
				target="_blank"
				rel="noopener noreferrer"
			>
				<Icon svg icon="instagram" />
			</a>
		{/if}
	</div>
{/if}

<style>
	.block {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp0);

		max-width: var(--mobileWidth);
	}

	a {
		--size: 40px;
		display: flex;
		justify-content: center;
		align-items: center;

		width: var(--size);
		height: var(--size);
		border-radius: var(--sp1);
		padding: var(--sp1);

		fill: var(--ft2);
		background-color: var(--bg2);

		transition: fill var(--trans);
	}

	a:hover {
		fill: var(--cl1);
	}
</style>
