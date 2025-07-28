<script>
	import { module, user } from '$lib/store.svelte.js';
	import { Button, RoundButton } from '$lib/button';
	import { Row, PageNote } from '$lib/layout';
	import { Meta } from '$lib/page';
	import { Icon } from '$lib/macro';
	import Add from './_add.svelte';

	let { data } = $props();
	let orgs = data.orgs;

	const add = () => {
		module.open(Add);
	};
</script>

<Meta title="{user.value.firstname} {user.value.lastname} - Organization" />

<Row space>
	<div class="page_title">
		Organization{#if orgs.length > 1}s{/if}
	</div>

	<Button size="small" onclick={add}>
		<Icon icon="add" />
		Add
	</Button>
</Row>
<br />

{#if orgs && orgs.length > 0}
	<div class="cards">
		{#each orgs as org}
			<a href="/@{org.slug}">
				<div class="menu">
					<!-- <RoundButton href="/@{org.slug}/card">
						<Icon icon="card" size="1.2"></Icon>
					</RoundButton> -->
					<!-- <RoundButton href="/@{org.slug}/setting">
						<Icon icon="settings" size="1.2"></Icon>
					</RoundButton> -->
				</div>
				<div class="img">
					{#if org.photo}
						<img src={org.photo} alt="org logo" />
					{:else}
						<Icon icon="corporate_fare" size="8" />
					{/if}
				</div>
				<span class="name">
					{org.fullname || org.name}
				</span>
			</a>
		{/each}
	</div>
{:else}
	<PageNote>
		No organization available
		<Button onclick={add}>
			<Icon icon="add" />
			Add Now
		</Button>
	</PageNote>
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

	a {
		position: relative;

		display: flex;
		flex-direction: column;

		text-decoration: none;
		color: var(--ft1);
	}
	a:hover .img {
		border-color: var(--ft2);
	}

	.img {
		display: flex;
		align-items: center;
		justify-content: center;

		border: 2px solid var(--bg2);
		border-radius: 8px;
		padding: var(--sp2);
		margin-bottom: var(--sp1);
		aspect-ratio: 1;
		fill: var(--bg2);

		transition: border-color var(--trans);
	}
	img {
		width: 100%;
		object-fit: contain;
	}

	.name {
		font-weight: 800;
		font-size: 1.2rem;
	}

	.menu {
		position: absolute;
		top: var(--sp1);
		right: var(--sp1);

		display: flex;
		gap: var(--sp0);
	}
</style>
