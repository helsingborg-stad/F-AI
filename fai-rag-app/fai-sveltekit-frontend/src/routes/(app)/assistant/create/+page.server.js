import { redirect } from '@sveltejs/kit';
import { SECRET_API_URL } from '$env/static/private';

export const actions = {
	create: async ({ request }) => {
		try {
			const formData = await request.formData();
			const data = Object.fromEntries(formData.entries());

			const response = await fetch(`${SECRET_API_URL}/api/rest/assistant/create`, {
				method: 'POSTXX',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(data)
			});
		} catch (e) {
			console.log(`CREATE ERROR: ${e.message}`);
		}

		redirect(303, '/assistant');
	}
};
