<script>
	import { EmailTemplate } from '$lib/layout';
</script>

<EmailTemplate>
	<b> Dear {'{'}firstname{'}'}, </b>
	<br />
	<br />
	Please use the verification code below to change your email.
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
	This verification code is valid for a limited time. If you didn't request this, please disregard this
	message.
	<br />
	<br />
	Warm regards,
	<br /><br />
	<b>Cado</b>
</EmailTemplate>
