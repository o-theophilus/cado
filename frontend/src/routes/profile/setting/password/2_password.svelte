<script>
	import { loading, token, notify } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import { Row } from '$lib/layout';
	import { Icon } from '$lib/macro';

	let { form, error = $bindable(), active_card, status } = $props();
	let show_password = $state(false);

	const validate = async () => {
		error = {};

		if (!form.password) {
			error.password = 'this field is required';
		} else if (
			!/[a-z]/.test(form.password) ||
			!/[A-Z]/.test(form.password) ||
			!/[0-9]/.test(form.password) ||
			form.password.length < 8 ||
			form.password.length > 18
		) {
			error.password =
				'must include at least 1 lowercase letter, 1 uppercase letter, 1 number and must contain 8 - 18 characters';
		}

		if (!form.confirm_password) {
			error.confirm_password = 'this field is required';
		} else if (form.password && form.password != form.confirm_password) {
			error.confirm_password = 'Password and confirm password does not match';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Saving Password . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/password/3`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: token.value
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			status.value = 0;
			form.code = null;
			form.password = null;
			form.confirm_password = null;

			active_card.close();
			notify.open('Password Changed');
		} else {
			error = resp;
		}
	};
</script>

<form onsubmit={(e) => e.preventDefault()} novalidate autocomplete="off">
	<IG
		name="Password"
		icon="key"
		error={error.password}
		placeholder="Password here"
		type="password++"
		bind:value={form.password}
		bind:show_password
	></IG>
	<IG
		name="Confirm Password"
		icon="key"
		error={error.confirm_password}
		placeholder="Password here"
		type="password+"
		bind:value={form.confirm_password}
		bind:show_password
	/>

	<Row --row-gap="8px">
		<Button primary onclick={validate}>Reset Password</Button>

		<Button
			onclick={() => {
				error = {};
				form.code = null;
				form.password = null;
				form.confirm_password = null;
				status.value = 0;
			}}
		>
			Cancel
			<Icon icon="close" />
		</Button>
	</Row>
</form>

<style>
</style>
