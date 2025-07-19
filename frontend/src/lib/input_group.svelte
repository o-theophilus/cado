<script>
	import Input from '$lib/input.svelte';
	import Icon from '$lib/icon.svelte';

	let {
		name = '',
		icon = '',
		icon_size = 1.2,
		error = '',

		value = $bindable(),
		type = 'text',
		placeholder = '',
		min = '',
		disabled = false,

		no_pad = false,
		required = false,

		onblur,
		oninput,
		onkeypress,

		label,
		input,
		right,
		down
	} = $props();

	let id = $derived.by(() => {
		let temp = '';
		if (name) {
			temp = name.split(' ').join('_').toLowerCase();
		}
		return temp;
	});
</script>

<div class="inputGroup" class:no_pad>
	{#if label}
		{@render label()}
	{:else if name}
		<div class="label">
			<label for={id}>
				{name}
				{#if required}
					<span class="error">*</span>
				{/if}
			</label>
		</div>
	{/if}

	{#if error}
		<div class="error">
			{@html error}
		</div>
	{/if}

	{#if input}
		{@render input(id)}
	{:else}
		<div class="input" class:left_pad={icon} class:disabled>
			{#if icon}
				<Icon {icon} size={icon_size} />
			{/if}
			<Input bind:value {id} {type} {placeholder} {min} {disabled} {onblur} {oninput}  {onkeypress}/>
			{@render right?.()}
		</div>
		{@render down?.()}
	{/if}
</div>

<style>
	.inputGroup {
		width: 100%;
	}
	.inputGroup:not(.no_pad) {
		margin: var(--sp2) 0;
	}

	.input {
		display: flex;
		align-items: center;

		width: 100%;

		border-radius: var(--sp0);
		border: none;

		outline: 2px solid var(--input);
		color: var(--ft2);
		fill: currentColor;

		transition: outline-color var(--trans);
	}

	.input.disabled {
		opacity: 0.4;
	}

	.input:hover:not(.disabled),
	:global(.input:has(:focus)) {
		outline-color: var(--cl1);
	}

	.left_pad {
		padding-left: var(--sp2);
	}

	.label,
	.error {
		font-size: 0.8rem;
		margin: var(--sp1) 0;
	}
</style>
