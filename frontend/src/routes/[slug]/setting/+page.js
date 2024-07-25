import { error } from '@sveltejs/kit';

export const load = async ({ fetch, params, parent }) => {
    let a = await parent();
    let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/${params.slug}`, {
        method: 'get',
        headers: {
            'Content-Type': 'application/json',
            Authorization: a.locals.token
        },
    });
    resp = await resp.json();

    if (resp.status == 200) {
        if (resp.user.slug != params.slug && !resp.user.access.some((x) => [
            "user:edit_photo",
            "user:edit_personal",
            "user:edit_organization",
            "user:edit_contact",
            "user:edit_social_media",
            "user:edit_access",
            "user:delete",
        ].includes(x))) {
            throw error(400, "unauthorized access")
        }

        return { ...resp }
    }
}
