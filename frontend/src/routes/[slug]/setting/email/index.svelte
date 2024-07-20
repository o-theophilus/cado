<script>
	import Card from '../card.svelte';

	import RequestCode from './1_request_code.svelte';
	import SubmitCode1 from './2_submit_code.svelte';
	import NewEmail from './3_new_email.svelte';
	import SubmitCode2 from './4_submit_code.svelte';

	let code;
	let email;
	let state = 0;
</script>

<Card>
	<svelte:fragment slot="title">Change Email</svelte:fragment>

	{#if state == 0}
		<RequestCode
			on:ok={() => {
				state = 1;
			}}
		/>
	{:else if state == 1}
		<SubmitCode1
			on:ok={(e) => {
				code = e.detail;
				state = 2;
			}}
		/>
	{:else if state == 2}
		<NewEmail
			{code}
			on:ok={(e) => {
				email = e.detail;
				state = 3;
			}}
		/>
	{:else if state == 3}
		<SubmitCode2
			{code}
			{email}
			on:ok={(e) => {
				state = 0;
			}}
		/>
	{/if}
</Card>

<style>
</style>
