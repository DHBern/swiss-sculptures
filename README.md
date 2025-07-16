# Re/Sculpture Web App

This project is an interactive web application created for the **Re/Sculpture** exhibition at the **Nouveau Musée Bienne (NMB)** in collaboration with the **University of Bern, Institute of Art History**.
The application is developed using Svelte, incorporating JavaScript, TypeScript, HTML, and CSS, along with the MapLibre library for enhanced mapping functionalities.

## Project Structure

- **`src/`**: Contains the main source files for the project.
  - **`routes/`**: Reusable Svelte components.
    - **`+pages.svelte`**: Acts as a parent component with one of the three map variations (Map.svelte, MapNew.svelte and MapOld.svelte).
    - **`Map.svelte`**: The main map containing old and new information about the sculptures.
    - **`Popup.svelte`**: Handles the components that show sculpture information. It is a child component of all map variants.
    - **`Slideshow.svelte`**: Handles the slideshow of images for the sculptures with more than one image to be displayed inside the Popup component. It is a child of the popup component.
- **`static/`**: Static assets such as images and fonts.

## Prerequisites

Before you start, ensure you have the following installed:

- **Node.js** (v14 or later)
- **npm** (v6 or later)

## Getting Started locally

Follow these steps to run the project locally:

1. **Clone the repository**:

   ```bash
   https://github.com/DHBern/swiss-sculptures.git
   cd swiss-sculptures
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```
3. **convert the data**:
   This step requires python 3 with pandas installed
   ```bash
   npm run convert_data
   ```
4. **setup .env variables**
   create a `.env`-File (just use the template) and add a API key from maptiler
5. **Run the project locally**:
   ```bash
   npm run dev
   ```

## Updating the data

To update the data just edit the [data.csv](https://github.com/DHBern/swiss-sculptures/blob/main/data-conversion/data.csv) and [images.csv](https://github.com/DHBern/swiss-sculptures/blob/main/data-conversion/images.csv) in `/data-conversion`.
After a commit to the main branch, the page will automatically rebuild.

## Credits

This project is tested with BrowserStack.
