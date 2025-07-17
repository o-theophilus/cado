<script>
	import { user } from '$lib/store.svelte.js';

	import Meta from '$lib/meta.svelte';
	import Icon from '$lib/icon.svelte';
	import Link from '$lib/button/link.svelte';

	import Avatar from '$lib/avatar.svelte';
	import BRound from '$lib/button/round.svelte';
</script>

<Meta title="{user.value.firstname} Profile" />

<section class="content">
	<div class="hline">
		<div class="page_title">Profile</div>
		<BRound icon="settings" tooltip="settings" href="/profile/setting" large></BRound>
	</div>
	<br />

	<div class="info">
		<Avatar
			name="{user.value.firstname} {user.value.lastname}"
			photo={user.value.photo}
			size="200"
			square
		/>

		<div class="name">
			{user.value.firstname}
			{user.value.lastname}
		</div>

		<div class="contact">
			{#if user.value.phone}
				<span class="group">
					<Icon icon="call" size="1.2" />
					<div>
						<div class="label">Phone:</div>
						<Link href="tel:{user.value.phone}">{user.value.phone}</Link>
					</div>
				</span>
			{/if}

			<div class="group">
				<Icon icon="email" size="1.2" />
				<div>
					<div class="label">Email:</div>
					<Link href="mailto:{user.value.email}">
						<span class="email">
							{user.value.email}
						</span>
					</Link>
				</div>
			</div>
		</div>
	</div>
</section>

<style>
	.content {
		width: 100%;
	}

	.info {
		display: flex;
		flex-direction: column;
		gap: var(--sp3);
	}
	
	@media screen and (min-width: 600px) {
		.info {
			align-items: center;
		}
	}

	.name {
		font-size: xx-large;
		font-weight: 700;
		color: var(--ft1);
	}

	.group {
		display: flex;
		gap: 0 var(--sp2);
		align-items: flex-start;
		margin: var(--sp2) 0;
	}

	.label {
		font-size: small;
	}

	.email {
		word-break: break-all;
		overflow-wrap: anywhere;
	}
</style>
