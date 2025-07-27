<script>
	import { Meta } from '$lib/page';
	import { BackButton } from '$lib/button';
	import { Row } from '$lib/layout';

	import Photo from './photo.svelte';
	import Info from './info.svelte';
	import Contact from './contact.svelte';
	import Social from './social.svelte';
	import Org from './org/index.svelte';
	import Email from './email/index.svelte';
	import Delete from './delete/index.svelte';

	let { data } = $props();
	let card = $state(data.card);

	let active_card = $state({
		value: null,
		set(v) {
			if (this.value == v) {
				this.value = null;
			} else {
				this.value = v;
			}
		},
		close() {
			this.value = null;
		}
	});

	const update = (n) => {
		card = n;
	};
</script>

<Meta title={card.firstname} />

<section class="page">
	<Row>
		<BackButton href="/{card.key}">
			<Icon icon="arrow_back" size="1.2"></Icon>
		</BackButton>
		<div class="page_title">Card Setting</div>
	</Row>

	<br />

	<Info {card} bind:active_card {update} />
	<Photo entity={card} _type="card" bind:active_card {update} />
	<Contact {card} bind:active_card {update} />
	<Social entity={card} _type="card" bind:active_card {update} />

	<br />
	<div class="page_title small">Advanced</div>

	<Org {card} bind:active_card {update} />
	<Email entity={card} type="card" bind:active_card {update} />
	<Delete entity={card} type="card" bind:active_card />
</section>

<style>
	.page {
		max-width: var(--mobileWidth);
		width: 100%;
		margin: auto;
		padding: var(--sp2);
	}

	.small {
		font-size: medium;
	}
</style>
