<script>
	import { Button } from '$lib/button';

	let mods = [
		{ attr: '--button-height', def: '40px', is_val: false, val: '32px' },
		{ attr: '--button-width', def: 'unset', is_val: false, val: '100%' },
		{ attr: '--button-border-radius', def: '4px', is_val: false, val: '100px' },
		{ attr: '--button-padding-x', def: '16px', is_val: false, val: '32px' },
		{ attr: '--button-font-size', def: '1rem', is_val: false, val: '1.2em' },
		{ attr: '--button-font-weight', def: '700', is_val: false, val: '500' },
		{ attr: '--button-background-color', def: 'hsl(0, 0%, 90%)', is_val: false, val: 'red' },
		{ attr: '--button-color', def: 'hsl(0, 0%, 0%)', is_val: false, val: 'red' },
		{ attr: '--button-background-color-hover', def: 'hsl(0, 0%, 85%)', is_val: false, val: 'red' },
		{ attr: '--button-color-hover', def: 'hsl(0, 0%, 0%)', is_val: false, val: 'red' },
		{ attr: '--button-border-color', def: 'hsl(0, 0%, 85%)', is_val: false, val: 'red' }
	];

	let border = false;
	let capitalize = false;
	let disabled = false;

	let type = 'button';

	const button = () => {
		let temp = '<Button';
		temp += border ? '\n border' : '';
		temp += capitalize ? '\n capitalize' : '';
		temp += disabled && type == 'button' ? '\n disabled' : '';
		temp += mods[0].is_val ? `\n --button-height="${mods[0].val}"` : '';
		temp += mods[1].is_val ? `\n --button-width="${mods[1].val}"` : '';
		temp += mods[2].is_val ? `\n --button-border-radius="${mods[2].val}"` : '';
		temp += mods[3].is_val ? `\n --button-padding-x="${mods[3].val}"` : '';
		temp += mods[4].is_val ? `\n --button-font-size="${mods[4].val}"` : '';
		temp += mods[5].is_val ? `\n --button-font-weight="${mods[5].val}"` : '';
		temp += mods[6].is_val ? `\n --button-background-color="${mods[6].val}"` : '';
		temp += mods[7].is_val ? `\n --button-color="${mods[7].val}"` : '';
		temp += mods[8].is_val ? `\n --button-background-color-hover="${mods[8].val}"` : '';
		temp += mods[9].is_val ? `\n --button-color-hover="${mods[9].val}"` : '';
		temp += mods[10].is_val ? `\n --button-border-color="${mods[10].val}"` : '';
		temp += '> click me! </Button>';

		return temp;
	};
</script>

<label>
	button
	<input type="radio" bind:group={type} value="button" />
</label>
<label>
	a
	<input type="radio" bind:group={type} value="a" />
</label>
<label>
	tag
	<input type="radio" bind:group={type} value="tag" />
</label>
<br />
<br />
{#if type == 'button'}
	border
	<input type="checkbox" bind:checked={border} />
	<br />
{/if}
capitalize
<input type="checkbox" bind:checked={capitalize} />
<br />
disabled
<input type="checkbox" bind:checked={disabled} />
<br />
<br />

<div class="block">
	{#each mods as x, i}
		{#if !(type == 'tag' && ['--button-background-color-hover', '--button-color-hover'].includes(x.attr))}
			<div class="attr">
				{x.attr}
			</div>
			<div class="def">
				{x.def}
			</div>
			<div class="def">
				<input type="checkbox" bind:checked={mods[i].is_val} />
			</div>
			<input type="text" bind:value={x.val} />
		{/if}
	{/each}
</div>

<br />
<br />

{#if type == 'button'}
	<Button
		onclick={() => {}}
		{border}
		{capitalize}
		{disabled}
		--button-height={!mods[0].is_val ? mods[0].def : mods[0].val}
		--button-width={!mods[1].is_val ? mods[1].def : mods[1].val}
		--button-border-radius={!mods[2].is_val ? mods[2].def : mods[2].val}
		--button-padding-x={!mods[3].is_val ? mods[3].def : mods[3].val}
		--button-font-size={!mods[4].is_val ? mods[4].def : mods[4].val}
		--button-font-weight={!mods[5].is_val ? mods[5].def : mods[5].val}
		--button-background-color={!mods[6].is_val ? mods[6].def : mods[6].val}
		--button-color={!mods[7].is_val ? mods[7].def : mods[7].val}
		--button-background-color-hover={!mods[8].is_val ? mods[8].def : mods[8].val}
		--button-color-hover={!mods[9].is_val ? mods[9].def : mods[9].val}
		--button-border-color={!mods[10].is_val ? mods[10].def : mods[10].val}
	>
		click me!
	</Button>
{:else if type == 'a'}
	<Button
		href="/"
		{border}
		{capitalize}
		--button-height={!mods[0].is_val ? mods[0].def : mods[0].val}
		--button-width={!mods[1].is_val ? mods[1].def : mods[1].val}
		--button-border-radius={!mods[2].is_val ? mods[2].def : mods[2].val}
		--button-padding-x={!mods[3].is_val ? mods[3].def : mods[3].val}
		--button-font-size={!mods[4].is_val ? mods[4].def : mods[4].val}
		--button-font-weight={!mods[5].is_val ? mods[5].def : mods[5].val}
		--button-background-color={!mods[6].is_val ? mods[6].def : mods[6].val}
		--button-color={!mods[7].is_val ? mods[7].def : mods[7].val}
		--button-background-color-hover={!mods[8].is_val ? mods[8].def : mods[8].val}
		--button-color-hover={!mods[9].is_val ? mods[9].def : mods[9].val}
		--button-border-color={!mods[10].is_val ? mods[10].def : mods[10].val}
	>
		click me!
	</Button>
{:else}
	<Button
		{border}
		{capitalize}
		--button-height={!mods[0].is_val ? mods[0].def : mods[0].val}
		--button-width={!mods[1].is_val ? mods[1].def : mods[1].val}
		--button-border-radius={!mods[2].is_val ? mods[2].def : mods[2].val}
		--button-padding-x={!mods[3].is_val ? mods[3].def : mods[3].val}
		--button-font-size={!mods[4].is_val ? mods[4].def : mods[4].val}
		--button-font-weight={!mods[5].is_val ? mods[5].def : mods[5].val}
		--button-background-color={!mods[6].is_val ? mods[6].def : mods[6].val}
		--button-color={!mods[7].is_val ? mods[7].def : mods[7].val}
		--button-border-color={!mods[10].is_val ? mods[10].def : mods[10].val}
	>
		click me!
	</Button>
{/if}

<br />
<br />

{#key type}
	{button()}
{/key}

<style>
	.block {
		display: grid;
		grid-template-columns: 1fr auto auto auto;
	}
</style>
