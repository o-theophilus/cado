<script>
	import { Icon } from '$lib/macro';

	let { value = $bindable(), list } = $props();

	const remove = (n) => {
		const { [n]: _, ...rest } = value;
		value = rest;
	};
</script>

<div class="social_block">
	{#each Object.entries(value) as [key, value] (key)}
		<div class="social">
			<a
				href={key != 'whatsapp' ? value : `https://wa.me/${value}/?text=Hello%20${name}`}
				target="_blank"
				rel="noopener noreferrer"
			>
				<Icon icon={list.includes(key) ? key : 'link'} />

				{key}
			</a>

			<button
				onclick={() => {
					remove(key);
				}}
			>
				<Icon icon="close" />
			</button>
		</div>
	{:else}
		<div class="empty">No Social Link</div>
	{/each}
</div>

<style>
	.social_block {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp1);
		margin-top: var(--sp2);
	}
	.social {
		display: flex;
		flex-wrap: wrap;
		gap: 1px;

		border-radius: var(--sp0);
		overflow: hidden;
	}

	a {
		display: flex;
		align-items: center;
		gap: var(--sp1);

		padding: var(--sp1);

		background-color: var(--bg2);
		color: var(--ft1);
		fill: currentColor;
		text-decoration: none;

		transition:
			background-color var(--trans),
			color var(--trans);
	}

	a:hover {
		color: var(--ft1_b);
		background-color: var(--button);
	}

	button {
		--size: 40px;

		display: flex;
		align-items: center;
		justify-content: center;

		width: var(--size);
		height: var(--size);

		border: none;
		background-color: var(--bg2);

		transition:
			background-color var(--trans),
			fill var(--trans);
	}
	button:hover {
		fill: var(--ft1_b);
		background-color: var(--red);
	}

	.empty {
		background-color: var(--bg2);
		padding: var(--sp2);
		border-radius: var(--sp0);
		width: 100%;
		text-align: center;
	}
</style>
