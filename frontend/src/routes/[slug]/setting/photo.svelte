<script>
	import { loading, notify, token } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import Icon from '$lib/icon.svelte';
	import Card from '$lib/card.svelte';

	let { entity, _type, name = 'photo', active_card, update } = $props();

	let error = $state({});
	let input;
	let dragover = $state(false);

	const validate = () => {
		error = {};
		let file = input.files[0];

		let [media, type] = file.type.split('/');
		if (media != 'image' || ['svg+xml', 'x-icon'].includes(type)) {
			error.error = 'invalid file';
		}

		Object.keys(error).length === 0 && submit(file);
	};

	const submit = async (file) => {
		let formData = new FormData();
		formData.append('file', file);

		loading.open('Uploading Photo . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/photo/${_type}/${entity.key}/${name}`, {
			method: 'post',
			headers: {
				Authorization: token.value
			},
			body: formData
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			active_card.close();
			update(resp[_type]);
			notify.open('Photo Uploaded');
		} else {
			error = resp;
			input.value = '';
		}
	};

	const remove = async () => {
		error = {};

		loading.open('Deleting Photo . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/photo/${_type}/${entity.key}/${name}`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: token.value
			}
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			active_card.close();
			update(resp[_type]);
			notify.open('Photo Deleted');
		} else {
			error = resp;
		}
	};

	let ar = $derived.by(() => {
		let temp = 1;
		let match = entity[name]?.match(/_(\d+)x(\d+)\./);
		if (match) {
			temp = parseInt(match[1]) / parseInt(match[2]);
		}
		return temp;
	});
</script>

<Card open={active_card.value == name} onopen={() => active_card.set(name)}>
	{#snippet title()}
		<span class="capitalize">
			{name}
		</span>
	{/snippet}

	<br />
	<img
		src={entity[name] || '/no_photo.png'}
		alt={entity.name}
		class:dragover
		style:--ar={ar}
		onclick={() => {
			input.click();
		}}
		ondragover={(e) => {
			e.preventDefault();
			dragover = true;
		}}
		ondragenter={() => {
			e.preventDefault();
		}}
		ondragleave={() => {
			e.preventDefault();
			dragover = false;
		}}
		ondrop={(e) => {
			dragover = false;
			e.preventDefault();
			input.files = e.dataTransfer.files;
			validate();
		}}
		role="presentation"
	/>
	<input
		style:display="none"
		type="file"
		accept="image/*"
		bind:this={input}
		onchange={() => {
			validate();
		}}
	/>

	{#if error.error}
		<div class="error">
			{@html error.error}
		</div>
	{/if}

	<br />

	<div class="line">
		<Button
			onclick={() => {
				input.click();
			}}
		>
			<Icon icon="add" />
			{#if entity[name]}
				Change
			{:else}
				Add
			{/if}
		</Button>

		{#if entity[name]}
			<Button
				onclick={() => {
					remove('delete');
				}}
			>
				<Icon icon="delete" />
				Delete
			</Button>
		{/if}
	</div>
</Card>

<style>
	.error {
		margin-top: var(--sp2);
		font-size: small;
	}

	img {
		width: 100%;
		max-width: 200px;
		border-radius: var(--sp1);
		outline: 2px solid var(--bg2);
		transition:
			outline-color var(--trans),
			transform var(--trans);
		display: block;
		aspect-ratio: var(--ar);
	}
	img:hover,
	.dragover {
		outline-color: var(--cl1);
		cursor: pointer;
	}

	.line {
		display: flex;
		gap: var(--sp1);
		flex-wrap: wrap;
	}
	.capitalize {
		text-transform: capitalize;
	}
</style>
