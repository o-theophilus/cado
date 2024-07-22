<script>
	import Avatar from '$lib/avatar.svelte';
	export let org;
</script>

<a href="/organization/{org.slug}">
	<Avatar name={org.name} photo={org.photo} />
	<div class="details">
		<div class="name">
			{org.name}
		</div>

		<span>
			{org.email}
		</span>
	</div>
</a>

<style>
	a {
		display: flex;
		align-items: center;
		gap: var(--sp2);

		margin: var(--sp2) 0;
		padding-top: var(--sp2);
		border-top: 2px solid var(--input);

		text-decoration: none;
		color: var(--ft2);
	}
	a:hover {
		text-decoration: none;
	}

	.details {
		width: 100%;
	}

	.name {
		font-weight: 700;
		color: var(--ft1);
	}

	span {
		word-wrap: break-word;
		word-break: break-all;
	}
</style>
