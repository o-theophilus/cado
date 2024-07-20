<script>
	import Content from '$lib/content.svelte';
	import Meta from '$lib/meta.svelte';
	import Back from '$lib/button/back.svelte';

	import Photo from './photo.svelte';
	import Personal from './personal.svelte';
	import Organization from './organization.svelte';
	import Contact from './contact.svelte';
	import Social from './social.svelte';
	import Email from './email/index.svelte';
	import Password from './password/index.svelte';
	import Delete from './delete.svelte';

	export let data;
	let user = data.user;
</script>

<Meta title={user?.firstname || data.error} />

<Content>
	<div class="title">
		<div class="left">
			<Back />
			<strong class="ititle"> Setting </strong>
		</div>
	</div>

	<Photo {user} />
	<Personal {user} />
	<Organization {user} />
	<Contact {user} />
	<Social {user} />
	<Email />
	<Password />
	<Delete />
</Content>

<style>
	.title {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	.left {
		display: flex;
		align-items: center;
		gap: var(--sp2);
	}
</style>
