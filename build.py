import os
import markdown
import html
import json

POSTS_DIR = "posts"
DIST_DIR = "dist"
TPL_DIR = "templates"

SITE_TITLE = "0u"
SITE_URL = "https://0u.nz"
SITE_DESC = "notes"

# ---------------- utils ----------------

def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def load_tpl(name):
    return read(os.path.join(TPL_DIR, name))

# ---------------- parse markdown ----------------

def parse_md(path):
    lines = read(path).splitlines()

    title = ""
    date = ""
    tags = []
    body_lines = []

    mode = "head"

    for line in lines:
        s = line.strip()

        if mode == "head":
            if s.startswith("# ") and not title:
                title = s[2:].strip()
            elif s.startswith("tags:"):
                tags = [t.strip() for t in s[5:].split(",") if t.strip()]
            elif s == "---":
                mode = "body"
            elif not date and s and s[0].isdigit():
                date = s
        else:
            line = line.replace('\t', ' ')
            body_lines.append(line)

    body_html = markdown.markdown(
        "\n".join(body_lines),
        extensions=[
            "tables", 
            "fenced_code"
        ]
    )
    
    import re
    def add_br_in_p(match):
        p_content = match.group(1)
        if re.search(r'<(?!/?(?:a|code|strong|em|span|br)\b)[^>]+>', p_content):
            return f'<p>{p_content}</p>'
        p_content = re.sub(r'(?<!\n)\n(?!\n)', '<br>\n', p_content)
        return f'<p>{p_content}</p>'
    
    body_html = re.sub(r'<p>(.*?)</p>', add_br_in_p, body_html, flags=re.DOTALL)

    return {
        "title": title,
        "date": date,
        "tags": tags,
        "body": body_html
    }

def extract_text(html_str):
    import re
    text = re.sub('<[^<]+?>', '', html_str)
    return text

def process_external_links(html_str):
    import re
    def add_target_blank(match):
        href = match.group(1)
        if href.startswith('/') or href.startswith('#'):
            return match.group(0)
        return f'<a href="{href}" target="_blank" rel="noopener noreferrer">'
    
    html_str = re.sub(r'<a href="([^"]+)">', add_target_blank, html_str)
    return html_str

# ---------------- build ----------------

def main():
    os.makedirs(DIST_DIR, exist_ok=True)
    os.makedirs(os.path.join(DIST_DIR, "tags"), exist_ok=True)

    post_tpl = load_tpl("post.html")
    index_tpl = load_tpl("index.html")
    tags_tpl = load_tpl("tags.html")
    friends_tpl = load_tpl("friends.html")
    about_tpl = load_tpl("about.html")
    tag_detail_tpl = load_tpl("tag-detail.html")
    search_tpl = load_tpl("search.html")
    base_style = load_tpl("base-style.html")
    
    nav_html = '''<nav>
  <a href="/">home</a>
  <a href="/tags">tags</a>
  <a href="/tree">tree</a>
  <a href="/friends">friends</a>
  <a href="/about">about</a>
  <a href="/search">search</a>
</nav>'''

    posts = []
    tags_map = {}

    # ---------- posts ----------
    for fn in sorted(os.listdir(POSTS_DIR), reverse=True):
        if not fn.endswith(".md") or fn == "about.md":
            continue

        data = parse_md(os.path.join(POSTS_DIR, fn))

        date_parts = data["date"].split("-")
        if len(date_parts) >= 2:
            year = date_parts[0]
            month = date_parts[1]
            out_name = fn.replace(".md", ".html")
            out_path = os.path.join("posts", year, month, out_name)
            file_url = f"posts/{year}/{month}/{out_name}"
        else:
            out_name = fn.replace(".md", ".html")
            out_path = out_name
            file_url = out_name

        tags_html = "".join(
            f'<a class="tag" href="/tags/{t}">{t}</a>'
            for t in data["tags"]
        )

        processed_body = process_external_links(data["body"])
        
        page = (
            post_tpl
            .replace("{{base_style}}", base_style)
            .replace("{{title}}", data["title"])
            .replace("{{date}}", data["date"])
            .replace("{{tags}}", tags_html)
            .replace("{{content}}", processed_body)
        )

        write(os.path.join(DIST_DIR, out_path), page)

        post = {
            "title": data["title"],
            "date": data["date"],
            "file": file_url,
            "tags": data["tags"],
            "content": extract_text(data["body"])[:500]
        }

        posts.append(post)

        for t in data["tags"]:
            tags_map.setdefault(t, []).append(post)

    # ---------- index ----------
    posts_sorted = sorted(posts, key=lambda p: p["date"], reverse=True)
    
    items = []
    for p in posts_sorted:
        items.append(f"""
<li>
  <a href="/{p["file"]}">{p["title"]}</a> - <span class="post-date">{p["date"]}</span>
</li>
""".strip())

    write(
        os.path.join(DIST_DIR, "index.html"),
        index_tpl.replace("{{posts}}", "\n".join(items)).replace("{{nav}}", nav_html)
    )

    # ---------- tags index page ----------
    tags_items = []
    for tag in sorted(tags_map.keys()):
        count = len(tags_map[tag])
        tags_items.append(f'<li><a href="/tags/{tag}">#{tag}</a> <span class="post-date">({count})</span></li>')
    
    tags_page = (
        tags_tpl
        .replace("{{site_title}}", SITE_TITLE)
        .replace("{{base_style}}", base_style)
        .replace("{{nav}}", nav_html)
        .replace("{{tags_list}}", ''.join(tags_items))
    )
    write(os.path.join(DIST_DIR, "tags", "index.html"), tags_page)

    # ---------- friends page ----------
    friends_list_html = ""
    try:
        with open(os.path.join("data", "friends.json"), encoding="utf-8") as f:
            friends_data = json.load(f)
            friends_items = []
            for friend in friends_data.get("friends", []):
                friends_items.append(f'<li><a href="{friend["url"]}">{friend["name"]}</a></li>')
            friends_list_html = "\n".join(friends_items)
    except:
        friends_list_html = ""

    friends_page = (
        friends_tpl
        .replace("{{site_title}}", SITE_TITLE)
        .replace("{{base_style}}", base_style)
        .replace("{{nav}}", nav_html)
        .replace("{{friends_list}}", friends_list_html)
    )
    os.makedirs(os.path.join(DIST_DIR, "friends"), exist_ok=True)
    write(os.path.join(DIST_DIR, "friends", "index.html"), friends_page)

    # ---------- about page ----------
    about_content_html = ""
    try:
        about_md_path = os.path.join(POSTS_DIR, "about.md")
        if os.path.exists(about_md_path):
            with open(about_md_path, encoding="utf-8") as f:
                about_raw = f.read()
            about_content_html = f'<article>{markdown.markdown(about_raw, extensions=["fenced_code"])}</article>'
    except:
        about_content_html = ""

    about_page = (
        about_tpl
        .replace("{{site_title}}", SITE_TITLE)
        .replace("{{base_style}}", base_style)
        .replace("{{nav}}", nav_html)
        .replace("{{content}}", about_content_html)
    )
    os.makedirs(os.path.join(DIST_DIR, "about"), exist_ok=True)
    write(os.path.join(DIST_DIR, "about", "index.html"), about_page)

    # ---------- search page ----------
    posts_json = json.dumps(posts, ensure_ascii=False)
    search_page = (
        search_tpl
        .replace("{{site_title}}", SITE_TITLE)
        .replace("{{base_style}}", base_style)
        .replace("{{nav}}", nav_html)
        .replace("{{posts_json_data}}", posts_json)
    )
    os.makedirs(os.path.join(DIST_DIR, "search"), exist_ok=True)
    write(os.path.join(DIST_DIR, "search", "index.html"), search_page)

    # ---------- tag detail pages ----------
    for tag, plist in tags_map.items():
        li = "\n".join(
            f'<li><a href="/{p["file"]}">{p["title"]}</a> - <span class="post-date">{p["date"]}</span></li>'
            for p in plist
        )

        tag_page = (
            tag_detail_tpl
            .replace("{{tag}}", tag)
            .replace("{{site_title}}", SITE_TITLE)
            .replace("{{base_style}}", base_style)
            .replace("{{nav}}", nav_html)
            .replace("{{posts_list}}", li)
        )

        os.makedirs(os.path.join(DIST_DIR, "tags", tag), exist_ok=True)
        write(os.path.join(DIST_DIR, "tags", tag, "index.html"), tag_page)

    # ---------- tree page ----------
    tree_tpl = load_tpl("tree.html")
    
    # 构建树形结构
    from collections import defaultdict
    tree_structure = defaultdict(lambda: defaultdict(list))
    
    for p in posts:
        date_parts = p["date"].split("-")
        if len(date_parts) >= 2:
            year = date_parts[0]
            month = date_parts[1]
            tree_structure[year][month].append(p)
    
    # 生成树形文本
    tree_lines = ["posts/"]
    years = sorted(tree_structure.keys(), reverse=True)
    
    for i, year in enumerate(years):
        is_last_year = (i == len(years) - 1)
        year_prefix = "└── " if is_last_year else "├── "
        tree_lines.append(f"{year_prefix}{year}/")
        
        months = sorted(tree_structure[year].keys(), reverse=True)
        for j, month in enumerate(months):
            is_last_month = (j == len(months) - 1)
            month_indent = "    " if is_last_year else "│   "
            month_prefix = "└── " if is_last_month else "├── "
            tree_lines.append(f"{month_indent}{month_prefix}{month}/")
            
            posts_in_month = sorted(tree_structure[year][month], key=lambda x: x["date"], reverse=True)
            for k, post in enumerate(posts_in_month):
                is_last_post = (k == len(posts_in_month) - 1)
                post_indent = month_indent + ("    " if is_last_month else "│   ")
                post_prefix = "└── " if is_last_post else "├── "
                tree_lines.append(f'{post_indent}{post_prefix}<a href="/{post["file"]}">{post["title"]}</a>')
    
    tree_content = "\n".join(tree_lines)
    
    tree_page = (
        tree_tpl
        .replace("{{site_title}}", SITE_TITLE)
        .replace("{{base_style}}", base_style)
        .replace("{{nav}}", nav_html)
        .replace("{{tree_content}}", tree_content)
    )
    os.makedirs(os.path.join(DIST_DIR, "tree"), exist_ok=True)
    write(os.path.join(DIST_DIR, "tree", "index.html"), tree_page)

    # ---------- RSS ----------
    rss_items = []
    for p in posts:
        rss_items.append(f"""
<item>
<title>{html.escape(p["title"])}</title>
<link>{SITE_URL}/{p["file"]}</link>
<guid>{SITE_URL}/{p["file"]}</guid>
<pubDate>{p["date"]}</pubDate>
</item>
""".strip())

    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
<title>{SITE_TITLE}</title>
<link>{SITE_URL}/</link>
<description>{SITE_DESC}</description>
{''.join(rss_items)}
</channel>
</rss>
"""

    write(os.path.join(DIST_DIR, "rss.xml"), rss)


if __name__ == "__main__":
    main()
