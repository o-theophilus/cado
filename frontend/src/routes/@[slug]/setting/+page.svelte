<script>
	import Meta from '$lib/meta.svelte';
	import { BRound } from '$lib/button';
	import Icon from '$lib/icon.svelte';

	import Photo from '../../[slug]/setting/photo.svelte';
	import Info from './info.svelte';
	import Contact from './contact.svelte';
	import Social from '../../[slug]/setting/social.svelte';
	import Domain from './domain.svelte';
	import Slug from './slug.svelte';
	import Email from '../../[slug]/setting/email/index.svelte';
	import Delete from '../../[slug]/setting/delete.svelte';

	let { data } = $props();
	let org = $state(data.org);
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
		org = n;
	};
</script>

<Meta title={org.firstname} />

<section class="page">
	<div class="hline">
		<div class="hline">
			<BRound icon="arrow_back" href="/@{org.slug}">
				<Icon icon="arrow_back" size="1.2"></Icon>
			</BRound>
			<div class="page_title">Organization Setting</div>
		</div>
	</div>

	<br />

	<Info {org} bind:active_card {update} />
	<Photo entity={org} _type="org" bind:active_card {update} />
	<Contact {org} bind:active_card {update} />
	<Social entity={org} _type="org" bind:active_card {update} />
	<Domain {org} bind:active_card {update} />

	<br />
	<div class="page_title">Advanced</div>
	<br />

	<Slug {org} bind:active_card {update} />
	<Email entity={org} _type="org" bind:active_card {update} />
	<Delete entity={org} _type="org" bind:active_card />
</section>

<style>
	.page {
		max-width: var(--mobileWidth);
		width: 100%;
		margin: auto;
		padding: var(--sp2);
	}
</style>
