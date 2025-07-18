import { redirect, error } from '@sveltejs/kit';

export const load = async ({ parent, url, fetch, params }) => {
    let a = await parent();

    if (!a.locals.user.login) {
        throw redirect(307, `/?module=login&return_url=${url.pathname}`);
    }

    let org = await fetch(`${import.meta.env.VITE_BACKEND}/org/${params.slug}`, {
        headers: {
            'Content-Type': 'application/json',
            Authorization: a.locals.token
        }
    });

    let cards = await fetch(`${import.meta.env.VITE_BACKEND}/org/card/${params.slug}`, {
        headers: {
            'Content-Type': 'application/json',
            Authorization: a.locals.token
        }
    });

    org = await org.json();
    cards = await cards.json();


    if (a.locals.user.key != org.org.user_key) {
        throw error(400, "unauthorized access")
    } else if (org.status == 200 && cards.status == 200) {
        return {
            org: org.org,
            cards: cards.cards,
        }
    }
}