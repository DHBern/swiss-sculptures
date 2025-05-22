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
			resetZoom();
		}
	}

	let class_side = $state('');
	let style_side = $state('');
	let close_fun = $state();
	let images_key = $state('');
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
			<div class="info" style="overflow-y: auto;">
				{#if side == 'left'}
					<button
						style="display: block; color:black; text-decoration: none; margin-top: 5px; margin-left: auto; margin-right: auto;"
						onclick={(ev) => {
							ev.preventDefault();
							showOtherPopup(popup_id, 'right');
						}}
					>
						<div style="display:flex; flex-gap: 5px; justify-content: center; align-items: center;">
							<p style="text-align: left; font-size: 0.8vw;">
								Aller à l’emplacement actuel
								<br />
								Zum aktuellen Standort
							</p>
							<p style="color: blue; font-size: 20px; border-radius: 100%;">&#9654;</p>
						</div>
					</button>
				{:else if side == 'right'}
					<button
						style="display: block; color:black; text-decoration: none; margin-top: 5px; margin-left: auto; margin-right: auto;"
						onclick={(ev) => {
							ev.preventDefault();
							showOtherPopup(popup_id, 'left');
						}}
					>
						<div style="display:flex; flex-gap: 5px; justify-content: center; align-items: center;">
							<p style="color: red; font-size: 20px; border-radius: 100%;">&#9664;</p>
							<p style="text-align: left; font-size: 0.8vw;">
								Aller à l’emplacement d'origine
								<br />
								Zum ursprünglichen Standort
							</p>
						</div>
					</button>
				{/if}

				<Hr classHr="my-8" />
				<h4>Artiste / Künstler*in:</h4>
				<p>
					{mdrow.artist} ({mdrow.expo})
				</p>
				<Hr classHr="my-8" />
				<h4>Lieu / Ort:</h4>
				<p>{side == 'left' ? mdrow.place_hist : mdrow.place_today}</p>
			</div>
		</div>
	{:else}
		<p>Loading...</p>
	{/if}
</div>
