<script>
	import Icon from '$lib/icon.svelte';
	let { org } = $props();

	let width = $state(80);
	let height = $state(80);
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

<a href="/@{org.slug}">
	<div class="img">
		{#if org.photo}
			<img
				src={org.photo || '/no_photo.png'}
				alt={org.name}
				style:max-width="{width}px"
				onerror={() => (org.photo = null)}
			/>
		{:else}
			<Icon icon="corporate_fare" size="4" />
		{/if}
	</div>

	{#if org.photo}{/if}

	<div class="details">
		<div class="name">
			{org.fullname}
		</div>
		<div class="email">
			{org.email}
		</div>
	</div>
</a>

<style>
	a {
		display: flex;
		gap: var(--sp2);
		align-items: center;
		flex-wrap: wrap;

		fill: currentColor;
		color: var(--ft2);
		padding: var(--sp2);
		border-radius: var(--sp0);
		border: 2px solid var(--ft2_b);
		text-decoration: none;
		background-color: transparent;

		transition: background-color var(--trans);
	}

	a:hover {
		background-color: var(--ft1_b);
	}

	img {
		width: 100%;
	}
	.name {
		font-weight: 800;
		font-size: 1rem;
		color: var(--ft1);
	}

	.email {
		word-break: break-all;
		overflow-wrap: anywhere;
	}
</style>
