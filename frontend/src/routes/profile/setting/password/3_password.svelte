<script>
	import { loading, token, notify } from '$lib/store.svelte.js';

	import IG from '$lib/input_group.svelte';
	import { Button } from '$lib/button';
	import Icon from '$lib/icon.svelte';
	import Password from '$lib/auth/password_checker.svelte';
	import ShowPassword from '$lib/auth/password_show.svelte';

	let { form, active_card } = $props();
	let error = $state({});
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
			form.state = 0;
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
	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

	<IG
		name="Password"
		icon="key"
		error={error.password}
		bind:value={form.password}
		type={show_password ? 'text' : 'password'}
		placeholder="Password here"
	>
		{#snippet right()}
			<div class="right">
				<ShowPassword bind:show_password />
			</div>
		{/snippet}
		{#snippet down()}
			<Password password={form.password} />
		{/snippet}
	</IG>

	<IG
		name="Confirm Password"
		icon="key"
		error={error.confirm_password}
		bind:value={form.confirm_password}
		type={show_password ? 'text' : 'password'}
		placeholder="Password here"
	/>

	<div class="line">
		<Button primary onclick={validate}>Reset Password</Button>

		<Button
			onclick={() => {
				form.state = 0;
				form.code = null;
				form.password = null;
				form.confirm_password = null;
			}}
		>
			Cancel
			<Icon icon="close" />
		</Button>
	</div>
</form>

<style>
	.error {
		margin: var(--sp2) 0;
	}

	.right {
		padding-right: var(--sp2);
	}

	.line {
		display: flex;
		gap: var(--sp1);
	}
</style>
