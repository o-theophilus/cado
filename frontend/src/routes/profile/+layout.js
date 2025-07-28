import { redirect } from '@sveltejs/kit';

export const load = async ({ parent, fetch }) => {
    let a = await parent();

    if (!a.locals.user.login) {
        throw redirect(307, "/?module=login");
    }


    let org = await fetch(`${import.meta.env.VITE_BACKEND}/org`, {
        headers: {
            'Content-Type': 'application/json',
            Authorization: a.locals.token
        }
    });
    let card = await fetch(`${import.meta.env.VITE_BACKEND}/card`, {
        headers: {
            'Content-Type': 'application/json',
            Authorization: a.locals.token
        }
    });


    org = await org.json();
    card = await card.json();


    if (org.status == 200 && card.status == 200) {
        return {
            orgs: org.orgs,
            cards: card.cards,
        }
    }
}