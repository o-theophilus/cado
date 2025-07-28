<script>
	import { token } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';

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

<Button --button-font-size="0.8rem" --button-height="32px" onclick={submit}>
	<Icon icon="logout" size="1.2" />
	Logout
</Button>
