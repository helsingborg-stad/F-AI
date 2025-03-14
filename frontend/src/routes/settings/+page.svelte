<script lang="ts">
	import TextInput from '$lib/components/FormControl/TextInput.svelte';

	const settings = {
		fixedPin: '1234',
		openAiApiKey: null,
		brevoApiUrl: null,
		brevoApiKey: null
	};
</script>

<div class="p-4">
	<h1>Settings</h1>
	<p>Configure your settings here.</p>
	<form method="POST">
		<h2 class="mt-12">Basic</h2>
		<TextInput
			label="Fixed pin" value={settings.fixedPin}
			placeholder="NOTE: Make sure Brevo API is setup correctly to avoid account lock-out!" />

		<h2 class="mt-12">AI Settings</h2>
		<TextInput
			label="OpenAI API Key" value={settings.openAiApiKey}
			placeholder="sk-proj-..." />

		<h2 class="mt-12">E-mail (Brevo)</h2>
		<TextInput
			label="Brevo API URL" value={settings.brevoApiUrl}
			placeholder="" />
		<TextInput
			label="Brevo API Key" value={settings.brevoApiKey}
			placeholder="xkeysib-..." />
		<button class="btn btn-sm btn-primary mt-16">Save settings</button>
	</form>
</div>
