<script>
	import { onMount } from 'svelte';
	// import { points } from './data';
	let points = [];

	var selectedPoint;
	var highlightColor = '#5C6BC0',
		mutedHighlightColor = '#9FA8DA',
		mutedFill = '#f3f4fa',
		selectedFill = '#E8EAF6',
		normalFill = 'white';

	let chart;

	onMount(() => {
		if (!window.JSC) {
			console.error('JSC not found on window!');
			return;
		}

		chart = JSC.chart('chartDiv1', {
			debug: true,
			type: 'organizational',
			defaultTooltip_enabled: false,

			defaultAnnotation: {
				padding: [5, 10],
				margin: 6
			},
			annotations: [
				{
					position: 'bottom',
					label_text: 'Click on a node to select all nodes up the tree or click again to deselect.'
				}
			],

			defaultSeries: {
				color: normalFill,
				/* Point selection is disabled because it is managed manually with point click events. */
				pointSelection: false
			},
			defaultPoint: {
				focusGlow: false,
				connectorLine: {
					color: '#e0e0e0',
					radius: [10, 3]
				},
				label: {
					text: '%photo%name<br><span style="color:#9E9E9E">%role</span>',
					style_color: 'black'
				},
				outline: { color: '#e0e0e0', width: 1 },
				annotation: { syncHeight_with: 'level' },
				states: {
					mute: {
						opacity: 0.8,
						outline: {
							color: mutedHighlightColor,
							opacity: 0.9,
							width: 2
						}
					},
					select: {
						enabled: true,
						outline: {
							color: highlightColor,
							width: 2
						},
						color: selectedFill
					},
					hover: {
						outline: {
							color: mutedHighlightColor,
							width: 2
						},
						color: mutedFill
					}
				},
				events: {
					click: pointClick,
					mouseOver: pointMouseOver,
					mouseOut: pointMouseOut
				}
			},
			series: [{ points: points }]
		});
	});

	function pointClick() {
		var point = this,
			chart = point.chart;
		resetStyles(chart);
		if (point.id === selectedPoint) {
			selectedPoint = undefined;
			return;
		}
		selectedPoint = point.id;
		styleSelectedPoint(chart);
	}

	function pointMouseOver() {
		var point = this,
			chart = point.chart;
		chart.connectors([point.id, 'up'], {
			color: mutedHighlightColor,
			width: 2
		});
		chart.series().points([point.id, 'up']).options({ muted: true });
	}

	function pointMouseOut() {
		var point = this,
			chart = point.chart;
		// Reset point and line styling.
		resetStyles(chart);
		// Style clicked points
		styleSelectedPoint(chart);
		return false;
	}

	function styleSelectedPoint(chart) {
		if (selectedPoint) {
			chart.connectors([selectedPoint, 'up'], {
				color: highlightColor,
				width: 2
			});
			chart.series().points([selectedPoint, 'up']).options({ selected: true, muted: false });
		}
	}

	function resetStyles(chart) {
		chart.connectors();
		chart.series().points().options({ selected: false, muted: false });
	}

	function getImgText(name) {
		return (
			'<img width=50 height=50 align=center margin_bottom=4 margin_top=4 src=' + name + '><br>'
		);
	}
</script>

<svelte:head>
	<script
		script
		type="text/javascript"
		src="https://code.jscharting.com/latest/jscharting.js"
	></script>
	<link rel="stylesheet" href="https://code.jscharting.com/latest/jscharting.css" />
</svelte:head>


<Meta title="{org.fullname || org.name} - Organizational Chart" />

<div class="page_title">Organizational Chart</div>

<br />

<div id="chartDiv1" class="chartDiv" style="max-width: 770px;height: 560px"></div>

<style>
	.chartDiv {
		width: 100vw;
		height: 100vh;
		/* margin: 8px auto; */
		/* padding: 15px; */
		/* border-radius: 10px; */
	}
</style>
