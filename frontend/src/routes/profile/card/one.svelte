<script>
	import { RoundButton, Tag } from '$lib/button';
	import { Icon } from '$lib/macro';

	let { card } = $props();
	const color = () => {
		if (card.status == 'pending')
			return ['var(--cl4)', 'color-mix(in srgb, var(--cl4), white 90%)'];
		if (card.status == 'live') return ['var(--cl3)', 'color-mix(in srgb, var(--cl3), white 90%)'];
		return ['', 'transparent'];
	};
	let clr = color();
</script>

<a href="/{card.key}" class="card">
	<Tag --button-outline-color={clr[0]} --button-color={clr[0]} --button-background-color={clr[1]}>
		{card.status}
	</Tag>

	<div class="right">
		<RoundButton href="/{card.key}/setting">
			<Icon icon="settings" />
		</RoundButton>
	</div>
	<div class="name">
		{card.firstname}
		{card.lastname}
	</div>
	<div class="role">
		{card.job_title}
	</div>

	{#if card.status == 'live'}
		@ {card.org.name}
	{/if}
</a>

<style>
	.card {
		position: relative;

		border: 2px solid transparent;
		border-radius: 8px;
		padding: var(--sp2);

		/* aspect-ratio: 16 / 9; */

		text-decoration: none;
		color: var(--ft1);
		box-shadow: 0 2px 8px rgb(200, 200, 200);
		/* background-color: var(--bg2); */
		/* width: 100%; */

		transition: border-color var(--trans);
	}

	.card:hover {
		border-color: var(--ft2);
	}

	.name {
		font-weight: 800;
		margin-top: var(--sp2);
	}

	.role {
		font-size: small;
	}

	.right {
		position: absolute;
		top: var(--sp2);
		right: var(--sp2);
	}
</style>
