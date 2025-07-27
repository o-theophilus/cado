<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import { Row, Error } from '$lib/layout';
	import Icon from '$lib/icon.svelte';

	let { value = $bindable(), error } = $props();
	let _err = $state({});
	let form = $state({ address: null, url: null });

	const add = () => {
		_err = {};
		if (!form.address) {
			_err.address = 'this field is required';
		} else {
			for (const i of value) {
				if (i.address == form.address) {
					_err.address = 'address already added';
					break;
				}
			}
		}

		if (Object.keys(_err).length != 0) {
			return;
		}

		value.push(form);
		form = { address: null, url: null };
	};

	const remove = (x) => {
		let addresses = [];
		for (const i of value) {
			if (i.address != x) {
				addresses.push(i);
			}
		}
		value = addresses;
	};
</script>

<form onsubmit={(e) => e.preventDefault()} novalidate autocomplete="off">
	<Error error={error.address} --error-margin-top="16px"></Error>
	<IG
		name="Address"
		icon="location_on"
		placeholder="Address here"
		error={_err.address}
		type="text"
		bind:value={form.address}
	/>

	<Row nowrap>
		<IG icon="language" placeholder="Map URL here" type="text" bind:value={form.url} no_pad />
		<Button onclick={add}>
			Add
			<Icon icon="add" />
		</Button>
	</Row>
</form>

<div>
	{#each value as i (i.address)}
		<div class="address" animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
			<a href={i.url} target="_blank" rel="noopener noreferrer">
				{i.address}
			</a>
			<button
				onclick={() => {
					remove(i.address);
				}}
			>
				<Icon icon="close" />
			</button>
		</div>
	{/each}
</div>

<style>
	form {
		padding: var(--sp2);
		padding-top: 0;
		border: 2px solid var(--bg2);
		border-radius: var(--sp0);
	}

	.address {
		display: flex;
		align-items: stretch;
		gap: 1px;

		margin-top: var(--sp1);
		border-radius: var(--sp0);
		overflow: hidden;
	}
	.address:first-child {
		margin-top: var(--sp2);
	}

	a {
		width: 100%;
		padding: var(--sp1) var(--sp2);

		background-color: var(--bg2);
		color: var(--ft1);
		text-decoration: none;

		transition:
			background-color var(--trans),
			color var(--trans);
	}

	a:hover {
		color: var(--ft1_b);
		background-color: var(--button);
	}

	button {
		display: flex;
		align-items: center;
		justify-content: center;

		width: 40px;

		border: none;
		background-color: var(--bg2);

		transition:
			background-color var(--trans),
			fill var(--trans);
	}
	button:hover {
		fill: var(--ft1_b);
		background-color: var(--cl2);
	}
</style>
