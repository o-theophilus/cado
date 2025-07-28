<script>
	import { user } from '$lib/store.svelte.js';

	import { Meta } from '$lib/page';

	import Photo from '../../[slug]/setting/photo.svelte';
	import Info from './info.svelte';
	import Contact from './contact.svelte';
	import Email from './email/index.svelte';
	import Password from './password/index.svelte';
	import Delete from './delete/index.svelte';

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

<Meta title="{user.value.firstname} {user.value.lastname} - Setting" />

<div class="page_title">Setting</div>

<br />

<Info {user} bind:active_card {update} />
<Photo entity={user.value} _type="user" bind:active_card {update} />
<Contact {user} bind:active_card {update} />

<br />
<div class="page_title mod">Advanced</div>

<Email bind:active_card {update} />
<Password bind:active_card />
<Delete {user} bind:active_card />

<style>
	.mod {
		font-size: medium;
	}
</style>
