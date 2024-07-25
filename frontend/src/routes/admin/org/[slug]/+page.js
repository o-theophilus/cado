import { error } from '@sveltejs/kit';

export const load = async ({ fetch, params, parent }) => {
    let a = await parent();
    let resp = await fetch(`${import.meta.env.VITE_BACKEND}/organization/${params.slug}`, {
        method: 'get',
        headers: {
            'Content-Type': 'application/json',
            Authorization: a.locals.token
        },
    });
    resp = await resp.json();

    if (resp.status == 200) {

        if (
            !a.locals.user.access.includes('organization:view')
            && !(
                a.locals.user.organization_key == resp.organization.key
                && a.locals.user.access.some((x) => [
                    'organization:edit_logo',
                    'organization:edit_icon',
                    'organization:edit_organization',
                    'organization:edit_contact',
                    'organization:edit_social_media',
                    'organization:delete'
                ].includes(x))
            )
        ) {
            throw error(400, "unauthorized access")
        }


        return { ...resp }
    }
}