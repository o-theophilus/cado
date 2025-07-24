<script>
	import Button from '$lib/button/tag.svelte';
	import Icon from '$lib/icon.svelte';

	let { fabric, canvas } = $props();
</script>

<div class="tools">
	<Button
		no_grow
		onclick={() => {
			const obj = new fabric.Rect({
				top: 150,
				left: 150,
				width: 150,
				height: 150,
				fill: '#084d42',
				id: crypto.randomUUID()
			});
			obj.name = obj.type;
			canvas.add(obj);
		}}
	>
		<Icon icon="add"></Icon>
		Rect
	</Button>

	<Button
		no_grow
		onclick={() => {
			const obj = new fabric.Circle({
				top: 150,
				left: 150,
				radius: 50,
				fill: '#ff0000',
				id: crypto.randomUUID()
			});
			obj.name = obj.type;
			canvas.add(obj);
		}}
	>
		<Icon icon="add"></Icon>
		Circle
	</Button>

	<Button
		no_grow
		onclick={() => {
			const obj = new fabric.Text('Hello world!', {
				left: 50,
				top: 50,
				id: crypto.randomUUID()
			});
			obj.name = obj.type;
			canvas.add(obj);
		}}
	>
		<Icon icon="add"></Icon>
		Text
	</Button>

	<Button
		no_grow
		onclick={() => {
			// Create a link and trigger download
			let imageSrc = '';
			imageSrc = canvas.toDataURL({
				format: 'png'
			});
			const a = document.createElement('a');
			a.href = imageSrc;
			a.download = 'image.png';
			document.body.appendChild(a);
			a.click();
			document.body.removeChild(a);

			// const json = canvas.toJSON(['id', 'name']);
		}}
	>
		<Icon icon="add"></Icon>
		Download
	</Button>
</div>

<style>
	.tools {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp0);
	}
</style>
