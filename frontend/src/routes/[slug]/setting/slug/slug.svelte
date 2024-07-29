<script>
	import { createEventDispatcher } from 'svelte';
	import { user as me } from '$lib/store.js';

	import IG from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';

	let emit = createEventDispatcher();
	export let slug;
	export let user_key;
	export let error = {};
	let form = {
		slug
	};

	const validate = () => {
		error = {};
		if (!form.slug) {
			error.slug = 'this field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		emit('ok', form.slug);
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<div class="note">
		<div class="title">
			<Icon icon="error" size="2" />
			Please note:
		</div>

		<span>
			Changing
			{#if user_key == $me.key}
				your
			{:else}
				this
			{/if}
			username will invalidate the associated URL and any generated QR codes for 
			{#if user_key == $me.key}
				your
			{:else}
				this
			{/if}
			account.
		</span>
	</div>

	<IG
		name="Username"
		icon="language"
		error={error.slug}
		placeholder="Username here"
		type="text"
		bind:value={form.slug}
		required
	/>

	<Button on:click={validate}>
		Submit
		<Icon icon="send" />
	</Button>
</form>

<style>
	.note {
		padding: var(--sp2);
		margin: var(--sp2) 0;
		background-color: var(--bg2);

		border-radius: var(--sp0);
	}

	.note span{
		font-size: 0.8rem;
	}
	
	.title {
		display: flex;
		align-items: center;
		gap: var(--sp2);

		margin-bottom: var(--sp2);
		fill: currentColor;
		color: var(--cl4);
		font-weight: 800;
	}
</style>
