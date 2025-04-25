<script>
	import Slideshow from './Slideshow.svelte';
	import { Hr } from 'flowbite-svelte';

	let {
		metadata,
		popup_id = $bindable(),
		side,
		showLeft = $bindable(false),
		showRight = $bindable(false),
		resetZoom
	} = $props();


	const idx = $derived(metadata.findIndex((m) => m.id === popup_id));
	const mdrow = $derived(metadata[idx]);

	function closeL() {
		showLeft = false;
	}

	function closeR() {
		// Retrieve the value of showLeft from the event
		showRight = false;
	}

	function showOtherPopup(id, which) {
		if (id !== undefined) {
			popup_id = id;
			if (which === 'left') {
				showLeft = true;
			} else if (which === 'right') {
				showRight = true;
			}
			// resetZoom();
		}
	}

	let class_side = '';
	let style_side = '';
	let close_fun;
	let images_key = '';
	switch (side) {
		case 'left':
			class_side = 'left';
			style_side =
				'position: relative; overflow: hidden; height: 37.035vh; width: auto; max-height: 37.035vh; border-style: solid; border-color:red;';
			close_fun = closeL;
			images_key = 'images_hist';
			break;
		case 'right':
			class_side = 'right';
			style_side =
				'position: relative; overflow: hidden; height: 37.035vh; width: 100%; min-height: 37.035vh; border-style: solid; border-color:blue;';
			close_fun = closeR;
			images_key = 'images_today';
			break;
	}
</script>

<div class={class_side}>
	<button class="close-btn" onclick={close_fun}>x</button>
	{#if mdrow}
		<div class="grid-item">
			<div class="popup_title">{mdrow.title}</div>
			<div class="bg-red-300" style={style_side}>
				<Slideshow images={mdrow[images_key]} />
			</div>
			<div class="info">
				{#if side == 'left'}
					<a
						href="#"
						style="color:black; text-decoration: none;"
						onclick={(ev) => {
							ev.preventDefault();
							showOtherPopup(popup_id, 'right');
						}}
					>
						<span style="font-size: 0.8vw;"
							>aller à l’emplacement actuel / zum aktuellen Standort</span
						>
						<span style="color: blue;">&#9654;</span>
					</a>
				{:else if side == 'right'}
					<a
						href="#"
						style="color:black; text-decoration: none;"
						onclick={(ev) => {
							ev.preventDefault();
							showOtherPopup(popup_id, 'left');
						}}
					>
						<span style="color: red;">&#9664;</span>
						<span style="font-size: 0.8vw;"
							>aller à l’emplacement d’origine / zum ursprünglichen Standort</span
						>
					</a>
				{/if}

				<Hr classHr="my-8" />
				<h4>Artiste / Künstler*in:</h4>
				<p>
					{mdrow.artist} ({mdrow.expo})
				</p>
				<Hr classHr="my-8" />
				<h4>Lieu / Ort:</h4>
				<p>{mdrow.place_hist}</p>
			</div>
		</div>
	{:else}
		<p>Loading...</p>
	{/if}
</div>
