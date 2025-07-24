<script>
	let { fabric, canvas } = $props();

	let selected_snap_point = { x: [], y: [] };
	let snap_point = { x: [], y: [] };
	let guidelines = [];
	let snap_threshold = 10;
	let active_guidelines = {
		x: { obj_point: null, point: 0, threshold: snap_threshold },
		y: { obj_point: null, point: 0, threshold: snap_threshold }
	};

	const update_snap_points = (o) => {
		snap_point = { x: [], y: [] };
		snap_point.x.push(0);
		snap_point.x.push(canvas.getWidth());
		snap_point.y.push(0);
		snap_point.y.push(canvas.getHeight());
		for (const x of canvas.getObjects()) {
			if (x.id != o.id) {
				snap_point.x.push(x.left);
				snap_point.x.push(x.left + (x.width * x.scaleX) / 2);
				snap_point.x.push(x.left + x.width * x.scaleX);
				snap_point.y.push(x.top);
				snap_point.y.push(x.top + (x.height * x.scaleY) / 2);
				snap_point.y.push(x.top + x.height * x.scaleY);
			}
		}
	};

	const clear_guidelines = () => {
		guidelines = [];
		for (const x of canvas.getObjects()) {
			if (x._type == 'guideline') {
				canvas.remove(x);
			}
		}

		active_guidelines = {
			x: { obj_point: null, point: 0, threshold: snap_threshold },
			y: { obj_point: null, point: 0, threshold: snap_threshold }
		};
	};

	const create_guideline = (type, x, active = false) => {
		let coords = type == 'vertical' ? [x, 0, x, canvas.getWidth()] : [0, x, canvas.getHeight(), x];
		const shp = new fabric.Line(coords, {
			stroke: '#ff0000',
			strokeWidth: 1,
			selectable: false,
			hasControls: false,
			evented: false,
			strokeDashArray: [5, 5],
			// opacity: 0.8,
			opacity: active ? 0.8 : 0.2,
			_type: 'guideline'
		});
		canvas.add(shp);
	};

	const update_selected_snap_points = (o) => {
		selected_snap_point.x.min = o.left;
		selected_snap_point.x.mid = o.left + (o.width * o.scaleX) / 2;
		selected_snap_point.x.max = o.left + o.width * o.scaleX;
		selected_snap_point.y.min = o.top;
		selected_snap_point.y.mid = o.top + (o.height * o.scaleY) / 2;
		selected_snap_point.y.max = o.top + o.height * o.scaleY;

		clear_guidelines();

		for (const i of snap_point.x) {
			if (Math.abs(i - selected_snap_point.x.min) < snap_threshold) {
				let threshold = Math.abs(i - selected_snap_point.x.min);
				if (threshold < active_guidelines.x.threshold) {
					active_guidelines.x.point = i;
					active_guidelines.x.obj_point = 'min';
					active_guidelines.x.threshold = threshold;
				}
				guidelines.push({
					type: 'vertical',
					point: i,
					obj_point: 'min'
				});
			}
			if (Math.abs(i - selected_snap_point.x.mid) < snap_threshold) {
				let threshold = Math.abs(i - selected_snap_point.x.mid);
				if (threshold < active_guidelines.x.threshold) {
					active_guidelines.x.point = i;
					active_guidelines.x.obj_point = 'mid';
					active_guidelines.x.threshold = threshold;
				}
				guidelines.push({
					type: 'vertical',
					point: i,
					obj_point: 'mid'
				});
			}
			if (Math.abs(i - selected_snap_point.x.max) < snap_threshold) {
				let threshold = Math.abs(i - selected_snap_point.x.max);
				if (threshold < active_guidelines.x.threshold) {
					active_guidelines.x.point = i;
					active_guidelines.x.obj_point = 'max';
					active_guidelines.x.threshold = threshold;
				}
				guidelines.push({
					type: 'vertical',
					point: i,
					obj_point: 'max'
				});
			}
		}
		for (const i of snap_point.y) {
			if (Math.abs(i - selected_snap_point.y.min) < snap_threshold) {
				let threshold = Math.abs(i - selected_snap_point.y.min);
				if (threshold < active_guidelines.y.threshold) {
					active_guidelines.y.point = i;
					active_guidelines.y.obj_point = 'min';
					active_guidelines.y.threshold = threshold;
				}
				guidelines.push({
					type: 'horizontal',
					point: i,
					obj_point: 'min'
				});
			}
			if (Math.abs(i - selected_snap_point.y.mid) < snap_threshold) {
				let threshold = Math.abs(i - selected_snap_point.y.mid);
				if (threshold < active_guidelines.y.threshold) {
					active_guidelines.y.point = i;
					active_guidelines.y.obj_point = 'mid';
					active_guidelines.y.threshold = threshold;
				}
				guidelines.push({
					type: 'horizontal',
					point: i,
					obj_point: 'mid'
				});
			}
			if (Math.abs(i - selected_snap_point.y.max) < snap_threshold) {
				let threshold = Math.abs(i - selected_snap_point.y.max);
				if (threshold < active_guidelines.y.threshold) {
					active_guidelines.y.point = i;
					active_guidelines.y.obj_point = 'max';
					active_guidelines.y.threshold = threshold;
				}
				guidelines.push({
					type: 'horizontal',
					point: i,
					obj_point: 'max'
				});
			}
		}

		for (const i of guidelines) {
			if (
				(i.type == 'vertical' && i.obj_point == active_guidelines.x.obj_point) ||
				(i.type == 'horizontal' && i.obj_point == active_guidelines.y.obj_point)
			) {
				create_guideline(i.type, i.point, true);
			} else {
				create_guideline(i.type, i.point);
			}
		}
	};

	canvas.on('selection:created', (e) => {
		update_snap_points(e.selected[0]);
	});

	canvas.on('selection:updated', (e) => {
		update_snap_points(e.selected[0]);
	});

	canvas.on('object:modified', (e) => {
		if (active_guidelines.x.obj_point == 'min') {
			e.target.left = active_guidelines.x.point;
		} else if (active_guidelines.x.obj_point == 'mid') {
			e.target.left = active_guidelines.x.point - (e.target.width * e.target.scaleX) / 2;
		} else if (active_guidelines.x.obj_point == 'max') {
			e.target.left = active_guidelines.x.point - e.target.width * e.target.scaleX;
		}

		if (active_guidelines.y.obj_point == 'min') {
			e.target.top = active_guidelines.y.point;
		} else if (active_guidelines.y.obj_point == 'mid') {
			e.target.top = active_guidelines.y.point - (e.target.height * e.target.scaleY) / 2;
		} else if (active_guidelines.y.obj_point == 'max') {
			e.target.top = active_guidelines.y.point - e.target.height * e.target.scaleY;
		}

		clear_guidelines();
	});

	canvas.on('object:moving', (e) => {
		update_selected_snap_points(e.target);
	});
</script>

<style>
</style>
