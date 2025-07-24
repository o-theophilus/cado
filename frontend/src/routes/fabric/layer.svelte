<script>
	let { fabric, canvas } = $props();

	// let layer = $state([]);
	let layer = $state(canvas._objects);
	let selected = $state(null);

	const select_item_on_canvas = (e) => {
		selected = e.target;
	};
	const select_item_on_layer = (e) => {
		selected = e.target;
		canvas.setActiveObject(e);
	};
	const clear_highlight = () => {
		selected = null;
	};
	const refresh_layer = (e) => {
		if (e.target._type == 'guideline') return;
		layer = canvas.getObjects();
		layer.reverse();
	};

	canvas.on('object:added', (e) => {
		refresh_layer(e);
	});
	canvas.on('object:removed', (e) => {
		refresh_layer(e);
	});

	canvas.on('selection:created', (e) => {
		select_item_on_canvas(e);
	});

	canvas.on('selection:updated', (e) => {
		select_item_on_canvas(e);
	});
	canvas.on('selection:cleared', (e) => {
		clear_highlight();
	});
</script>

<div class="window">
	<div class="title_bar">Layer</div>
	<div class="content">
		{#each layer as o}
			<button
				class="item"
				class:active={o.id == selected?.id}
				onclick={() => select_item_on_layer(o)}
			>
				{o.name}
			</button>
		{/each}
	</div>
	<div class="controls">
		<button
			class="ctrl"
			onclick={() => {
				if (!canvas.getActiveObject()) return;
				canvas.remove(canvas.getActiveObject());
			}}
		>
			delete
		</button>
	</div>
</div>

<style>
	.window {
		max-width: 200px;
		border: 1px solid rgb(212, 212, 212);
		border-radius: 8px;
		overflow: hidden;
	}

	.title_bar {
		padding: 8px;
		border-bottom: 1px solid rgb(212, 212, 212);
		font-weight: 800;
		font-size: 1.1rem;
	}
	.content {
		height: 200px;
		overflow-x: auto;
	}

	.item {
		padding: 8px;
		border: none;
		background-color: transparent;
		width: 100%;
		border-bottom: 1px solid rgb(212, 212, 212);
	}
	.item.active {
		background-color: aliceblue;
	}

	.item:hover {
		background-color: aliceblue;
	}
</style>
