<script>
	import { module } from '$lib/store.svelte.js';
	import Button from '$lib/button/button.svelte';
	import BRound from '$lib/button/round.svelte';
	import Icon from '$lib/icon.svelte';
	import Add from './_add.svelte';
	import Note from '$lib/note.2.svelte';

	let { data } = $props();
	let orgs = data.orgs;

	const add = () => {
		module.open(Add);
	};
</script>

<div class="hline">
	<div class="page_title">
		Organization{#if orgs.length > 1}s{/if}
	</div>

	<Button size="small" onclick={add}>
		<Icon icon="add" />
		Add
	</Button>
</div>
<br />

{#if orgs && orgs.length > 0}
	<div class="cards">
		{#each orgs as org}
			<div class="card">
				<div class="menu">
					<BRound icon="card" href="/@{org.slug}/card"></BRound>
					<BRound icon="settings" href="/@{org.slug}/setting"></BRound>
				</div>
				<a href="/@{org.slug}">
					<div class="img">
						{#if org.photo}
							<img src={org.photo} alt="org logo" />
						{:else}
							<Icon icon="corporate_fare" size="8" />
						{/if}
					</div>
				</a>
				<a href="/@{org.slug}">
					{#if org.fullname}
						{org.fullname}
					{:else}
						{org.name}
					{/if}
				</a>
			</div>
		{/each}
	</div>
{:else}
	<Note>
		No organization available
		<Button onclick={add}>
			<Icon icon="add" />
			Add Now
		</Button>
	</Note>
{/if}

<style>
	.cards {
		display: grid;
		grid-template-columns: repeat(1, 1fr);
		gap: var(--sp2);

		width: 100%;
	}

	@media (min-width: 451px) and (max-width: 650px) {
		.cards {
			grid-template-columns: repeat(2, 1fr);
		}
	}

	@media (min-width: 651px) {
		.cards {
			grid-template-columns: repeat(3, 1fr);
		}
	}

	.card {
		position: relative;

		display: flex;
		flex-direction: column;

		text-decoration: none;
		color: var(--ft1);

		transition: border-color var(--trans);
	}

	a {
		text-decoration: none;
		color: var(--ft1);
	}

	.img {
		display: flex;
		align-items: center;
		justify-content: center;

		border: 2px solid var(--bg2);
		border-radius: 8px;
		padding: var(--sp2);
		aspect-ratio: 1;
		fill: var(--bg2);
	}
	img {
		width: 100%;
		object-fit: contain;
	}

	.card:hover .img {
		border-color: var(--ft2);
	}

	.menu {
		position: absolute;
		top: var(--sp1);
		right: var(--sp1);

		display: flex;
		gap: var(--sp0);
	}
</style>
