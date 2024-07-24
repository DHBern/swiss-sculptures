<script>
	import Map from './Map.svelte';
	import Swal from 'sweetalert2/dist/sweetalert2.js';
	import 'sweetalert2/dist/sweetalert2.min.css';

	function showPopup() {
		// @ts-ignore
		Swal.fire({
			icon: 'info',
			title: 'Info',
			html: `
				<b>Exposition suisse de sculpture interactive</b> <br>
				<p>Où les sculptures de l'Exposition suisse de sculpture étaient-elles visibles à l'origine ?
					Où se trouvent-elles aujourd'hui et à quoi ressemblent-elles ? La comparaison
					photographique révèle la postérité de cette série d'expositions.
					La carte de la sculpture suisse continuera de s'enrichir à l'avenir, et vous pouvez y
					contribuer. Veuillez soumettre vos photographies et souvenirs sur publics-arts.ch.
					Pour l'installation interactive, des données de crowdsourcing du site publics-arts.ch ont
					été rassemblées. Les numérisations proviennent de collections privées, de Wikimedia
					Commons et d'archives publiques. Le site web et l'installation ont été réalisés en
					coopération entre l'Institut d'histoire de l'art et les Humanités numériques de
					l'Université de Berne, avec le soutien de la Commission de digitalisation de l'Université
					de Berne.
				</p> <br>
				<b>Schweizerische Plastikausstellung interaktiv</b> <br>
				<p>
					Wo waren die Skulpturen der Schweizerischen Plastikausstellung jeweils zu sehen? Wo
					stehen sie jetzt und wie sehen sie aus? Der Fotovergleich zeigt das Nachleben der
					Ausstellungsreihe.
					Die Landkarte zur Schweizer Skulptur wird in Zukunft weiterwachsen. Sie können dazu
					beitragen: Bitte reichen Sie Ihre Fotografien und Erinnerungen ein unter publics-arts.ch.
					Für die interaktive Installation sind Crowdsourcing-Daten der Webseite publics-arts.ch
					aufbereitet. Die Digitalisate stammen aus Privatnachlässen, aus Wikimedia Commons
					und aus öffentlichen Archiven. Website und Installation wurden als Kooperation
					zwischen dem Institut für Kunstgeschichte und den Digital Humanities der Universität
					Bern realisiert. Gefördert von der Digitalisierungskommission der Universität Bern.
				</p> <br>
				<i>
					Réalisation / Umsetzung: Prof. Dr. Tobias Hodel (DH), Sebastian Flick (DH), Daniel
					Zeidan (DH), Nicolas Gränacher (IKG), Dr. Yvonne Schweizer (IKG)
				</i><br>
				<div class="logo-container">
					<img src="/logo.jpg" class="logo"><img src="unibe_logo.png" class="logo"><img src="SNF_logo_standard_web_color_pos_e.png" class="logo">
				</div>
			`,
			width: '50%',
			showCloseButton: true,
			showConfirmButton: false
		});
	}
</script>

<meta name="viewport" content="width=device-width, initial-scale=1" />
<link rel="stylesheet" href="https://unpkg.com/maplibre-gl@4.4.1/dist/maplibre-gl.css" />
<link rel="stylesheet" href="src/styles.css" />
<body style="margin: 0; padding: 0; overflow:hidden;">
	<Map />

	<!-- Footer/Legend -->

	<div class="grid-container">
		<div class="col-auto p">
			<h1>
				Exposition suisse de sculpture interactive / Schweizerische Plastikausstellung interaktiv
			</h1>
			<h3>
				Cliquez sur les points et les lignes pour voir plus de détails. / Für mehr Details klicken
				Sie auf die Punkte und Linien.
			</h3>
		</div>
		<div class="p" style="display:grid;">
			<div class="line-container">
				<div><img src="/red.svg" alt="red" class="svg" /></div>
				<div>
					<p class="l-text">emplacement d’origine (rouge) / ursprünglicher Standort (rot)</p>
				</div>
			</div>
			<div class="line-container">
				<div><img src="/blue.svg" alt="blue" class="svg" /></div>
				<div><p class="l-text">emplacement actuel (bleu) / aktueller Standort (blau)</p></div>
			</div>
			<button
				style="position: absolute; z-index:10; color:black; bottom:1vh; right:0.25vw; background-color: transparent; border: none;"
				on:click={showPopup}
			>
				<img src="/info.svg" alt="info" />
			</button>
		</div>
	</div>
</body>
