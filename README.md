# Simon Wainaina

My personal website. The home page is my About page (with social links and recent essays), followed by my Résumé and Essays (Corner Thoughts), with reader comments on each essay.
Built with a small Python script (`build.py`) that turns Markdown files into web pages.

## Folder layout

```
config.py            site name, menu, social links, comments  ← edit first
build.py             the generator (you rarely need to touch this)
content/essays/      one .md file per essay
content/pages/       about.md (home page), resume.md, more.md, any new sections
templates/           the HTML layout of each kind of page
static/style.css     colours, fonts, spacing
.github/workflows/   publishes the site automatically on GitHub
```

## 1. Run it on your computer

You need Python 3.10 or newer.

```bash
cd "Website-Simon Wainaina"
python3 -m venv .venv
# Windows:      .venv\Scripts\activate
# Mac / Linux:  source .venv/bin/activate
pip install -r requirements.txt
python build.py --serve
```

Open http://localhost:8000. After editing a file, stop the preview (Ctrl+C) and run the last command again.

## 2. Write an essay

Create a file in `content/essays/`, for example `content/essays/my-new-essay.md`. The file name becomes the web address (`/essays/my-new-essay/`).

```
title: My New Essay
date: 2026-11-05
summary: One sentence that appears on the home page.

First paragraph...
```

Add `status: draft` to the header to keep an essay off the site while you work on it.

## 3. Publish it free on GitHub Pages

1. Create a free account at github.com.
2. Create a new **public** repository named exactly `YOUR-USERNAME.github.io`.
3. Upload this folder to it (with GitHub Desktop, or `git init`, `git add .`, `git commit -m "First version"`, `git push`).
4. In the repository, go to **Settings → Pages** and set **Source** to **GitHub Actions**.
5. In `config.py`, set `"url"` to `https://YOUR-USERNAME.github.io` and push again.

Every push to `main` rebuilds the site; the **Actions** tab shows progress. It goes live at `https://YOUR-USERNAME.github.io` within a minute or two.

## 4. Turn on comments (Cusdis)

Readers can comment without making an account. Each comment waits for your approval, so spam never appears on the site.

1. Sign up at https://cusdis.com and add a website.
2. Copy the **App ID** from the embed code it shows you.
3. Paste it into `config.py` as `"cusdis_app_id"` and push.
4. In Cusdis settings, turn on email notifications so you hear about new comments.

The free plan covers one site and 100 approved comments a month; Pro is $12/year if you outgrow it.

## 5. Social links

In `config.py`, fill in the full address of each profile under `"social"` (for example `"LinkedIn": "https://www.linkedin.com/in/your-profile"`). Filled-in links appear as buttons under "Find me online" on the home page and in the footer of every page; empty ones stay hidden. Add a line for any other network.

## 6. Profile picture and light / dark background

- **Profile picture:** copy your photo into `static/` and name it `profile.jpg`, then rebuild. It appears as a circle beside your name on the home page, and as the preview image when someone shares a link to your site. A square photo of at least 400×400 pixels looks best. To use a different file name (e.g. `me.png`), change `"photo"` in `config.py`.
- **Light / dark:** the sun/moon button at the end of the menu switches the background, and the site remembers each visitor's choice. In `config.py`, `"default_theme"` sets what first-time visitors see: `"system"` (match their device), `"dark"` or `"light"`.

## 7. Add another section

1. Create a file such as `content/pages/projects.md` (starting with `title: Projects`, a blank line, then the text).
2. In `config.py`, add `("Projects", "/projects/")` to `"nav"` where you want it in the menu.

## 8. News headlines on the More page

Every build pulls the latest headlines from news outlets' RSS feeds (Business Daily, The Standard, Daily Nation, Capital FM, Financial Times, CNBC, The Guardian, BBC, Al Jazeera, NPR) into four sections: Kenyan and world business, and Kenyan and world politics. GitHub rebuilds the site at 6 a.m. and 6 p.m. Nairobi time, so the list stays current on its own.

- To add, remove or swap a source, edit `"news"` in `config.py`. Each line is a name and the outlet's RSS address.
- If an outlet's feed is down, it's skipped and the rest still show.
- GitHub pauses scheduled rebuilds if the repository has no pushes for 60 days. It emails you first; click the link (or push any change) to keep them running.

## 9. Optional extras

- **Your own domain** (e.g. `simonwainaina.com`, about $10–15/year): buy it from a registrar, add it under Settings → Pages → Custom domain, follow GitHub's DNS instructions, then update `"url"` in `config.py`.
- **PDF résumé:** put `resume.pdf` in `static/`; the résumé page already links to it.
- **Restyle:** change the colour values at the top of `static/style.css`.
