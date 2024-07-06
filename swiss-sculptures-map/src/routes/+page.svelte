<script>
	import Map from './Map.svelte';
</script>

<meta name="viewport" content="width=device-width, initial-scale=1" />
<link rel="stylesheet" href="https://unpkg.com/maplibre-gl@4.4.1/dist/maplibre-gl.css" />
<body style="margin: 0; padding: 0;">
	<Map />

	<!-- Footer/Legend -->
	<style>
		.grid-container {
			position: absolute;
			bottom: 0;
			left: 0;
			width: 100%;
			height: 25.93vh;
			display: grid;
			grid-template-columns: auto auto;
			gap: 1rem;
			padding: 20px;
			background-color: #d9d9d9;
			z-index: 10;
		}

		.col-auto {
			grid-column: span 1;
		}

		h1 {
			font-weight: bold;
			color: #333;
			margin-bottom: 1rem;
			font-size: 48px;
		}

		h3 {
			font-weight: 600;
			color: #666;
			margin-bottom: 1rem;
			font-size: 36px;
		}

		h4 {
			font-size: 28px;
			font-family: Inter;
		}

		.l-text {
			margine-top: 2rem;
			color: #888;
			font-size: 28px;
		}
	</style>
	<div class="grid-container">
		<div class="col-auto">
			<h1>Schweizer Plastiken</h1>
			<h3>Klicken Sie auf die Punkte und Linien, um mehr Details zu sehen.</h3>
		</div>
		<div>
			<p class="l-text">&#128308 ursprünglicher Standort (Rot)</p>
			<p class="l-text">&#128309 neuer Standort (Blau)</p>
		</div>
	</div>
</body>
