<script>
	import { page } from '$app/state';
	import Meta from '$lib/meta.svelte';
	import Icon from '$lib/icon.svelte';
	import Button from '$lib/button/button.svelte';

	let error = page.error.message;
</script>

<Meta title={error} description={error.message} />

<section class="page">
	<div class="page_title">{page.status}</div>
	<br />
	{error}

	<br />
	<br />

	<img src="/error.png" alt="error" />

	<br />
	<br />

	<Button href="/">
		<Icon icon="home" />
		Back to Home
	</Button>
</section>

<style>
	.page {
		max-width: var(--mobileWidth);
		width: 100%;
		margin: auto;
		padding: var(--sp2);
	}
	img {
		width: 100%;
	}
</style>
