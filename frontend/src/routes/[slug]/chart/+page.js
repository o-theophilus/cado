import { error } from '@sveltejs/kit';
export const load = async ({ fetch, params, parent }) => {
    let a = await parent();
    // TODO: check login

    let resp = await fetch(`${import.meta.env.VITE_BACKEND}/card/chart/${params.slug}`, {
        headers: {
            'Content-Type': 'application/json',
            Authorization: a.locals.token
        }
    });

    resp = await resp.json();

    if (resp.status == 200) {
        return resp

    }
}