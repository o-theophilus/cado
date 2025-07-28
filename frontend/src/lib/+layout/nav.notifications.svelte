<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';

	import { token } from '$lib/store.svelte.js';
	import { Icon } from '$lib/macro';
	import { Button } from '$lib/button';
	import { onMount } from 'svelte';

	let nots = $state([]);

	const format = (x) => {
		if (x._type == 'org_card_join_request') {
			x.message = `${x.info.count} card join request.`;
			x.href = `/@${x.info.slug}/card?status=pending`;
		}
		return x;
	};

	const submit = async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/notification`, {
			headers: {
				'Content-Type': 'application/json',
				Authorization: token.value
			}
		});
		resp = await resp.json();

		if (resp.status == 200) {
			nots = resp.nots.map((x) => format(x));
		}
	};

	onMount(async () => {
		await submit();
	});

	let open = $state(false);
	let self = $state(false);
</script>

<svelte:window
	onclick={() => {
		if (open && !self) {
			open = false;
		}
		self = false;
	}}
/>

{#if nots.length > 0}
	<Button
		--button-width="20px"
		--button-height="20px"
		--button-padding-x="0"
		--button-border-radius="50%"
		--button-background-color="transparent"
		--button-color="var(--ft1)"
		onclick={() => {
			open = !open;
			self = true;
		}}
	>
		<div class="new"></div>
		<Icon icon="notify"></Icon>

		{#if open}
			<div class="nots" transition:slide={{ delay: 0, duration: 200, easing: cubicInOut }}>
				{#each nots as n}
					<a href={n.href}>
						{n.message}
					</a>
				{/each}
			</div>
		{/if}
	</Button>
{/if}

<style>
	.new {
		--size: 6px;

		flex-shrink: 0;
		position: absolute;
		top: 0px;
		right: 0px;

		width: var(--size);
		height: var(--size);
		border-radius: 50%;
		background-color: var(--cl2);
	}

	.nots {
		position: absolute;
		top: 100%;
		right: 0;
		z-index: 1;

		display: flex;
		flex-direction: column;

		width: 160px;
		overflow: hidden;
		background-color: var(--bg1);
		border-radius: var(--sp0);
		box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
	}

	a {
		padding: var(--sp0) var(--sp2);

		font-size: 0.8rem;
		font-weight: 500;
		text-decoration: none;
		color: var(--ft1);
		background-color: transparent;

		transition: background-color var(--trans);
	}
	a:not(:last-child) {
		border-bottom: 2px solid var(--bg2);
	}

	a:hover {
		background-color: var(--bg2);
	}
</style>
