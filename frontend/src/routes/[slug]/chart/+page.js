import { redirect } from '@sveltejs/kit';

export const load = async ({ fetch, params, parent }) => {
    let a = await parent();

    if (!a.locals.user.login) {
        throw redirect(307, `/?${new URLSearchParams({
            "module": "dialogue",
            "title": "Warning",
            "status": 201,
            "message": "Unauthorized Access",
        })}`);
    }

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