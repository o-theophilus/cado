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
	let open = null;
</script>

<Meta title={user?.firstname || data.error} />

<div class="bg">
	<Content>
		<div class="title">
			<div class="left">
				<Back />
				<strong class="ititle"> Setting </strong>
			</div>
		</div>

		<Photo
			{user}
			open={open == 'photo'}
			on:open={() => {
				open = 'photo';
			}}
		/>
		<Personal
			{user}
			open={open == 'personal'}
			on:open={() => {
				open = 'personal';
			}}
		/>
		<Organization
			{user}
			open={open == 'organization'}
			on:open={() => {
				open = 'organization';
			}}
		/>
		<Contact
			{user}
			open={open == 'contact'}
			on:open={() => {
				open = 'contact';
			}}
		/>
		<Social
			{user}
			open={open == 'social'}
			on:open={() => {
				open = 'social';
			}}
		/>

		<!-- <br /> -->
		<hr />
		<!-- <br /> -->
		<strong class="ititle title"> Advanced </strong>

		<Email
			open={open == 'email'}
			on:open={() => {
				open = 'email';
			}}
		/>
		<Password
			open={open == 'password'}
			on:open={() => {
				open = 'password';
			}}
		/>
		<Delete
			open={open == 'delete'}
			on:open={() => {
				open = 'delete';
			}}
		/>
	</Content>
</div>

<style>
	.title {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: var(--sp3);
	}
	.left {
		display: flex;
		align-items: center;
		gap: var(--sp2);
	}
	.bg {
		padding: var(--sp3) 0;
		background-color: var(--bg2);
	}

	hr {
		margin: var(--sp3) 0;
	}
</style>
