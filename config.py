# Site settings. Edit these, then run:  python build.py

SITE = {
    "title": "Simon Wainaina",
    "tagline": "Senior at Williams College, MA, USA. Studying Economics and Mathematics. I am interested in finance, Economics research, East Africa, the world and the small things in between.",
    "author": "Simon Wainaina",

    # Profile picture shown on the home page. Put the image in static/
    # and write its file name here, e.g. "profile.jpg". Leave "" to hide it.
    "photo": "profile.jpg",

    # Colour scheme visitors see first: "system" (follow their device),
    # "dark" or "light". They can switch with the button in the menu.
    "default_theme": "system",

    # Name and one-line description of the essays section.
    "essays_title": "Essays",
    "essays_intro": "Essays on money, everyday economics, and occasional personal reflective pieces.",

    # Full public address of the site, no trailing slash.
    # GitHub Pages user site: "https://<your-username>.github.io"
    # Custom domain later:    "https://simonwainaina.com"
    "url": "https://SimonWainaina.github.io",

    # Leave "" if the site lives at the root of the domain (recommended:
    # name your GitHub repo YOUR-USERNAME.github.io). If you use a repo
    # like "website", set this to "/website".
    "base_path": "",

    # Comments (Cusdis). Paste the App ID from your Cusdis dashboard.
    # Leave empty to hide the comment box.
    "cusdis_app_id": "",

    # Social media. Fill in the full address of each profile you use.
    # Anything left as "" is hidden. Add new lines for other networks.
    "social": {
        "LinkedIn": "https://www.linkedin.com/in/simon-wainaina-79b6b2222/",
        "X": "https://x.com/Thinkingcorner0",
        "Instagram": "https://www.instagram.com/simon_wainaina1/",
        "Substack": "https://substack.com/@simonwainaina1",
        "Medium": "https://medium.com/@simonwainaina810",
        "GitHub": "https://github.com/simonWainaina",
        "Email": "mailto:simonwainaina810@gmail.com",
    },

    # Top menu, in this order: (label, path).
    # To add a section later (e.g. Projects): create content/pages/projects.md,
    # then add ("Projects", "/projects/") below.
    "nav": [
        ("About", "/"),
        ("Résumé", "/resume/"),
        ("Essays", "/essays/"),
        ("More", "/more/"),
    ],
}