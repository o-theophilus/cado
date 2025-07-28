<script>
	import { page } from '$app/state';
	import { goto } from '$app/navigation';

	import { onMount } from 'svelte';
	import { module, user } from '$lib/store.svelte.js';

	import { Meta } from '$lib/page';
	import { Icon } from '$lib/macro';
	import { Button } from '$lib/button';
	import { Dialogue } from '$lib/modal';
	import { Login } from '$lib/auth';

	const get_module = (x) => {
		if (x == 'login') {
			return Login;
		} else if (x == 'dialogue') {
			return Dialogue;
		}
		return null;
	};

	onMount(() => {
		let _module = null;
		let value = {};

		for (const [key, val] of page.url.searchParams.entries()) {
			if (key == 'module') {
				_module = get_module(val);
			} else {
				value[key] = val;
			}
		}

		if (_module) {
			module.open(_module, value);
			window.history.replaceState(history.state, '', '/');
		}
	});
</script>

<Meta title="Home" description="Welcome to Cado" />

<div class="frame">
	<img src="/bg1.jpg" alt="hero" />
	<div class="block">
		<div class="content">
			<div class="copy">All Your Contacts <br /> in One Place</div>
			<div class="divider"></div>
			<div class="sub_copy">
				Store and manage all your essential contact information and social media links. Share your
				profile with a simple QR code scan, making networking and staying in touch easier than ever.
			</div>

			<Button
				--button-height="56px"
				--button-padding-x="24px"
				--button-background-color="var(--cl1)"
				--button-color="var(--ft1_b)"
				onclick={() => {
					if (user.value.login) {
						goto('/profile');
					} else {
						module.open(Login);
					}
				}}
			>
				Get Started
				<Icon icon="arrow_forward" />
			</Button>
		</div>
	</div>
</div>

{#snippet card(icon, color, title, details)}
	<div class="card">
		<div class="icon" style:fill="var({color})">
			<Icon {icon} size="3"></Icon>
		</div>
		<div class="title">
			{title}
		</div>
		<div class="details">
			{details}
		</div>
	</div>
{/snippet}

<div class="page">
	<div class="page_title">Features</div>
	<div class="features">
		{@render card(
			'design',
			'--cl5',
			'Create & Customize Your Digital Business Card',
			'Build sleek, professional digital cards with your name, photo, role, and links to WhatsApp, LinkedIn, Instagram, and more. Upload your logo, choose themes, and preview changes in real time.'
		)}
		{@render card(
			'qr_code',
			'--cl2',
			'Instant QR Code for Easy Sharing',
			'Each card comes with a unique QR code that instantly connects others to your profile. Download it for printing, packaging, or social bios — one scan, and they’re viewing your details.'
		)}
		{@render card(
			'timer',
			'--cl3',
			'Dynamic and Always Up-to-Date',
			'Update your contact info anytime without reprinting or resending links. Your card is always current — change your title, add promotions, or update your number and it reflects instantly.'
		)}
		{@render card(
			'chart',
			'--cl4',
			'Insights and Control Dashboard',
			'Track who’s viewing your card with scan analytics. See view counts, locations, and device types. Manage multiple cards in one place — perfect for professionals, teams, and events.'
		)}
	</div>
	<br />
	<br />
	<Button
		--button-height="56px"
		--button-background-color="var(--cl1)"
		--button-color="var(--ft1_b)"
		onclick={() => {
			if (user.value.login) {
				goto('/profile');
			} else {
				module.open(Login);
			}
		}}
	>
		Get Started
		<Icon icon="arrow_forward" />
	</Button>
</div>

<style>
	.frame {
		position: relative;
	}
	.block {
		position: absolute;
		inset: 0;

		display: flex;
		align-items: center;

		padding: var(--sp3);
		max-width: var(--mobileWidth);
		margin: auto;
	}

	.copy,
	.sub_copy {
		color: var(--bg1);
		max-width: 300px;
		font-size: medium;

		text-shadow: 0 0 10px #0e141b;
	}

	.copy {
		font-size: x-large;
		font-weight: 700;
	}
	.sub_copy {
		margin: var(--sp3) 0;
	}

	.divider {
		background-color: var(--cl1);
		height: 4px;
		max-width: 100px;
		margin: var(--sp3) 0;
	}

	img {
		display: block;

		height: 480px;
		width: 100%;

		object-fit: cover;
		background-color: #0e141b;
	}

	@media screen and (min-width: 900px) {
		img {
			object-fit: contain;
		}
	}

	.page {
		max-width: var(--mobileWidth);
		width: 100%;
		margin: var(--sp5) auto;
		padding: 0 var(--sp2);
	}

	.page_title {
		margin-top: var(--sp5);
		margin-bottom: var(--sp3);
	}

	.features {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: var(--sp2);
	}

	@media (max-width: 600px) {
		.features {
			grid-template-columns: 1fr;
		}
	}
	.card {
		background-color: var(--bg2);
		border-radius: 8px;
		padding: var(--sp3);
	}

	.icon {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 64px;
		height: 64px;

		background-color: var(--bg1);
		border-radius: 8px;
	}

	.title {
		font-size: large;
		font-weight: 800;
		color: var(--ft1);

		margin: var(--sp2) 0;
	}
	.details {
		font-size: medium;
	}
</style>
