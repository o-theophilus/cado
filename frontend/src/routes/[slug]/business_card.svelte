<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { organization } from '$lib/store.js';

	import QRCode from 'qrcode';
	import Icon from '$lib/icon.svelte';

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

	let card_width=400

</script>




	<div class="block" style:font-size="{(0.6 * card_width)/400}rem">
		<div class="card front" bind:clientWidth={card_width}>
			<div class="row1">
				<div class="left">
					<div class="name" style:font-size="{(1.2 * card_width)/400}rem">
						{user.firstname}
						{user.lastname}
					</div>

					{#if user.role}
						<div>
							{user.role}
						</div>
					{/if}
				</div>
				<img class="qr" {src} alt="qr_code" />
			</div>

			<div class="divider" />

			<div class="row2" 
			style:--size="{card_width/400}rem">
				<div class="left">
					{#if user.phone}
						<div class="phone">
							<div class="icon" >
								<Icon icon="phone" />
							</div>
							{user.phone}
						</div>
					{/if}

					<div class="email">
						<div class="icon" >
							<Icon icon="email" />
						</div>
						{user.email}
					</div>

					{#each $organization.address as a}
						{#if a.name == user.office_location}
							<div class="location">
								<div class="icon" >
									<Icon icon="location_on" />
								</div>
								{a.address}
							</div>
						{/if}
					{/each}
				</div>

				<div class="right">
					<img class="logo" src="/logo.png" alt="logo" />
					<div class="slogan">Work Smart, Achieve More</div>
				</div>
			</div>
		</div>

		<div class="card back">
			<div class="row1">
				<img src="/logo.png" alt="logo" />
				<span class="slogan">
					Wragby Business Solutions & Technologies Limited.
					<br />
					Work smart, achieve more.
				</span>
			</div>

			<div class="row2">
				<div class="divider" />
				<Icon icon="language" size="1.2" />
				{$organization.website}
				<div class="divider" />
			</div>
		</div>

	
	</div>




<style>
	* {
		-webkit-print-color-adjust: exact !important;
		print-color-adjust: exact !important;

	}
	
	.block {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		gap: var(--sp2);

		/* font-size: 0.6rem; */

		padding: var(--sp2);

		background-color: var(--bg2);
	}

	.card {
		width: 100%;
		max-width: 400px;
		aspect-ratio: 1000/650;
		flex-shrink: 0;
		background-color: white;
	}

	.back {
		display: flex;
		flex-direction: column;
		background-color: var(--ft1);
	}

	.back .row1 {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		color: var(--ft1_b);
		height: 100%;
		gap: var(--sp1);

		line-height: 1.5;
	}
	.back .row1 img {
		width: 40%;
	}

	.back .row2 {
		display: flex;
		justify-content: center;
		align-items: center;
		gap: var(--sp1);
		flex-shrink: 0;

		height: 15%;

		color: var(--ft1_b);
		fill: currentColor;
		background-color: var(--ft2_d);
	}

	.back .divider {
		background-color: var(--cl1);
		height: 2px;
		width: 100%;
		margin: 12px 0;
	}

	.front {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		padding: var(--sp2);
	}

	.front > div {
		display: flex;
		justify-content: space-between;
		align-items: flex-end;
		gap: var(--sp1);

		width: 100%;
		flex-shrink: 0;
	}
	.front .name {
		font-weight: 800;
		/* font-size: 1.2rem; */
		color: var(--ft1);
	}

	.front .qr {
		width: 15%;
	}

	.front .divider {
		background-color: var(--cl1);
		height: 2px;
		width: 100%;
		margin: 12px 0;
	}

	.front .row2 .left {
		max-width: 13rem;
	}

	.front .row2 .right {
		width: 7rem;

		display: flex;
		flex-direction: column;
		gap: var(--sp1);
		align-items: flex-end;
	}
	.front .logo {
		width: 100%;
	}

	.icon {
		/* --size: 1rem; */

		display: flex;
		justify-content: center;
		align-items: center;

		flex-shrink: 0;

		width: var(--size);
		height: var(--size);
		border-radius: var(--sp0);
		background-color: var(--ft2_d);
		color: white;
	}

	.phone,
	.email,
	.location {
		display: flex;
		gap: var(--sp2);
		margin: var(--sp0) 0;

		fill: currentColor;
	}

	.slogan {
		/* font-size: xx-small; */
		text-align: center;
	}

	@media print {
		.card {
			width: 400px;
		}
	}
</style>
