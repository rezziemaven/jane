# Jane

Beautifully simple static site generator.

Preview it here: [Jane Static Site Generator](https://rezziemaven.github.io/jane/)

## Usage

1. Clone this repository to your computer.
2. To test locally:
    1. Run the `main.sh` script to test locally. It should run successfully without errors.
    2. Visit [https://localhost:8888](https://localhost:8888) to view the dummy content in the `content` and `static` folders.
3. To alter the dummy generated content with your own:
    1. Replace the `content/` and `static/` folder content with your own content, and update the `static/index.css` and `template.html` if necessary.
    2. Re-run `main.sh` to preview the changes.
    3. Do ensure that the markdown in your `MD` files are formatted correctly, or this could result in an error.
4. To run this on GitHub Pages:
    1. Create a new repository in your account and upload the contents of this repository there.
    2. Change `jane` in `build.sh` to `REPO_NAME`, where `REPO_NAME` is the name of your repository.
    3. Run the `build.sh` script locally to rebuild the `docs/` folder.
    4. Open your repository's settings on GitHub and select `Pages` in the `Code and automation` section to [config the publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site#publishing-from-a-branch):
        - Set the source to the `main` branch and the `docs` directory.
        - Save the settings.
        - The `/docs` directory on your `main` branch will auto deploy to your GitHub Pages URL once something is in it.

## License

This project is under an [MIT License](/LICENSE.md).
