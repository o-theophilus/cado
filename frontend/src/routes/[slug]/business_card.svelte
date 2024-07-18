<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { organization } from '$lib/store.js';

	import * as htmlToImage from 'html-to-image';
	//import { saveAs } from 'file-saver-es';
	import QRCode from 'qrcode';

	import Icon from '$lib/icon.svelte';

	export let user;

	export const download = () => {
		htmlToImage.toBlob(document.getElementById('to_print')).then(function (blob) {
			//saveAs(blob, `${user.firstname} ${user.lastname} business card.png`);
		});
	};



export let ccc = ""
export let ddd = ""

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

htmlToImage.toPng(document.getElementById('to_print')).then(function (dataUrl) {
ccc = dataUrl
			ddd =`${user.firstname} ${user.lastname} business card.png`
		});
	});

	let src = '';

	let cw = 400;
	let _cw = 400;
</script>

<div class="hide">
	<div class="block" id="to_print" style:--size={cw / _cw}>
		<div class="card front" bind:clientWidth={cw}>
			<div class="row1">
				<div class="left">
					<span class="name">
						{user.firstname}&nbsp;{user.lastname}
					</span>

					{#if user.role}
						<br />
						<span class="role">
							{user.role}
						</span>
					{/if}
				</div>
				<img class="qr" {src} alt="qr_code" />
			</div>

			<div class="divider" />

			<div class="row2">
				<div class="left">
					{#if user.phone}
						<div class="phone">
							<div class="icon">
								<Icon icon="call" />
							</div>
							{user.phone}
						</div>
					{/if}

					<div class="email">
						<div class="icon">
							<Icon icon="email" />
						</div>
						{user.email}
					</div>

					{#each $organization.address as a}
						{#if a.name == user.office_location}
							<div class="location">
								<div class="icon">
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
					Wragby&nbsp;Business&nbsp;Solutions&nbsp;&&nbsp;Technologies&nbsp;Limited.
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
</div>

<style>
	.hide {
		height: 0;
		overflow: hidden;
	}

	* {
		-webkit-print-color-adjust: exact !important;
		print-color-adjust: exact !important;
	}

	.block {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		gap: calc(var(--sp2) * var(--size));

		width: fit-content;
		padding: calc(var(--sp2) * var(--size));
		background-color: var(--bg2);
	}

	.card {
		width: 2000px;
		/* width: 100%; */
		/* max-width: 400px; */
		aspect-ratio: 1000/650;
		flex-shrink: 0;
		font-size: calc(0.6rem * var(--size));
	}

	.slogan {
		font-size: calc(0.5rem * var(--size));
		text-align: center;
	}

	.front {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		gap: calc(var(--sp2) * var(--size));

		padding: calc(var(--sp2) * var(--size));

		background-color: white;
	}

	.front .row1,
	.front .row2 {
		display: flex;
		justify-content: space-between;
		align-items: flex-end;
		gap: calc(var(--sp1) * var(--size));

		width: 100%;
	}
	.front .name {
		font-weight: 800;
		font-size: calc(1.2rem * var(--size));
		color: var(--ft1);
	}

	.front .role {
		color: var(--cl1);
	}

	.front .qr {
		width: calc(56px * var(--size));
	}

	.front .divider {
		background-color: var(--cl1);
		height: calc(2px * var(--size));
		width: 100%;
		flex-shrink: 0;
	}

	.front .row2 {
		height: 100%;
	}

	.front .row2 .left {
		max-width: calc(200px * var(--size));
		align-self: flex-start;
	}

	.front .row2 .right {
		width: calc(100px * var(--size));

		display: flex;
		flex-direction: column;
		gap: calc(var(--sp1) * var(--size));
		align-items: flex-end;
	}
	.front .logo {
		width: 100%;
	}

	.icon {
		display: flex;
		justify-content: center;
		align-items: center;
		flex-shrink: 0;

		width: calc(1rem * var(--size));
		height: calc(1rem * var(--size));
		border-radius: calc(var(--sp0) * var(--size));

		background-color: var(--ft2_d);
		/* background-color: var(--cl1); */
		color: white;
	}

	.phone,
	.email,
	.location {
		display: flex;
		align-items: center;
		gap: calc(var(--sp2) * var(--size));
		margin: calc(var(--sp0) * var(--size)) 0;

		fill: currentColor;
	}

	.location {
		align-items: flex-start;
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
		gap: calc(var(--sp1) * var(--size));
	}
	.back .row1 img {
		width: 40%;
	}

	.back .row2 {
		display: flex;
		justify-content: center;
		align-items: center;
		gap: calc(var(--sp1) * var(--size));
		flex-shrink: 0;

		height: 15%;

		color: var(--ft1_b);
		fill: currentColor;
		background-color: var(--ft2_d);
	}

	.back .divider {
		background-color: var(--cl1);
		height: calc(2px * var(--size));
		width: 100%;
	}
</style>
