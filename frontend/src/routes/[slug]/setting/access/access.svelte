<script>
	import { createEventDispatcher } from 'svelte';

	import Button from '$lib/button/button.svelte';
	import Link from '$lib/button/link.svelte';
	import Tag from '$lib/button/tag.svelte';
	import Icon from '$lib/icon.svelte';

	let emit = createEventDispatcher();
	export let raw_access;
	export let user_access;
	let init_access = [...user_access];

	const select_group = (_in) => {
		let group = [];
		for (const [name, r0les] of Object.entries(raw_access)) {
			for (const x of r0les) {
				if (_in == name) {
					group.push(`${name}:${x[0]}`);
				} else if (_in == x[1]) {
					group.push(`${name}:${x[0]}`);
				} else if (!_in) {
					group.push(`${name}:${x[0]}`);
				}
			}
		}

		let add_all = false;
		for (const x of group) {
			if (!user_access.includes(x)) {
				add_all = true;
				break;
			}
		}

		if (add_all) {
			for (const x of group) {
				if (!user_access.includes(x)) {
					user_access.push(x);
				}
			}
			user_access = user_access;
		} else {
			user_access = user_access.filter((x) => !group.includes(x));
		}
	};

	const select = (_in) => {
		if (user_access.includes(_in)) {
			user_access = user_access.filter((x) => x != _in);
		} else {
			user_access.push(_in);
			user_access = user_access;
		}
	};

	let disabled = true;
	$: {
		let t1 = user_access.sort((a, b) => a - b).join(',');
		let t2 = init_access.sort((a, b) => a - b).join(',');
		disabled = t1 == t2;
	}
</script>

<div class="grid">
	<span>
		<Link
			small
			on:click={() => {
				select_group();
			}}
		>
			category
		</Link>
	</span>

	{#each [1, 2, 3] as x}
		<span>
			<Link
				small
				on:click={() => {
					select_group(x);
				}}
			>
				Level {x}
			</Link>
		</span>
	{/each}

	{#each Object.entries(raw_access) as [_type, _actions]}
		<span>
			<Link
				small
				on:click={() => {
					select_group(_type);
				}}
			>
				{_type}
			</Link>
		</span>

		{#each [1, 2, 3] as x}
			<span>
				{#each _actions as action}
					{#if action[1] == x}
						<Tag
							active={user_access.includes(`${_type}:${action[0]}`)}
							on:click={() => {
								select(`${_type}:${action[0]}`);
							}}
						>
							{action[0].split('_').join(' ')}
						</Tag>
					{/if}
				{/each}
			</span>
		{/each}
	{/each}
</div>

<Button
	{disabled}
	on:click={() => {
		emit('ok', user_access);
	}}
>
	Submit
	<Icon icon="send" />
</Button>

<style>
	.grid {
		display: grid;
		grid-template-columns: repeat(4, auto);
		margin: var(--sp2) 0;
	}

	span {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp0);
		align-items: center;

		outline: 1px solid var(--bg2);
		padding: var(--sp0);
	}
</style>
