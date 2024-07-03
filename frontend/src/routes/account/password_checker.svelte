<script>
	export let password = '';
</script>

<section>
	<div class:active={password && /[a-z]/.test(password)}>lowercase</div>
	<div class:active={password && /[A-Z]/.test(password)}>uppercase</div>
	<div class:active={password && /[0-9]/.test(password)}>number</div>
	<div class:active={password && password.length >= 8 && password.length <= 18}>8 - 18 length
	</div>
</section>

<style>
	section {
		display: flex;
		gap: 2px;
		width: 100%;
	}
	
	div {
		display: flex;
		justify-content: center;
		align-items: center;
		text-align: center;
		
		padding: 4px;
		
		font-size: 0.6rem;
		color: var(--ft2);
		background-color: var(--bg2);

		width: 100%;
	}
	
	.active {
		color: var(--ft1_b);
		background-color: var(--cl3);
	}
</style>
