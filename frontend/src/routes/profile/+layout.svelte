<script>
	import { page } from '$app/state';
	import { Button, RoundButton } from '$lib/button';
	import { Row } from '$lib/layout';
	import Icon from '$lib/icon.svelte';

	let { children } = $props();
</script>

{#snippet button(href, icon)}
	<Button
		{href}
		--button-width="4rem"
		--button-height="4rem"
		--button-background-color={page.route.id == href ? 'var(--bg2)' : 'transparent'}
		--button-background-color-hover="var(--bg2)"
		--button-color={page.route.id == href ? 'var(--ft1)' : 'var(--ft2)'}
		--button-color-hover="var(--ft1)"
	>
		<Icon {icon} size="2" />
	</Button>
{/snippet}

<nav>
	<div class="pos">
		<Row space>
			<div>
				{@render button('/profile', 'person')}
				{@render button('/profile/card', 'card')}
				{@render button('/profile/org', 'corporate_fare')}
			</div>

			{#if page.route.id == '/profile'}
				<RoundButton icon="settings" tooltip="settings" href="/profile/setting">
					<Icon icon="settings" size="1.2"></Icon>
				</RoundButton>
			{/if}
		</Row>
	</div>
</nav>

<div class="page">
	<!-- <br /> -->
	{@render children()}
</div>

<style>
	nav {
		border-bottom: 1px solid var(--bg2);
	}

	.page,
	.pos {
		max-width: var(--mobileWidth);
		width: 100%;
		margin: auto;
		padding: var(--sp2);
	}

	.pos {
		padding: var(--sp1) var(--sp2);
	}
</style>
