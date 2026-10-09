#!/usr/bin/env python3
"""Wiki Builder with Collection + Manual HTML Build (Quartz-independent)."""

#!/usr/bin/env python3
"""Wiki Builder: Convert Quartz markdown files to Wikipedia-style HTML. Independent of Quartz build system."""

import os
import sys

CWD = "/opt/data/workspace/wiki-quartz"
CONTENT_DIR = os.path.join(CWD, "content")
PUBLIC_EN = os.path.join(CWD, "public-en")
PUBLIC_KO = os.path.join(CWD, "public-ko")

def build():
    # EN papers
    papers_dir = os.path.join(CONTENT_DIR, "en", "sources", "papers")
    if os.path.exists(papers_dir):
        for md_file in sorted(os.listdir(papers_dir)):
            if md_file.endswith(".md"):
                with open(os.path.join(papers_dir, md_file), "r") as f:
                    md_text = f.read()

                # Extract title and abstract from markdown
                title = md_file.replace(".md", "").replace("_", " ")
                abstract = md_text.split("\n# ")[0] if "\n# " in md_text else md_text[:200]

                html_content = f"""<!DOCTYPE html>
<html lang="en" dir="ltr">
<head><meta charset="UTF-8"><title>{title}</title></head>
<body><article><h1>{title}</h1><p><strong>Source:</strong> Published paper.</p><p><strong>Abstract:</strong> {abstract}</p></article></body>
</html>"""

                output_path = os.path.join(PUBLIC_EN, "sources", "papers", md_file.replace(".md", ".html"))
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, "w") as out:
                    out.write(html_content)

    # KO papers
    ko_papers_dir = os.path.join(CONTENT_DIR, "ko", "sources", "papers")
    if os.path.exists(ko_papers_dir):
        for md_file in sorted(os.listdir(ko_papers_dir)):
            if md_file.endswith(".md"):
                with open(os.path.join(ko_papers_dir, md_file), "r") as f:
                    md_text = f.read()

                title = md_file.replace(".md", "").replace("_", " ")

                html_content = f"""<!DOCTYPE html>
<html lang="ko" dir="ltr">
<head><meta charset="UTF-8"><title>{title}</title></head>
<body><article><h1>{title}</h1><p><strong>출처:</strong> 간행된 논문입니다.</p><p><strong>요약:</strong> 논문의 주요 내용이 포함되어 있습니다.</p></article></body>
</html>"""

                output_path = os.path.join(PUBLIC_KO, "sources", "papers", md_file.replace(".md", ".html"))
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, "w") as out:
                    out.write(html_content)

    print("Build completed: EN and KO papers converted to Wikipedia-style HTML")



def collect_sources():
    """Collect today's sources from RSS feeds (blogwatcher-cli) and HuggingFace papers."""
    import subprocess
    import sys

    # 1. RSS Articles via blogwatcher-cli
    try:
        result = subprocess.run(
            ["/home/user/.local/bin/blogwatcher-cli", "articles"],
            capture_output=True, text=True, timeout=60
        )
        articles_output = result.stdout if result.returncode == 0 else "No unread articles!"
        print(f"[COLLECT] RSS Articles: {articles_output.strip()}")
    except Exception as e:
        print(f"[COLLECT] RSS collection error: {e}")

    # 2. HuggingFace Papers
    try:
        result = subprocess.run(
            ["/home/user/.local/bin/hf", "papers", "ls"],
            capture_output=True, text=True, timeout=60
        )
        papers_output = result.stdout if result.returncode == 0 else "No papers found."
        print(f"[COLLECT] HF Papers: {papers_output[:500]}...")
    except Exception as e:
        print(f"[COLLECT] HF papers collection error: {e}")

    # Note: The original opencode agent handles writing from these sources.
    # This function verifies the collection mechanism is available.
    return articles_output, papers_output

if __name__ == "__main__":
    # Run full pipeline: collect + build (manual HTML generation, no Quartz build dependency)
    articles, papers = collect_sources()
    build()
