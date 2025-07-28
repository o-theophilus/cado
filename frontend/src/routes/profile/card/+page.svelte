<script>
	import { module, user } from '$lib/store.svelte.js';
	import { Button } from '$lib/button';
	import { Row } from '$lib/layout';
	import { Meta } from '$lib/page';
	import Icon from '$lib/icon.svelte';
	import Add from './_add.svelte';
	import One from './one.svelte';
	import Note from '$lib/note.2.svelte';

	let { data } = $props();
	let cards = data.cards;

	const add = () => {
		module.open(Add, {
			email: user.value.email,
			firstname: user.value.firstname,
			lastname: user.value.lastname
		});
	};
</script>

<Meta title="{user.value.firstname} {user.value.lastname} - Card" />

<Row space>
	<div class="page_title">
		My Business Card{#if cards.length > 1}s{/if}
	</div>

	<Button size="small" onclick={add}>
		<Icon icon="add" />
		Add
	</Button>
</Row>

<br />

{#if cards && cards.length > 0}
	<div class="cards">
		{#each cards as card}
			<One {card} />
		{/each}
	</div>
{:else}
	<Note>
		No business card available
		<Button onclick={add}>
			<Icon icon="add" />
			Add Now
		</Button>
	</Note>
{/if}

<style>
	.cards {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: var(--sp2);
		padding-bottom: var(--sp2);

		width: 100%;
	}

	@media (max-width: 600px) {
		.cards {
			grid-template-columns: 1fr;
		}
	}
</style>
