<script>
	import { IG, Dropdown } from '$lib/input';
	import { Button } from '$lib/button';
	import { Row, Br, Error } from '$lib/layout';
	import Icon from '$lib/icon.svelte';

	let { value = $bindable(), list } = $props();
	let error = $state('');
	let _key = $state('');
	let _key2 = $state('');
	let _val = $state('');
	let _list = $derived(list.filter((k) => !Object.keys(value).includes(k)));

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
</script>

<form onsubmit={(e) => e.preventDefault()} novalidate autocomplete="off">
	<Error {error} --error-margin-bottom="16px"></Error>

	<Row nowrap>
		{#key _list}
			<Dropdown bind:value={_key} list={_list} wide={_key != 'other'}></Dropdown>
		{/key}
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
	</Row>

	<Br />

	<Row nowrap>
		<IG
			type="text"
			bind:value={_val}
			placeholder={_key != 'whatsapp'
				? `${_key} profile url`
				: 'Whatsapp number (e.g. +2348012345678)'}
			no_pad
			onkeypress={(e) => {
				if (e.key == 'Enter') {
					add();
				}
			}}
		/>

		<Button onclick={add}>
			Add
			<Icon icon="send" />
		</Button>
	</Row>
</form>

<style>
	form {
		padding: var(--sp2);
		border: 2px solid var(--bg2);
		border-radius: var(--sp0);
	}
</style>
