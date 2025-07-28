<script>
	import { page } from '$app/state';
	import { onMount } from 'svelte';
	import { page_state } from '$lib/store.svelte.js';

	import { Search } from '$lib/layout';
	import { Icon } from '$lib/macro';
	import { Button } from '$lib/button';
	import { Row } from '$lib/layout';
	import Drop from '$lib/dropdown.svelte';

	export let access;

	let user_key = '';
	let type = 'all';
	let action = 'all';
	let search = `${user_key}:${type}:${action}`;
	let drop_1;
	let drop_2;

	onMount(() => {
		if (page.url.searchParams.has('search')) {
			let temp = page.url.searchParams.get('search');
			temp = temp.split(':');
			if (temp.length == 3) {
				user_key = temp[0];
				type = temp[1];
				action = temp[2];
				search = `${user_key}:${type}:${action}`;
				drop_1.set(type);
				drop_2.set(action);
			}
		}
	});

	const submit = (clear = false) => {
		if (clear) {
			user_key = '';
			type = 'all';
			action = 'all';
			drop_1.set(type);
			drop_2.set(action);
		}

		let check = `${search}`;
		search = `${user_key}:${type || 'all'}:${action || 'all'}`;
		if (search != check) {
			page_state('search', search != ':all:all' ? search : '');
		}
	};
</script>

<section>
	<Row>
		<Drop
			wide
			list={Object.keys(access)}
			default_value="all"
			bind:this={drop_1}
			on:change={(e) => {
				type = e.target.value;
				action = 'all';
				drop_2.set(action);
			}}
		/>

		<Drop
			wide
			list={access[type]}
			default_value="all"
			bind:this={drop_2}
			on:change={(e) => {
				action = e.target.value;
			}}
		/>
	</Row>

	<Row>
		<Search
			non_default
			placeholder="Search for User"
			bind:search={user_key}
			on:clear={() => {
				user_key = '';
			}}
		>
			<Button
				disabled={`${user_key}:${type}:${action}` == search}
				onclick={() => {
					submit();
				}}
			>
				<Icon icon="search" />
			</Button>
		</Search>
		<Button
			extra="hover_red"
			disabled={`${user_key}:${type}:${action}` == ':all:all'}
			onclick={() => {
				submit(true);
			}}
		>
			<Icon icon="close" />
		</Button>
	</Row>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		gap: var(--sp1);
		margin: var(--sp2) 0;
	}
</style>
