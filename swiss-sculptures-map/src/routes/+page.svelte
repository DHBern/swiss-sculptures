<script>
	import Map from './Map.svelte';
</script>

<meta name="viewport" content="width=device-width, initial-scale=1" />
<link rel="stylesheet" href="https://unpkg.com/maplibre-gl@4.4.1/dist/maplibre-gl.css" />
<body style="margin: 0; padding: 0; overflow:hidden;">
	<Map />

	<!-- Footer/Legend -->
	<style>
		.grid-container {
			position: absolute;
			bottom: 0;
			left: 0;
			width: 100%;
			height: 26vh;
			display: grid;
			grid-template-columns: auto auto;
			gap: 1rem;
			background-color: #d9d9d9;
			z-index: 10;
			overflow: hidden;
		}

		.col-auto {
			grid-column: span 1;
		}

		h1 {
			font-weight: bold;
			color: #333;
			margin-bottom: 1rem;
			font-size: 4vw;
		}

		h3 {
			font-weight: 600;
			color: #666;
			margin-bottom: 1rem;
			font-size: 2vw;
		}

		h4 {
			font-size: 28px;
			font-family: Inter;
		}

		.l-text {
			margine-top: 2vh;
			color: #888;
			font-size: 2vw;
			padding-left: 1vw;
		}
		.p {
			padding: 1vw;
		}
		.svg {
			width: 2vw;
			height: auto;
		}
		.line-container {
			display: flex;
			align-items: center;
			justify-content: center;
		}
	</style>
	<div class="grid-container">
		<div class="col-auto p">
			<h1>Schweizer Plastiken</h1>
			<h3>Klicken Sie auf die Punkte und Linien, um mehr Details zu sehen.</h3>
		</div>
		<div class="p" style="display:grid;">
			<div class="line-container">
				<div><img src="/red.svg" alt="red" class="svg" /></div>
				<div><p class="l-text">ursprünglicher Standort (Rot)</p></div>
			</div>
			<div class="line-container">
				<div><img src="/blue.svg" alt="blue" class="svg" /></div>
				<div><p class="l-text">neuer Standort (Blau)</p></div>
			</div>
		</div>
	</div>
</body>
