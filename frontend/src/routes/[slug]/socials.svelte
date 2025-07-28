<script>
	import { Icon } from '$lib/macro';
	let { links = {}, name = '' } = $props();

	let icons = ['whatsapp', 'linkedin', 'twitter', 'facebook', 'instagram'];
</script>

{#if Object.keys(links).length > 0}
	<div class="block">
		{#each Object.entries(links) as [key, value] (key)}
			<a
				href={key != 'whatsapp' ? value : `https://wa.me/${value}/?text=Hello%20${name}`}
				target="_blank"
				rel="noopener noreferrer"
			>
				<Icon icon={icons.includes(key) ? key : 'link'} />
			</a>
		{/each}
	</div>
{/if}

<style>
	.block {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp0);
		margin: var(--sp2) 0;

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

		transition:
			background-color var(--trans),
			fill var(--trans);
	}

	a:hover {
		fill: var(--ft1_b);
		background-color: var(--button);
	}
</style>
