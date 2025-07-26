<script>
	import { Button } from '.';

	let { children, ...props } = $props();
</script>

<Button
	{...props}
	--button-height="24px"
	--button-background-color="transparent"
	--button-border-radius="20px"
	--button-color="var(--cl4)"
	--button-font-size="0.8rem"
	--button-outline-color="var(--cl4)"
	outline
>
	{@render children()}
</Button>
