<script>
	import { user } from '$lib/store.svelte.js';

	import { Meta, Icon } from '$lib/macro';
	import { RoundButton } from '$lib/button';
	import { Row } from '$lib/layout';
	import Org from './org.svelte';

	let { data } = $props();
	let org = data.org;
</script>

<Meta title={org.fullname || org.name} description={org.about} />

<section class="content">
	<Row space>
		<div class="page_title">Organization</div>

		{#if org.user_key == user.value.key}
			<Row --row-gap="8px">
				<RoundButton title="settings" href="/@{org.slug}/card" large>
					<Icon icon="card" size="1.2"></Icon>
				</RoundButton>
				<RoundButton title="settings" href="/@{org.slug}/setting" large>
					<Icon icon="settings" size="1.2"></Icon>
				</RoundButton>
			</Row>
		{/if}
	</Row>

	<br />
	<br />

	<Org {org}></Org>
</section>

<style>
	.content {
		position: relative;

		max-width: var(--mobileWidth);
		width: 100%;
		margin: auto;
		padding: var(--sp2);
		padding-bottom: var(--sp4);
	}
</style>
