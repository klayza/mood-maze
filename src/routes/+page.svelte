<script>
	let { data } = $props();
	console.log(data);
</script>

{#if data.user}
	<h1>Welcome {data.user.username}</h1>
{:else}
	<h1>Welcome to SvelteKit</h1>
{/if}
<p>Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to read the documentation</p>
