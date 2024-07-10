<script>
	import { page } from '$app/stores';
	import Template from '$lib/email_template.svelte';
</script>

<Template>
	<b> Hello {'{'}firstname{'}'}, </b>
	<br />
	<br />
	Please use the code below to reset your password.
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
	This code is valid for a limited time. If you didn't request this, please disregard this message.
	<br />
	<br />
	Warm regards,
	<br />
	<br />
	<b>{'{'}organization_name{'}'}</b>
</Template>
