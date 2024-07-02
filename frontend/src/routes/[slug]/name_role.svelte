<script>
	import Avatar from '$lib/avatar.svelte';

	export let user;
</script>

<div class="block">
	<div class="content">
		<div class="avatar_place">
			<div class="avatar">
				<Avatar name={user.firstname} photo={user.photo} size="148" square />
			</div>
		</div>

		<div class="name_role">
			<strong class="ititle">
				{user.firstname}
				{user.lastname}
			</strong>
			{#if user.role}
				{user.role}
			{/if}
		</div>
	</div>
</div>

<style>
	.block {
		background-color: var(--bg2);
	}

	.content {
		max-width: var(--mobileWidth);
		width: 100%;
		margin: auto;

		display: flex;
		gap: var(--sp3);
		padding: var(--sp3);

		flex-wrap: wrap;
	}

	.name_role {
		display: flex;
		flex-direction: column;
		justify-content: flex-end;
	}

	.ititle {
		color: var(--ft1);
		font-size: x-large;
	}

	.avatar_place {
		position: relative;
		width: 148px;
		flex-shrink: 0;
	}

	.avatar {
		bottom: 0;

		outline: 8px solid var(--bg2);
		outline-offset: -4px;
		border-radius: var(--sp1);
		line-height: 0;
	}

	@media screen and (min-width: 500px) {
		.avatar {
			position: absolute;
		}
	}
</style>
