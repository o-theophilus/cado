<script>
	import SVG from '$lib/svg.svelte';
	export let links = {};
</script>

<div class="block" >
	{#if links.whatsapp}
		<a href="https://wa.me/{links.whatsapp}/?text=Hello%20{links.name}">
			<SVG type="whatsapp" />
		</a>
	{/if}

	{#if links.linkedin}
		<a
			href="https://www.linkedin.com/in/{links.linkedin}/"
			target="_blank"
			rel="noopener noreferrer"
		>
			<SVG type="linkedin" />
		</a>
	{/if}

	{#if links.twitter}
		<a href="https://twitter.com/{links.twitter}" target="_blank" rel="noopener noreferrer">
			<SVG type="twitter" />
		</a>
	{/if}

	{#if links.facebook}
		<a href="https://m.facebook.com/{links.facebook}" target="_blank" rel="noopener noreferrer">
			<SVG type="facebook" />
		</a>
	{/if}

	{#if links.instagram}
		<a
			href="https://www.instagram.com/{links.instagram}/"
			target="_blank"
			rel="noopener noreferrer"
		>
			<SVG type="instagram" />
		</a>
	{/if}
</div>

<style>
	.block {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp1);

		margin: var(--sp4) 0;

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
