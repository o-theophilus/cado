<script>
	import { user } from '$lib/store.svelte.js';

	import Meta from '$lib/meta.svelte';
	import BRound from '$lib/button/round.svelte';

	import Photo from '../../[slug]/setting/photo.svelte';
	import Info from './info.svelte';
	import Contact from './contact.svelte';
	import Email from './email/index.svelte';
	import Password from './password/index.svelte';
	import Delete from './delete.svelte';

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
		user.value = n;
	};
</script>

<Meta title={user.value?.firstname} />

<div class=" hline">
	<div class=" hline">
		<BRound icon="arrow_back" href="/profile" />
		<div class="page_title">Setting</div>
	</div>
</div>

<br />

<Info {user} bind:active_card />
<Photo entity={user.value} _type="user" bind:active_card {update} />
<Contact {user} bind:active_card />

<br />
<div class="page_title mod">Advanced</div>

<Email bind:active_card />
<Password bind:active_card />
<Delete {user} bind:active_card />

<style>
	.mod {
		font-size: medium;
	}
</style>
