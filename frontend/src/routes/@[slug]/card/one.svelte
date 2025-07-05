<script>
	import Tag from '$lib/button/tag.svelte';
	import BRound from '$lib/button/round.svelte';
	import Avatar from '$lib/avatar.svelte';

	let { card, selected, status } = $props();
</script>

<div class="card">
	<Avatar name="{card.firstname} {card.lastname}" photo={card.photo} size="100" square />
	<div class="block">
		<div class="details">
			<span>{card.firstname} {card.lastname}</span>
			<span>{card.email}</span>
			<span>{card.job_title}</span>
		</div>
		<Tag no_grow onclick={() => selected.add(card.key)}>
			{card.status}
		</Tag>
	</div>

	{#if selected.check(card.key)}
		<div class="dialog">
			<div class="block">
				<span> Change Status </span>
				<div class="buttons">
					<Tag no_grow onclick={() => status('live')}>
						Accept {selected.value.length > 1 ? 'All' : ''}
					</Tag>
					<Tag no_grow onclick={() => status('draft')}>
						Cancel {selected.value.length > 1 ? 'All' : ''}
					</Tag>
					<BRound icon="close" onclick={() => selected.remove(card.key)}></BRound>
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

	.details {
		display: flex;
		flex-direction: column;
		gap: var(--sp1);
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
