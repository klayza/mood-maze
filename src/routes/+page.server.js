import { redirect } from '@sveltejs/kit';

export const load = async (event) => {
	if (!event.locals.user) {
		return redirect(302, '/demo/lucia/login');
	} else {
		return { user: event.locals.user };
	}
};
