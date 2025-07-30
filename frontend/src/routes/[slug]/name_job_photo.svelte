<script>
	import { Avatar } from '$lib/macro';
	let { card } = $props();
</script>

<div class="block">
	<div class="content">
		<div class="avatar_place">
			<div class="avatar">
				<Avatar name="{card.firstname} {card.lastname}" photo={card.photo} size="148" />
			</div>
		</div>

		<div class="name_job_title">
			<div class="name">
				{card.firstname}
				{card.lastname}
			</div>
			{#if card.job_title}
				{card.job_title}
			{/if}
		</div>
	</div>
</div>

<style>
	.block {
		background-color: var(--bg2);
	}

	.content {
		max-width: var(--mobileWidth);
		width: 100%;
		margin: auto;

		display: flex;
		gap: var(--sp3);
		padding: var(--sp3);

		flex-wrap: wrap;
	}

	.avatar_place {
		position: relative;
		width: 148px;
		flex-shrink: 0;
	}

	.avatar {
		bottom: 0;

		outline: 8px solid var(--bg2);
		outline-offset: -4px;
		border-radius: var(--sp1);
		background-color: var(--bg1);
	}

	@media screen and (min-width: 300px) {
		.avatar_place {
			height: 45px;
		}
		.avatar {
			position: absolute;
		}
	}

	.name_job_title {
		display: flex;
		flex-direction: column;
		justify-content: flex-end;
	}

	.name {
		font-size: 1.5rem;
		font-weight: 800;
		color: var(--ft1);
	}
</style>
