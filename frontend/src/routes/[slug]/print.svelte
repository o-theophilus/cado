<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { organization, to_print } from '$lib/store.js';

	import QRCode from 'qrcode';
	import Icon from '$lib/icon.svelte';

	export let user;

	onMount(() => {
		QRCode.toDataURL(
			$page.url.href,
			{
				margin: 3
			},
			(error, url) => {
				if (error) console.error(error);
				src = url;
			}
		);
	});

	let src = '';

	window.onafterprint = () => {
		$to_print = null;
	};
</script>

<div class="print_area">
	<div class="block">
		<div class="card back">
			<div class="row2">
				<img src="/logo.png" alt="logo" />
				<span class="slogan">
					Wragby Business Solutions & Technologies Limited
					<br />
					Work smart, achieve more.
				</span>
			</div>

			<div class="row3">
				<Icon icon="language" size="1.2" />
				{$organization.website}
			</div>
			<div class="row4" />
		</div>

		<div class=" card front">
			<div class="col1">
				<img src="/logo.png" alt="logo" />
				<div class="slogan">Work Smart, Achieve More</div>
				<img class="qr" {src} alt="qr_code" />
			</div>

			<div class="col2">
				<div />
				<div />
			</div>
			<div class="col3">
				<div class="details">
					<div class="name">
						{user.firstname}
						{user.lastname}
					</div>

					{#if user.role}
						<div>
							{user.role}
						</div>
					{/if}

					<div class="divider" />

					{#if user.phone}
						<div class="phone">
							<div class="icon">
								<Icon icon="phone" size="1.2" />
							</div>
							{user.phone}
						</div>
					{/if}

					<div class="email">
						<div class="icon">
							<Icon icon="email" size="1.2" />
						</div>
						{user.email}
					</div>

					{#each $organization.address as a}
						{#if a.name == user.office_location}
							<div class="location">
								<div class="icon">
									<Icon icon="location_on" size="1.2" />
								</div>
								{a.address}
							</div>
						{/if}
					{/each}
				</div>
			</div>
		</div>
	</div>
</div>

<style>
	* {
		-webkit-print-color-adjust: exact !important;
		print-color-adjust: exact !important;

		font-size: 10px;
	}

	.block {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		gap: var(--sp2);

		padding: var(--sp2);

		background-color: gray;
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

	.row2 {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		color: var(--ft1_b);
		height: 100%;
		gap: var(--sp1);
	}
	.row2 img {
		width: 50%;
	}

	.row3 {
		display: flex;
		justify-content: center;
		align-items: center;
		gap: var(--sp1);
		color: var(--ft1_b);
		padding-bottom: var(--sp1);
	}

	.row4 {
		height: 10%;
		flex-shrink: 0;
		background-color: var(--cl1);
	}

	.front {
		display: flex;
	}

	.col1 {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;

		background-color: var(--bg2);
		padding: var(--sp2);

		width: 40%;
		flex-shrink: 0;
	}
	.col1 img {
		width: 100%;
	}
	.col1 .qr {
		width: 50%;
	}

	.col2 {
		display: flex;
		flex-direction: column;
		justify-content: space-between;

		width: 12px;
	}

	.col2 div {
		height: 24px;
		width: 100%;
	}

	.col3 {
		padding: var(--sp2);
		width: 100%;

		display: flex;
		align-items: center;
	}

	.slogan {
		font-size: xx-small;
		text-align: center;
	}

	.name {
		font-weight: 800;
		font-size: medium;
		color: var(--ft1);
	}

	.divider {
		background-color: var(--cl1);
		height: 2px;
		width: 100px;
		margin: 12px 0;
	}

	.icon {
		--size: 14px;

		display: flex;
		justify-content: center;
		align-items: center;

		flex-shrink: 0;

		width: var(--size);
		height: var(--size);
		border-radius: 50%;
		background-color: var(--ft1);
		color: white;
	}

	.phone,
	.email,
	.location {
		display: flex;
		gap: var(--sp2);
		margin: var(--sp0) 0;
	}

	@media print {
		.card {
			width: 400px;
		}
	}
</style>
