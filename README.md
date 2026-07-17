# SciML blog starter

A small Quarto blog designed for mathematical and computational writing. It includes:

- equations and cross-references;
- BibTeX citations and a cite-this-post appendix;
- Python/Jupyter code cells;
- frozen computational output for older posts;
- categories, search, RSS, light/dark themes, and a responsive layout;
- a sample technical post and a reusable post template;
- GitHub Pages publishing through the `docs/` directory.

## 1. Personalize the site

Replace these placeholders across the project:

- `Alex Benanti`
- `alexbenanti`
- `Alex-Talks-Scientific-Computing-Machine-Learning`
- `alexander.benanti@stonybrook.edu`

The `site-url` in `_quarto.yml` must match the final public address. For a project site it normally has the form:

```text
https://alexbenanti.github.io/Alex-Talks-Scientific-Computing-Machine-Learning/
```

Replace `assets/profile-placeholder.svg` with your own image and update `about.qmd` if the filename changes.

## 2. Install and preview

Install Quarto from the official installer, then create a Python environment for executable posts:

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
quarto preview
```

### Windows PowerShell

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
quarto preview
```

## 3. Create a post

```bash
python scripts/new_post.py "Neural operators and classical approximation"
```

This creates a dated directory inside `posts/`. The new post starts with `draft: true`, so it appears during preview but not in the published site. Remove that line when the post is ready.

For a one-off post, you can also copy `templates/post/` manually.

## 4. Publish with GitHub Pages

Create an empty GitHub repository, then run:

```bash
git init
git add .
git commit -m "Create SciML blog"
git branch -M main
git remote add origin https://github.com/alexbenanti/Alex-Talks-Scientific-Computing-Machine-Learning.git
git push -u origin main
```

Render the site and push the generated `docs/` directory:

```bash
quarto render
git add docs
git commit -m "Publish site"
git push
```

In the GitHub repository, open **Settings → Pages** and choose:

- **Source:** Deploy from a branch
- **Branch:** `main`
- **Folder:** `/docs`

Future updates use the same cycle:

```bash
quarto render
git add .
git commit -m "Publish new post"
git push
```

## 5. Optional custom domain

Get the default `github.io` site working first. Then:

1. verify the domain in GitHub;
2. add the custom domain in **Settings → Pages**;
3. configure the DNS records with the domain registrar;
4. replace `site-url` in `_quarto.yml` with the custom domain;
5. render and push again;
6. enable HTTPS after GitHub completes its DNS and certificate checks.

## Recommended editorial workflow

- Keep unfinished posts as drafts.
- Use fixed publication dates, not dynamic dates such as `today`.
- Put shared references in `references.bib`.
- Give equations and figures labels such as `{#eq-stability}` and `#| label: fig-convergence`.
- Keep `freeze: true` for computational posts so old results do not need to be recomputed on every full-site render.
- State assumptions and limitations explicitly.

## Main files

```text
_quarto.yml                  Site configuration
index.qmd                    Home page and post listing
about.qmd                    Author page
styles.css                   Visual design
references.bib               Shared bibliography
posts/_metadata.yml          Defaults for all posts
posts/residual-error/        Sample technical post
templates/post/              Reusable draft template
scripts/new_post.py          Post generator
docs/                        Generated website after rendering
```

## Official documentation

- Quarto blogs: https://quarto.org/docs/websites/website-blog.html
- Quarto authoring: https://quarto.org/docs/get-started/authoring/
- Quarto citations: https://quarto.org/docs/authoring/citations.html
- Quarto cross-references: https://quarto.org/docs/authoring/cross-references.html
- Quarto on GitHub Pages: https://quarto.org/docs/publishing/github-pages.html
- GitHub Pages custom domains: https://docs.github.com/pages/configuring-a-custom-domain-for-your-github-pages-site
