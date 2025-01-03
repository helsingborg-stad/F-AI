export interface MenuItem {
	label: string;
	path: string;
}

export type Message = {
	sender: 'user' | 'bot';
	text: string;
}

// Dummy export to prevent empty module at runtime.
// Fixes Storybook error where module is empty after TypeScript compilation.
export const __types = {};
