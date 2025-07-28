export const load = async ({ fetch, params }) => {
    let resp = await fetch(`${import.meta.env.VITE_BACKEND}/card/${params.slug}`);
    resp = await resp.json();

    if (resp.status == 200) {
        return resp
    }
}