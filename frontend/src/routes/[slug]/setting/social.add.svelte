<script>
	import IG from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Dropdown from '$lib/dropdown.svelte';

	let { value = $bindable() } = $props();
	let error = $state('');
	let _key = $state('');
	let _key2 = $state('');
	let _val = $state('');

	const add = () => {
		error = '';
		let _k = _key;
		if (_k == 'other') {
			_k = _key2;
		}

		if (!_k) {
			error = 'name is required';
		}
		if (!_val) {
			error = error ? `${error}. url is required` : 'url is required';
		} else if (_k == 'whatsapp' && !/^\+\d{1,3}[\d]*$/.test(_val.replace(/\s+/g, ''))) {
			error =
				'Invalid phone number. Phone number should start with a "+" followed by the country code and then the phone number. For example, +2348012345678.';
		}

		if (!error) {
			value = { ...value, [_k]: _val };

			_key2 = '';
			_val = '';
		}
	};

	const remove = (n) => {
		const { [n]: _, ...rest } = value;
		value = rest;
	};

	let list = ['whatsapp', 'linkedin', 'twitter', 'facebook', 'instagram', 'other'];
</script>

{#if Object.keys(value).length > 0}
	<div class="social_block">
		{#each Object.entries(value) as [key, value] (key)}
			<div class="social">
				<a
					href={key != 'whatsapp' ? value : `https://wa.me/${value}/?text=Hello%20${name}`}
					target="_blank"
					rel="noopener noreferrer"
				>
					<Icon icon={list.includes(key) ? key : 'link'} />

					{key}
				</a>
				<div
					class="close"
					onclick={() => {
						remove(key);
					}}
					role="presentation"
				>
					<Icon icon="close" />
				</div>
			</div>
		{/each}
	</div>
	<br />
{/if}

<form onsubmit={(e) => e.preventDefault()} novalidate autocomplete="off">
	{#if error}
		<div class="error">
			{error}
		</div>
	{/if}

	<div class="line">
		<Dropdown
			bind:value={_key}
			list={list.filter((k) => !Object.keys(value).includes(k))}
			wide={_key != 'other'}
		></Dropdown>

		{#if _key == 'other'}
			<IG
				type="text"
				placeholder={_key != 'whatsapp'
					? `${_key} profile name`
					: 'Whatsapp number (e.g. +2348012345678)'}
				bind:value={_key2}
				no_pad
			/>
		{/if}
	</div>

	<br />

	<div class="line">
		<IG
			type="text"
			placeholder={_key != 'whatsapp'
				? `${_key} profile url`
				: 'Whatsapp number (e.g. +2348012345678)'}
			bind:value={_val}
			no_pad
		/>

		<Button onclick={add}>
			Add
			<Icon icon="send" />
		</Button>
	</div>
</form>

<style>
	.line {
		display: flex;
		gap: var(--sp2);
		align-items: center;
	}

	.social_block {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp0);

		border-radius: var(--sp0);
	}
	.social {
		display: flex;
		flex-wrap: wrap;
		background-color: var(--bg2);

		border-radius: var(--sp0);
		overflow: hidden;
	}

	a {
		display: flex;
		align-items: center;
		gap: var(--sp1);

		padding: var(--sp1);

		color: var(--ft1);
		fill: currentColor;
		text-decoration: none;

		transition:
			background-color var(--trans),
			color var(--trans);
	}

	a:hover {
		color: var(--ft1_b);
		background-color: var(--button);
	}

	.close {
		--size: 40px;

		display: flex;
		align-items: center;
		justify-content: center;

		width: var(--size);
		height: var(--size);

		cursor: pointer;

		transition:
			background-color var(--trans),
			fill var(--trans);
	}
	.close:hover {
		fill: var(--ft1_b);
		background-color: var(--cl2);
	}

	.error {
		margin: var(--sp1) 0;
		font-size: smaller;
	}
</style>
