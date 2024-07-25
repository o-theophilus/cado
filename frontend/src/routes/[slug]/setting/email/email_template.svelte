<script>
	import { organization } from '$lib/store.js';
	import Template from '$lib/email_template.svelte';
</script>

<Template>
	<b> Dear {'{'}firstname{'}'}, </b>
	<br />
	<br />
	Please use the code below to change your email.
	<br />
	<br />
	<div
		style="
		text-align: center;
		font-size: x-large;
		padding: 16px;
		border: 2px solid #efefef;
		border-radius: 4px;
	"
	>
		<b> {'{'}code{'}'} </b>
	</div>
	<br />
	<br />
	This code is valid for a limited time. If you didn't request this, please disregard this message.
	<br />
	<br />
	Warm regards{#if $organization.name},
		<br /><br />
		<b>{$organization.name}</b>
	{/if}
</Template>
