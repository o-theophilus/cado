<script>
	import { Button } from '$lib/button';

	let mods = [
		{ attr: '--button-height', def: '40px', is_def: false, val: '32px' },
		{ attr: '--button-width', def: 'unset', is_def: false, val: '100%' },
		{ attr: '--button-border-radius', def: '4px', is_def: false, val: '100px' },
		{ attr: '--button-padding-x', def: '16px', is_def: false, val: '32px' },
		{ attr: '--button-font-size', def: '1rem', is_def: false, val: '1.2em' },
		{ attr: '--button-font-weight', def: '700', is_def: false, val: '500' },
		{ attr: '--button-background-color', def: 'hsl(0, 0%, 90%)', is_def: false, val: 'red' },
		{ attr: '--button-color', def: 'hsl(0, 0%, 0%)', is_def: false, val: 'red' },
		{ attr: '--button-background-color-hover', def: 'hsl(0, 0%, 85%)', is_def: false, val: 'red' },
		{ attr: '--button-color-hover', def: 'hsl(0, 0%, 0%)', is_def: false, val: 'red' },
		{ attr: '--button-border-color', def: 'hsl(0, 0%, 85%)', is_def: false, val: 'red' }
	];

	let border = false;
	let capitalize = false;
	let disabled = false;
</script>

<br />
<br />

<Button
	onclick={() => {}}
	{border}
	{capitalize}
	{disabled}
	--button-height={!mods[0].is_def ? mods[0].def : mods[0].val}
	--button-width={!mods[1].is_def ? mods[1].def : mods[1].val}
	--button-border-radius={!mods[2].is_def ? mods[2].def : mods[2].val}
	--button-padding-x={!mods[3].is_def ? mods[3].def : mods[3].val}
	--button-font-size={!mods[4].is_def ? mods[4].def : mods[4].val}
	--button-font-weight={!mods[5].is_def ? mods[5].def : mods[5].val}
	--button-background-color={!mods[6].is_def ? mods[6].def : mods[6].val}
	--button-color={!mods[7].is_def ? mods[7].def : mods[7].val}
	--button-background-color-hover={!mods[8].is_def ? mods[8].def : mods[8].val}
	--button-color-hover={!mods[9].is_def ? mods[9].def : mods[9].val}
	--button-border-color={!mods[10].is_def ? mods[10].def : mods[10].val}
>
	click me!
</Button>

<Button
	href="/"
	{border}
	{capitalize}
	--button-height={!mods[0].is_def ? mods[0].def : mods[0].val}
	--button-width={!mods[1].is_def ? mods[1].def : mods[1].val}
	--button-border-radius={!mods[2].is_def ? mods[2].def : mods[2].val}
	--button-padding-x={!mods[3].is_def ? mods[3].def : mods[3].val}
	--button-font-size={!mods[4].is_def ? mods[4].def : mods[4].val}
	--button-font-weight={!mods[5].is_def ? mods[5].def : mods[5].val}
	--button-background-color={!mods[6].is_def ? mods[6].def : mods[6].val}
	--button-color={!mods[7].is_def ? mods[7].def : mods[7].val}
	--button-background-color-hover={!mods[8].is_def ? mods[8].def : mods[8].val}
	--button-color-hover={!mods[9].is_def ? mods[9].def : mods[9].val}
	--button-border-color={!mods[10].is_def ? mods[10].def : mods[10].val}
>
	click me!
</Button>

<Button
	{border}
	{capitalize}
	--button-height={!mods[0].is_def ? mods[0].def : mods[0].val}
	--button-width={!mods[1].is_def ? mods[1].def : mods[1].val}
	--button-border-radius={!mods[2].is_def ? mods[2].def : mods[2].val}
	--button-padding-x={!mods[3].is_def ? mods[3].def : mods[3].val}
	--button-font-size={!mods[4].is_def ? mods[4].def : mods[4].val}
	--button-font-weight={!mods[5].is_def ? mods[5].def : mods[5].val}
	--button-background-color={!mods[6].is_def ? mods[6].def : mods[6].val}
	--button-color={!mods[7].is_def ? mods[7].def : mods[7].val}
	--button-border-color={!mods[10].is_def ? mods[10].def : mods[10].val}
>
	click me!
</Button>

<br />
<br />

<div class="block">
	{#each mods as x, i}
		<div class="attr">
			{x.attr}
		</div>
		<div class="def">
			{x.def}
		</div>
		<div class="def">
			<input type="checkbox" bind:checked={mods[i].is_def} />
		</div>
		<input type="text" bind:value={x.val} />
	{/each}
</div>

<br />
<br />
border
<input type="checkbox" bind:checked={border} />
<br />
capitalize
<input type="checkbox" bind:checked={capitalize} />
<br />
disabled
<input type="checkbox" bind:checked={disabled} />
<br />
<br />

<textarea name="" id="">
	<Button
	{border}
	{capitalize}
	--button-height={!mods[0].is_def ? mods[0].def : mods[0].val}
	--button-width={!mods[1].is_def ? mods[1].def : mods[1].val}
	--button-border-radius={!mods[2].is_def ? mods[2].def : mods[2].val}
	--button-padding-x={!mods[3].is_def ? mods[3].def : mods[3].val}
	--button-font-size={!mods[4].is_def ? mods[4].def : mods[4].val}
	--button-font-weight={!mods[5].is_def ? mods[5].def : mods[5].val}
	--button-background-color={!mods[6].is_def ? mods[6].def : mods[6].val}
	--button-color={!mods[7].is_def ? mods[7].def : mods[7].val}
	--button-border-color={!mods[10].is_def ? mods[10].def : mods[10].val}
	> click me! </Button>
</textarea>

<style>
	.block {
		display: grid;
		grid-template-columns: 1fr auto auto auto;
	}

	textarea {
		width: 100%;
		height: 200px;
	}
</style>
