<script>
	import { token } from '$lib/store.svelte.js';

	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';

	const submit = async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/logout`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: token.value
			}
		});

		resp = await resp.json();

		if (resp.status == 200) {
			token.value = resp.token;
			document.location = '/';
		}
	};
</script>

<Button size="small" extra="hover_red" onclick={submit}>
	<Icon icon="logout" size="1.2" />
	Logout
</Button>
