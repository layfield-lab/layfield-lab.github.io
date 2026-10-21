"""Build the Layfield Lab site: wraps each page body in the shared header and footer.

Edit the page bodies in pages/*.html, then run:  python3 build.py
"""
from pathlib import Path

ROOT = Path(__file__).parent
NAV = [
    ("index.html", "Home"),
    ("research.html", "Research"),
    ("software.html", "Software"),
    ("publications.html", "Publications"),
    ("join.html", "Join the lab"),
]
TITLES = {
    "index.html": "Layfield Lab · Computational Chemistry",
    "research.html": "Research · Layfield Lab",
    "software.html": "Software · Layfield Lab",
    "publications.html": "Publications · Layfield Lab",
    "join.html": "Join the lab · Layfield Lab",
}
DESCRIPTION = (
    "The Layfield Lab at the University of St. Thomas uses computational chemistry "
    "(quantum chemistry, molecular dynamics and enhanced sampling) with undergraduate researchers."
)
DRAFT = (ROOT / "DRAFT").exists()


def page(name: str, body: str) -> str:
    current = ' aria-current="page"'
    nav = "\n".join(
        f'        <a href="{href}"{current if href == name else ""}>{label}</a>'
        for href, label in NAV
    )
    banner = (
        '<div class="draft-banner">Draft for review. Not yet published.</div>\n' if DRAFT else ""
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{TITLES[name]}</title>
  <meta name="description" content="{DESCRIPTION}">
  <link rel="stylesheet" href="assets/site.css">
</head>
<body>
{banner}<header class="site-header">
    <div class="wrap">
      <a class="brand" href="index.html"><strong>Layfield Lab</strong><span>Computational chemistry · University of St. Thomas</span></a>
      <nav class="nav" aria-label="Main">
{nav}
      </nav>
    </div>
  </header>
  <main>
{body}
  </main>
  <footer class="site-footer">
    <div class="wrap">
      <div>Layfield Lab, Department of Chemistry, University of St. Thomas, St. Paul, Minnesota</div>
      <div><a href="mailto:jlayfield@stthomas.edu">jlayfield@stthomas.edu</a> · <a href="https://github.com/layfield-lab">GitHub</a></div>
    </div>
  </footer>
</body>
</html>
"""


for href, _ in NAV:
    body = (ROOT / "pages" / href).read_text()
    (ROOT / href).write_text(page(href, body))
    print("built", href)
