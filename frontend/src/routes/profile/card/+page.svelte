<script>
	import { module, user } from '$lib/store.svelte.js';
	import Button from '$lib/button/button.svelte';
	import Tag from '$lib/button/tag.svelte';
	import BRound from '$lib/button/round.svelte';
	import Icon from '$lib/icon.svelte';
	import Add from './_add.svelte';
	import Empty from '../empty.svelte';

	let { data } = $props();
	let cards = data.cards;

	const add = () => {
		module.open(Add, {
			email: user.value.email,
			firstname: user.value.firstname,
			lastname: user.value.lastname
		});
	};
	console.log(cards);
</script>

<div class="line">
	<div class="page_title">
		My Business Card{#if cards.length > 1}s{/if}
	</div>

	<Button size="small" onclick={add}>
		<Icon icon="add" />
		Add
	</Button>
</div>

<br />

{#snippet card(c)}
	<a href="/{c.key}" class="card">
		<div class="hline">
			<Tag no_grow>
				{c.status}
			</Tag>
			<!-- <BRound icon="settings" href="/{card.key}/setting" /> -->
		</div>

		<div class="name">
			{c.firstname}
			{c.lastname}
		</div>
		<div class="role">
			{c.job_title}
		</div>

		{#if c.status == 'live'}
			@ {c.org.name}
		{/if}
	</a>
{/snippet}

{#if cards && cards.length > 0}
	<div class="cards">
		{#each cards as c}
			{@render card(c)}
		{/each}
	</div>
{:else}
	<Empty>
		No business cards available.
		<Button onclick={add}>
			<Icon icon="add" />
			Add Now
		</Button>
	</Empty>
{/if}

<style>
	.line {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.cards {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: var(--sp2);
		padding-bottom: var(--sp2);

		width: 100%;
	}

	@media (max-width: 600px) {
		.cards {
			grid-template-columns: 1fr;
		}
	}

	.card {
		border: 2px solid transparent;
		border-radius: 8px;
		padding: var(--sp2);

		aspect-ratio: 16 / 9;

		text-decoration: none;
		color: var(--ft1);
		box-shadow: 0 2px 8px rgb(200, 200, 200);
		/* background-color: var(--bg2); */

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
</style>
