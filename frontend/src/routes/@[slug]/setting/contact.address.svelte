<script>
	import IG from '$lib/input_group.svelte';
	import BRound from '$lib/button/round.svelte';

	let { value = $bindable(), error } = $props();
</script>

<div class="line">
	Address

	<BRound
		icon="add"
		onclick={() => {
			value.push({
				address: '',
				url: ''
			});
		}}
	/>
</div>

{#if error.address}
	<div class="error">
		{error.address}
	</div>
	<br />
{/if}

{#each value as _, i}
	{@render template(i)}
{/each}

{#snippet template(i)}
	<div class="form">
		<div class="close">
			<BRound
				icon="close"
				onclick={() => {
					value.splice(i, 1);
				}}
			/>
		</div>

		<IG
			name="Address {i + 1}"
			icon="location_on"
			placeholder="Address here"
			error={error[i]}
			type="text"
			bind:value={value[i].address}
		/>

		<IG
			name="Map URL"
			icon="language"
			placeholder="Map URL here"
			type="text"
			bind:value={value[i].url}
		/>
	</div>
{/snippet}

<style>
	.form {
		position: relative;
		padding: var(--sp2);
		margin: var(--sp1) 0;
		border-radius: var(--sp0);

		background-color: var(--bg2);
	}

	.close {
		position: absolute;
		top: 12px;
		right: var(--sp2);
	}

	.line {
		display: flex;
		gap: var(--sp2);
		align-items: center;
		justify-content: space-between;
	}
</style>
