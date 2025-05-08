<script>
	/** @type {{ data: import('./$types').LayoutData, children: import('svelte').Snippet }} */
	let { data, children } = $props();
	import '../styles.css';
</script>

<link rel="stylesheet" href="https://unpkg.com/maplibre-gl@4.4.1/dist/maplibre-gl.css" />
{@render children()}
