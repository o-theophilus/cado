<script>
	import { loading, notification, organization as org } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Card from '$lib/card.svelte';

	export let organization;
	export let open;
	export let type;
	let edit_mode = true;
	let error = {};
	let input;
	let dragover = false;
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

		$loading = 'Uploading Photo . . .';
		let resp = await fetch(
			`${import.meta.env.VITE_BACKEND}/organization/${organization.key}/${type}`,
			{
				method: 'put',
				headers: {
					Authorization: $token
				},
				body: formData
			}
		);
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			organization = resp.organization;
			console.log(resp.organization);
			$org = resp.organization;
			$notification = {
				message: `${type.charAt(0).toUpperCase()}${type.slice(1)} Photo Uploaded`
			};

			error.error = resp.error;
		} else {
			error = resp;
		}
	};

	const remove = async () => {
		error = {};

		$loading = 'Deleting Photo . . .';
		let resp = await fetch(
			`${import.meta.env.VITE_BACKEND}/organization/${organization.key}/${type}`,
			{
				method: 'delete',
				headers: {
					'Content-Type': 'application/json',
					Authorization: $token
				}
			}
		);
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			organization[type] = null;
			$org = resp.organization;
			$notification = {
				message: `${type.charAt(0).toUpperCase()}${type.slice(1)} Photo Deleted`
			};
		} else {
			error = resp;
		}
	};

	let dim = [1 / 1];
	$: {
		dim = [1 / 1];
		let match = organization[type]?.match(/_(\d+)x(\d+)\./);
		if (match) {
			dim = [parseInt(match[1]), parseInt(match[2])];
		}
	}
</script>

<Card {open} on:open>
	<svelte:fragment slot="title">{type}</svelte:fragment>

	<br />
	<img
		src={organization[type] || '/no_photo.png'}
		alt={organization.name}
		class:dragover
		class:edit_mode
		style:--ar={dim[0] / dim[1]}
		on:click={() => {
			if (edit_mode) {
				input.click();
			}
		}}
		on:dragover|preventDefault={() => {
			dragover = true;
		}}
		on:dragenter
		on:dragleave|preventDefault={() => {
			dragover = false;
		}}
		on:drop={(e) => {
			dragover = false;
			if (edit_mode) {
				e.preventDefault();
				input.files = e.dataTransfer.files;
				validate();
			}
		}}
		role="presentation"
	/>
	<input
		style:display="none"
		type="file"
		accept="image/*"
		bind:this={input}
		on:change={(e) => {
			validate();
		}}
	/>

	{#if edit_mode}
		{#if error.error}
			<div class="error">
				{@html error.error}
			</div>
		{/if}

		<br />

		{#if !organization[type]}
			<Button
				primary
				on:click={() => {
					input.click();
				}}
			>
				<Icon icon="add" />
				Add
			</Button>
		{:else}
			<Button
				on:click={() => {
					remove('delete');
				}}
			>
				<Icon icon="delete" />
				Delete
			</Button>
		{/if}
	{/if}
</Card>

<style>
	.error {
		margin: var(--sp2) 0;
	}

	img {
		width: 100%;
		border-radius: var(--sp1);
		outline: 2px solid var(--bg2);
		transition: outline-color var(--trans), transform var(--trans);
		display: block;
	}
	img.edit_mode:hover,
	.dragover.edit_mode {
		outline-color: var(--cl1);
		cursor: pointer;
	}
</style>
