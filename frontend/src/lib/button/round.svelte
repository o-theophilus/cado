<script>
	import { Button } from './';

	let { children, ...props } = $props();
</script>

<Button
	{...props}
	--button-padding-x="0"
	--button-width="32px"
	--button-height="32px"
	--button-border-radius="50%"
	--button-background-color="var(--input)"
	--button-color="var(--ft1)"
>
	{@render children()}
</Button>
