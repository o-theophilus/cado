import { error } from '@sveltejs/kit';
export const load = async ({ fetch, params, parent }) => {
    let resp = await fetch(`${import.meta.env.VITE_BACKEND}/card/${params.slug}`);
    resp = await resp.json();

    let a = await parent();

    if (a.locals.user.key != resp.card.user_key) {
        throw error(400, "unauthorized access")
    } else if (resp.status == 200) {
        return resp
    }
}