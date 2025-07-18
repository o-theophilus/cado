<script>
	import { onMount } from 'svelte';
	import { user } from '$lib/store.svelte.js';

	import Meta from '$lib/meta.svelte';
	import BRound from '$lib/button/round.svelte';

	var selectedPoint;
	var highlightColor = '#5C6BC0',
		mutedHighlightColor = '#9FA8DA',
		mutedFill = '#f3f4fa',
		selectedFill = '#E8EAF6',
		normalFill = 'white';

	var points = [
		{
			x: 'Eliott Nieves',
			id: 'president',
			attributes: {
				role: 'CEO',
				photo: getImgText('images/vector-avatars2/avatar-1.svg')
			}
		},
		{
			x: 'Harvey-Lee Travis',
			id: 'vPresident1',
			parent: 'president',
			attributes: {
				role: 'Vice President',
				photo: getImgText('images/vector-avatars2/avatar-2.svg')
			}
		},
		{
			x: 'Gethin Morley',
			id: 'vPresident2',
			parent: 'president',
			attributes: {
				role: 'Vice President',
				photo: getImgText('images/vector-avatars2/avatar-4.svg')
			}
		},
		{
			x: 'Sonnie Kim',
			id: 'vPresident3',
			parent: 'president',
			attributes: {
				role: 'Vice President',
				photo: getImgText('images/vector-avatars2/avatar-3.svg')
			}
		},
		{
			x: 'Dante Curtis',
			id: 'manager1',
			parent: 'vPresident1',
			attributes: { role: 'Manager', photo: getImgText('images/vector-avatars2/avatar-3.svg') }
		},
		{
			x: 'Honey Mullen',
			id: 'manager2',
			parent: 'vPresident1',
			attributes: { role: 'Manager', photo: getImgText('images/vector-avatars2/avatar-3.svg') }
		},
		{
			x: 'Steffan Taylor',
			id: 'manager3',
			parent: 'vPresident2',
			attributes: { role: 'Manager', photo: getImgText('images/vector-avatars2/avatar-3.svg') }
		},
		{
			x: 'Charlton Hester',
			id: 'manager4',
			parent: 'vPresident2',
			attributes: { role: 'Manager', photo: getImgText('images/vector-avatars2/avatar-3.svg') }
		},
		{
			x: 'Ishmael Orr',
			id: 'manager5',
			parent: 'vPresident2',
			attributes: { role: 'Manager', photo: getImgText('images/vector-avatars2/avatar-3.svg') }
		},
		{
			x: 'Dua Frost',
			id: 'manager6',
			parent: 'manager5',
			attributes: { role: 'Manager', photo: getImgText('images/vector-avatars2/avatar-3.svg') }
		},
		{
			x: 'Salahuddin Eastwood',
			id: 'manager7',
			parent: 'manager5',
			attributes: { role: 'Manager', photo: getImgText('images/vector-avatars2/avatar-3.svg') }
		},
		{
			x: 'Nicole Tapia',
			id: 'employee1',
			parent: 'manager6',
			attributes: { role: 'Employee', photo: getImgText('images/vector-avatars2/avatar-3.svg') }
		},
		{
			x: 'Arisha Hinton',
			id: 'employee2',
			parent: 'manager6',
			attributes: { role: 'Employee', photo: getImgText('images/vector-avatars2/avatar-3.svg') }
		},
		{
			x: 'Martha Morley',
			id: 'employee3',
			parent: 'manager6',
			attributes: { role: 'Employee', photo: getImgText('images/vector-avatars2/avatar-3.svg') }
		},
		{
			x: 'Cathy Mcpherson',
			id: 'employee4',
			parent: 'manager6',
			attributes: { role: 'Employee', photo: getImgText('images/vector-avatars2/avatar-3.svg') }
		},
		{
			x: 'Kiara Johns',
			id: 'manager8',
			parent: 'vPresident3',
			attributes: { role: 'Manager', photo: getImgText('images/vector-avatars2/avatar-3.svg') }
		},
		{
			x: 'Grant Cash',
			id: 'manager9',
			parent: 'vPresident3',
			attributes: { role: 'Manager', photo: getImgText('images/vector-avatars2/avatar-3.svg') }
		},
		{
			x: 'Juanita Cottrell',
			id: 'employee5',
			parent: 'manager8',
			attributes: { role: 'Employee', photo: getImgText('images/vector-avatars2/avatar-3.svg') }
		},
		{
			x: 'Allana Frey',
			id: 'employee6',
			parent: 'manager8',
			attributes: { role: 'Employee', photo: getImgText('images/vector-avatars2/avatar-3.svg') }
		}
	];

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
	<script src="https://code.jscharting.com/latest/jscharting.js"></script>
	<link rel="stylesheet" href="https://code.jscharting.com/latest/jscharting.css" />
</svelte:head>

<Meta title={user.value?.firstname} />

<div class="hline">
	<div class="hline">
		<BRound icon="arrow_back" href="/profile" />
		<div class="page_title">Setting</div>
	</div>
</div>

<br />

<div id="chartDiv1" class="chartDiv" style="max-width: 770px;height: 560px"></div>

<style>
	.chartDiv {
		margin: 8px auto;
		padding: 15px;
		border-radius: 10px;
	}
</style>
