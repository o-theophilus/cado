import { redirect, error } from '@sveltejs/kit';
import { page_state, loading } from '$lib/store.svelte.js';
import { page } from '$app/state';


export const load = async ({ parent, url, fetch, params }) => {
    let a = await parent();
    let _url = page.url.href != "https://example.com/" ? page.url : url

    if (!a.locals.user.login) {
        throw redirect(307, `/?module=login&return_url=${_url.pathname}`);
    }

    page_state.searchParams = Object.fromEntries(_url.searchParams.entries());

    let backend = new URL(`${import.meta.env.VITE_BACKEND}/org/card/${params.slug}`)
    backend.search = _url.search
    let cards = await fetch(backend.href, {
        headers: {
            'Content-Type': 'application/json',
            Authorization: a.locals.token
        }
    });

    let org = await fetch(`${import.meta.env.VITE_BACKEND}/org/${params.slug}`, {
        headers: {
            'Content-Type': 'application/json',
            Authorization: a.locals.token
        }
    });


    org = await org.json();
    cards = await cards.json();
    loading.close()

    if (a.locals.user.key != org.org.user_key) {
        throw error(400, "unauthorized access")
    } else if (org.status == 200 && cards.status == 200) {
        return {
            ...org,
            ...cards
        }
    }
}
