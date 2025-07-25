<script>
	import { user } from '$lib/store.svelte.js';

	import Meta from '$lib/meta.svelte';
	import { BRound } from '$lib/button';
	import Icon from '$lib/icon.svelte';

	import { onMount } from 'svelte';

	onMount(() => {
		const ctx = document.getElementById('myChart');
		new Chart(ctx, {
			type: 'bar',
			data: {
				labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
				datasets: [
					{
						label: '# of Votes',
						data: [12, 19, 3, 5, 2, 3],
						borderWidth: 1
					}
				]
			},
			// options: {
			// 	scales: {
			// 		y: {
			// 			beginAtZero: true
			// 		}
			// 	}
			// }
			options: {
				animation: false,
				plugins: {
					legend: {
						display: false
					},
					tooltip: {
						enabled: false
					}
				}
			}
		});
	});
</script>

<svelte:head>
	<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</svelte:head>

<Meta title={user.value?.firstname} />

<div class="page">
	<div class="hline">
		<div class="hline">
			<BRound href="/profile">
				<Icon icon="arrow_back" size="1.2"></Icon>
			</BRound>
			<div class="page_title">Setting</div>
		</div>
	</div>

	<br />

	<canvas id="myChart"></canvas>
</div>

<style>
	.page {
		max-width: var(--mobileWidth);
		width: 100%;
		margin: auto;
		padding: 0 var(--sp2);
		padding-bottom: var(--sp5);
	}
</style>
