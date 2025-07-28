<script>
	import { Meta } from '$lib/page';
	import { RoundButton, Radio } from '$lib/button';
	import { Row, Br } from '$lib/layout';
	import { Icon } from '$lib/macro';

	import { onMount } from 'svelte';

	let { data } = $props();
	let card = data.card;

	let type = $state('bar');
	let chartInstance = null;

	let labels = [];
	let values = [];
	for (const x of data.data) {
		const date = new Date(x.day);
		const options = { day: '2-digit', month: 'short', timeZone: 'UTC' };
		const fmt = new Intl.DateTimeFormat('en-US', options).format(date);

		labels.push(fmt);
		values.push(x.count);
	}

	const createChart = () => {
		if (chartInstance) {
			chartInstance.destroy();
		}

		const ctx = document.getElementById('myChart');
		chartInstance = new Chart(ctx, {
			type: type,
			data: {
				labels: labels,
				datasets: [
					{
						label: 'Views per day',
						data: values,
						borderWidth: 2,
						backgroundColor: type === 'bar' ? 'rgba(54, 162, 235, 0.2)' : 'rgba(54, 162, 235, 0.1)',
						borderColor: 'rgba(54, 162, 235, 1)',
						fill: type === 'line'
					}
				]
			},
			options: {
				responsive: true,
				maintainAspectRatio: false,
				animation: {
					duration: 400
				},
				plugins: {
					legend: {
						display: true
					},
					tooltip: {
						enabled: true
					}
				},
				scales: {
					y: {
						beginAtZero: true,
						grid: {
							color: 'rgba(0, 0, 0, 0.1)'
						}
					},
					x: {
						grid: {
							color: 'rgba(0, 0, 0, 0.1)'
						}
					}
				}
			}
		});
	};

	onMount(() => {
		createChart();
	});
</script>

<Meta title="{card.firstname} {card.lastname} - Card" />

<div class="page">
	<Row space>
		<Row>
			<RoundButton href="/profile">
				<Icon icon="arrow_back" size="1.2"></Icon>
			</RoundButton>
			<div class="page_title">Card Chart</div>
		</Row>
		<Radio
			list={['bar', 'line']}
			onclick={(e) => {
				type = e;
				createChart();
			}}
		></Radio>
	</Row>

	<br />

	<canvas id="myChart"></canvas>
</div>

<style>
	.page {
		max-width: var(--mobileWidth);
		width: 100%;
		margin: auto;
		padding: var(--sp2);
		padding-bottom: var(--sp5);
	}

	#myChart {
		max-height: 400px;
		width: 100%;
	}
</style>
