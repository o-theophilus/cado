<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';

	import { organization } from '$lib/store.js';

	import QRCode from 'qrcode';
	import Icon from '$lib/icon.svelte';
	import Button from '$lib/button/button.svelte';
	import Fold from '$lib/button/fold.svelte';
	import BusinessCard from './business_card.svelte';

	export let user;

	onMount(() => {
		QRCode.toDataURL(
			$page.url.href,
			{
				margin: 0
			},
			(error, url) => {
				if (error) console.error(error);
				src = url;
			}
		);
	});

	let src = '';
	let open = false;

	// window.onafterprint = () => {
	// 	$to_print = null;
	// };
</script>

<hr />
<div class="area">

<div class="line gap">
	<div class="line">
		<Icon icon="credit_card" size="1.2" />
		Business card
	</div>
	<Fold
	{open}
	on:click={() => {
		open = !open;
	}}
	/>
</div>

{#if open}
		<div transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>

			<div class="business_card">
			<BusinessCard {user} />
		</div>


	<Button
		size="small"
		on:click={() => {
			// $to_print = user;
			// setTimeout(() => {
			// 	window.print();
			// });
			// setTimeout(() => {
			// 	$to_print = null;
			// });
		}}
	>
		Save
	</Button>
</div>
{/if}
</div>



<style>
	.area {
		margin: var(--sp2) 0;
	}
	.business_card {
		margin: var(--sp2) 0;
	}
	
	
	.line {
		display: flex;
		align-items: center;
		gap: var(--sp2);
	}

	.gap {
		justify-content: space-between;
	}
	
</style>
