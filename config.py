# Site settings. Edit these, then run:  python build.py

SITE = {
    "title": "Simon Wainaina",
    "tagline": "Senior at Williams College studying Economics and Mathematics. Investment Analyst at Haba Capital, Nairobi. Interested in finance, economic research, geopolitics, and the small things in between.",
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

    # Shown on the Essays page, above the list: where else to read your work.
    # Names must match entries under "social" below.
    "essays_handles_intro": "Some of my handles go by the name Corner Thoughts. To interact with more of my essays and work, please see these handles:",
    "essays_handles": ["Facebook", "Medium", "Substack"],

    # Full public address of the site, no trailing slash.
    # GitHub Pages user site: "https://<your-username>.github.io"
    # Custom domain later:    "https://simonwainaina.com"
    "url": "https://simonwainaina.github.io",

    # Leave "" if the site lives at the root of the domain (recommended:
    # name your GitHub repo YOUR-USERNAME.github.io). If you use a repo
    # like "website", set this to "/website".
    "base_path": "",

    # Helps search engines understand who the site is about (shown to Google,
    # not on the page). Your social links below are added automatically.
    "person": {
        "job_title": "Investment Analyst Intern",
        "works_for": "Haba Capital",
        "alumni_of": "Williams College",
    },

    # Google Search Console: paste the code from the "HTML tag" verification
    # method here (only the content="..." part). Leave "" until you have one.
    "google_site_verification": "Ssyp0wM5DKjF2680zxeeOLK-iXYGZ_EILnw-p2g0suY",

    # Visitor statistics (GoatCounter, free). Sign up at goatcounter.com and
    # put the code you chose here, e.g. "simonwainaina" for
    # simonwainaina.goatcounter.com. Leave "" to turn statistics off.
    "goatcounter": "",

    # Comments (Cusdis). Paste the App ID from your Cusdis dashboard.
    # Leave empty to hide the comment box.
    "cusdis_app_id": "",

    # Social media. Fill in the full address of each profile you use.
    # Anything left as "" is hidden. Add new lines for other networks.
    "social": {
        "LinkedIn": "https://www.linkedin.com/in/simon-wainaina-79b6b2222/",
        "Facebook": "https://www.facebook.com/profile.php?id=61591318871935",
        "X": "https://x.com/Thinkingcorner0",
        "Instagram": "https://www.instagram.com/simon_wainaina1/",
        "Substack": "https://substack.com/@simonwainaina1",
        "Medium": "https://medium.com/@simonwainaina810",
        "GitHub": "",       # https://github.com/simonWainaina
        "Email": "mailto:simonwainaina810@gmail.com",
    },

    # Headlines on the In the News page, refreshed every time the site is built
    # (GitHub rebuilds it every morning and evening). Each feed is
    # ("Name shown on the site", "RSS feed address"). Remove a line to drop
    # a source; a source that's down is simply skipped.
    "news": {
        "page": "news",
        "per_section": 6,      # stories shown per section
        "per_source": 2,       # at most this many from any one outlet
        "max_age_days": 3,     # ignore anything older
        "skip_links_containing": ["/lifestyle/", "/life-and-style/", "/sport", "/entertainment/", "obituary"],
        "sections": [
            {"title": "Kenya: business & finance", "feeds": [
                ("Business Daily", "https://www.businessdailyafrica.com/service/rss/bd/1939132/feed.rss"),
                ("The Standard", "https://www.standardmedia.co.ke/rss/business.php"),
                ("Capital FM", "https://www.capitalfm.co.ke/business/feed/"),
            ]},
            {"title": "Kenya: politics & current affairs", "feeds": [
                ("The Standard", "https://www.standardmedia.co.ke/rss/politics.php"),
                ("Daily Nation", "https://nation.africa/kenya/rss.xml"),
                ("Capital FM", "https://www.capitalfm.co.ke/news/feed/"),
            ]},
            {"title": "Africa: business & finance", "feeds": [
                ("African Business", "https://african.business/feed"),
                ("Business Insider Africa", "https://africa.businessinsider.com/rss"),
                ("The Africa Report", "https://www.theafricareport.com/feed/"),
            ]},
            {"title": "Africa: politics & geopolitics", "feeds": [
                ("BBC Africa", "https://feeds.bbci.co.uk/news/world/africa/rss.xml"),
                ("France 24", "https://www.france24.com/en/africa/rss"),
                ("The Guardian", "https://www.theguardian.com/world/africa/rss"),
            ]},
            {"title": "World: business & finance", "feeds": [
                ("Financial Times", "https://www.ft.com/global-economy?format=rss"),
                ("CNBC", "https://www.cnbc.com/id/100727362/device/rss/rss.html"),
                ("The Guardian", "https://www.theguardian.com/business/economics/rss"),
            ]},
            {"title": "World: politics & geopolitics", "feeds": [
                ("BBC", "https://feeds.bbci.co.uk/news/world/rss.xml"),
                ("Al Jazeera", "https://www.aljazeera.com/xml/rss/all.xml"),
                ("The Guardian", "https://www.theguardian.com/world/rss"),
                ("NPR", "https://feeds.npr.org/1014/rss.xml"),
            ]},
        ],
    },

    # Top menu, in this order: (label, path).
    # To add a section later (e.g. Projects): create content/pages/projects.md,
    # then add ("Projects", "/projects/") below.
    "nav": [
        ("About", "/"),
        ("Résumé", "/resume/"),
        ("Essays", "/essays/"),
        ("In the News", "/news/"),
        ("More", "/more/"),
    ],
}