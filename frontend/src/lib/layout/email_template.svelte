<script>
	import { page } from '$app/state';

	let { children } = $props();
</script>

<section
	style="
width: 100%;
max-width: 500px;
margin: auto;
line-height: 1.5
"
>
	<div
		style="
		padding: 20px 40px;
		display: flex;
		"
	>
		<img
			src="{page.url.origin}/logo.png"
			alt="Cado logo"
			style="
		height: 30px;
		"
		/>
	</div>

	<div
		class="content"
		style="
	border: 2px solid #efefef;
	border-radius: 4px;
	padding: 40px;"
	>
		{@render children()}
	</div>

	<div
		class="footer"
		style="
	text-align: center;
	padding: 20px 40px;
	font-size: x-small;
	color: grey;"
	>
		© 2025 | Cado
	</div>
</section>
