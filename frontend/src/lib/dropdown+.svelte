<script>
	import { onMount } from 'svelte';
	import { page_state } from '$lib/store.svelte.js';

	import Dropdown from './dropdown.svelte';

	let { default_value, value = $bindable(), list = [], onchange, ...props } = $props();

	onMount(() => {
		let _list = list;
		if (list[0] instanceof Object) {
			_list = Object.values(list);
		}

		if (!default_value || !_list.includes(default_value)) {
			default_value = _list[0];
		}

		if (page_state.searchParams.order) {
			value = page_state.searchParams.order;
		} else {
			value = default_value;
		}
	});
</script>

{#if list.length}
	<Dropdown
		bind:value
		{list}
		onchange={() => {
			onchange?.(value != default_value ? value : '');
		}}
		{...props}
	></Dropdown>
{/if}
