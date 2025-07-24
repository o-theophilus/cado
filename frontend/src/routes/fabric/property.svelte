<script>
	let { canvas } = $props();

	let selected = null;
	let ppt = $state({});

	$effect(() => {
		if (selected) {
			selected.set({
				width: ppt.width / selected.scaleX,
				height: ppt.height / selected.scaleY,
				radius: ppt.diameter / (selected.scaleX * 2),
				text: ppt.text,
				name: ppt.name,
				fill: ppt.color
			});
		} else {
			canvas.setWidth(ppt.width || canvas.getWidth());
			canvas.setHeight(ppt.height || canvas.getHeight());
			canvas.backgroundColor = ppt.color || canvas.backgroundColor;
		}

		canvas.renderAll();
	});

	const update_panel = (o) => {
		if (o.type == 'circle') {
			ppt.name = o.name;
			ppt.diameter = Math.round(o.radius * o.scaleX * 2);
			ppt.color = o.fill;
		} else if (o.type == 'rect') {
			ppt.name = o.name;
			ppt.width = Math.round(o.width * o.scaleX);
			ppt.height = Math.round(o.height * o.scaleY);
			ppt.color = o.fill;
		} else if (o.type == 'text') {
			ppt.name = o.name;
			ppt.width = Math.round(o.width * o.scaleX);
			ppt.height = Math.round(o.height * o.scaleY);
			ppt.text = o.text;
			ppt.color = o.fill;
		}
	};

	const update_panel_once = (obj) => {
		clear_panel();
		selected = obj;
		update_panel(obj);
	};

	const clear_panel = () => {
		selected = null;
		ppt = {};
		ppt.width = canvas.getWidth();
		ppt.height = canvas.getHeight();
		ppt.color = canvas.backgroundColor;
	};

	canvas.on('selection:created', (e) => {
		update_panel_once(e.selected[0]);
	});

	canvas.on('selection:updated', (e) => {
		update_panel_once(e.selected[0]);
	});

	canvas.on('selection:cleared', (e) => {
		clear_panel();
	});

	canvas.on('object:selected', (e) => {
		// Triggered when an individual object is selected
		console.log('Object selected:', e.target);
	});

	canvas.on('object:modified', (e) => {
		// update_panel_once(e.target);
		// console.log('Object modified:', e.target);
	});

	canvas.on('object:scaling', (e) => {
		update_panel(e.target);
	});

	clear_panel();
</script>

<div class="setting">
	{#if 'name' in ppt}
		<label>
			Name
			<input type="name" bind:value={ppt.name} />
		</label>
	{/if}
	{#if 'text' in ppt}
		<label>
			Text
			<input type="text" bind:value={ppt.text} />
		</label>
	{/if}
	{#if 'width' in ppt}
		<label>
			Width
			<input type="number" bind:value={ppt.width} />
		</label>
	{/if}
	{#if 'height' in ppt}
		<label>
			Height
			<input type="number" bind:value={ppt.height} />
		</label>
	{/if}
	{#if 'diameter' in ppt}
		<label>
			Diameter
			<input type="number" bind:value={ppt.diameter} />
		</label>
	{/if}
	{#if 'color' in ppt}
		<label>
			Color
			<input type="color" bind:value={ppt.color} />
		</label>
	{/if}
</div>

<style>
	.setting {
		max-width: 400px;
	}
	label {
		display: block;
	}
</style>
