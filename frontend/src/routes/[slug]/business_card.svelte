<script>
	import { page } from '$app/state';
	import { onMount } from 'svelte';

	import QRCode from 'qrcode';
	import { Icon } from '$lib/macro';

	let { card } = $props();
	let org = card.org;
	let src = $state('');

	onMount(() => {
		QRCode.toDataURL(
			page.url.href,
			{
				margin: 0
			},
			(error, dataUrl) => {
				if (error) console.error(error);
				src = dataUrl;
			}
		);
	});

	let cw = $state(400);
	let _cw = 400;
</script>

<div class="hide">
	<div class="block" id="to_print" style:--size={cw / _cw}>
		<div class="card front" bind:clientWidth={cw}>
			<div class="row1">
				<div class="left">
					<span class="name">
						{card.firstname}&nbsp;{card.lastname}
					</span>

					{#if card.job_title}
						<br />
						<span class="job_title">
							{card.job_title}
						</span>
					{/if}
				</div>
				<img class="qr" {src} alt="qr_code" />
			</div>

			<div class="divider"></div>

			<div class="row2">
				<div class="left">
					{#if card.phone}
						<div class="phone">
							<div class="icon">
								<Icon icon="call" />
							</div>
							{card.phone}
						</div>
					{/if}

					<div class="email">
						<div class="icon">
							<Icon icon="email" />
						</div>
						{card.email}
					</div>

					{#if org.address}
						{#each org.address as a}
							{#if a.name == card.office_location_id}
								<div class="location">
									<div class="icon">
										<Icon icon="location_on" />
									</div>
									{a.address}
								</div>
							{/if}
						{/each}
					{/if}
				</div>

				<div class="right">
					<img
						class="logo"
						src={org.photo || '/logo.png'}
						alt="{org.name} logo"
						onerror={(e) => {
							const img = e.currentTarget;
							img.onerror = null;
							img.src = '/logo.png';
						}}
					/>

					{#if org.slogan}
						<div class="slogan">{@html org.slogan.split(' ').join('&nbsp;')}</div>
					{/if}
				</div>
			</div>
		</div>

		<div class="card back">
			<div class="row1">
				<img
					src={org.photo || '/logo.png'}
					alt="{org.name} logo"
					onerror={(e) => {
						const img = e.currentTarget;
						img.onerror = null;
						img.src = '/logo.png';
					}}
				/>

				{#if org.fullname}
					<span class="slogan">
						{@html org.fullname.split(' ').join('&nbsp;')}
					</span>
				{/if}
			</div>

			<div class="row2">
				<div class="divider"></div>
				{#if org.website}
					<Icon icon="language" size="1.2" />
					{org.website}
					<div class="divider"></div>
				{/if}
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
		font-weight: 700;
		font-size: calc(1.2rem * var(--size));
		color: var(--ft1);
	}

	.front .job_title {
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
