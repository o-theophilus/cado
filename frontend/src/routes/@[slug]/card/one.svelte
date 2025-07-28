<script>
	import { Button, Tag, RoundButton } from '$lib/button';
	import Avatar from '$lib/avatar.svelte';
	import Icon from '$lib/icon.svelte';

	let { card, selected, card_status } = $props();

	const color = () => {
		if (card.status == 'pending') return 'var(--cl4)';
		if (card.status == 'live') return 'var(--cl3)';
		return '';
	};
</script>

<div class="card">
	<a href="/{card.key}">
		<Avatar name="{card.firstname} {card.lastname}" photo={card.photo} size="100" square />
		<div class="details">
			<div class="name">{card.firstname} {card.lastname}</div>
			<div>{card.email}</div>
			<div>{card.job_title}</div>
		</div>
	</a>

	<div class="actions">
		<Tag
			onclick={() => selected.add(card.key)}
			--button-outline-color={color()}
			--button-color={color()}
		>
			{card.status}
		</Tag>
	</div>

	{#if selected.check(card.key)}
		<div class="dialog">
			<div class="block">
				<span> Change Status </span>
				<div class="buttons">
					<Button no_grow onclick={() => card_status('live')}>
						Accept {selected.value.length > 1 ? 'All' : ''}
					</Button>
					<Button no_grow onclick={() => card_status('draft')}>
						Cancel {selected.value.length > 1 ? 'All' : ''}
					</Button>
					<RoundButton onclick={() => selected.remove(card.key)}>
						<Icon icon="close"></Icon>
					</RoundButton>
				</div>
			</div>
		</div>
	{/if}
</div>

<style>
	.card {
		position: relative;
		display: flex;
		gap: var(--sp2);
		align-items: center;
		border-bottom: 2px solid var(--bg2);
		padding: var(--sp2) 0;
	}

	.card .block {
		display: flex;
		gap: var(--sp1);
		align-items: center;
		justify-content: space-between;
		width: 100%;
	}

	a {
		display: flex;
		gap: var(--sp1);
		align-items: center;
		width: 100%;
		text-decoration: none;
		color: var(--ft2);
		border-right: 2px solid var(--bg2);
	}

	.details {
		font-size: 0.9rem;
		/* width: 100%; */
	}
	.name {
		font-weight: 800;
	}

	.dialog {
		position: absolute;
		inset: 0 -16px;

		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;

		backdrop-filter: blur(4px);
		background-color: rgba(255, 255, 255, 0.7);
	}
	.dialog .block {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: var(--sp1);
		justify-content: center;
		width: 100%;
	}

	.buttons {
		display: flex;
		gap: var(--sp1);
		align-items: center;
	}
</style>
