import os
import base64
import mimetypes
import re

# Base directories
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
INPUT_FILE = os.path.join(BASE_DIR, 'html', 'index.html')
INPUT_DIR = os.path.dirname(INPUT_FILE)
OUTPUT_FILE = os.path.join(BASE_DIR, 'presentation_finale.html')


def get_mime_base64(file_path, skip_large_videos=False):
    """
    Convert file to base64 data URI.
    If skip_large_videos is True, skip video files larger than 10MB.
    """

    if not os.path.exists(file_path):
        print(f"Warning: missing file -> {file_path}")
        return None
    
    # Encode ALL files including large videos
    file_size = os.path.getsize(file_path)
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type and mime_type.startswith('video/') and file_size > 10 * 1024 * 1024:
        print(f"Encoding large video file ({file_size / (1024*1024):.1f}MB): {file_path} - This may take a while...")
    
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        # Fallback pour les types de fichiers non reconnus
        if file_path.lower().endswith('.ttf'):
            mime_type = 'font/ttf'
        elif file_path.lower().endswith('.woff'):
            mime_type = 'font/woff'
        elif file_path.lower().endswith('.woff2'):
            mime_type = 'font/woff2'
        else:
            mime_type = 'application/octet-stream'
    with open(file_path, 'rb') as f:
        data = base64.b64encode(f.read()).decode('utf-8')
    return f"data:{mime_type};base64,{data}"


def inline_css_link(match):
    href = match.group(1)
    # don't inline remote stylesheets
    if href.startswith('http') or href.startswith('//'):
        return match.group(0)
    css_path = os.path.normpath(os.path.join(INPUT_DIR, href))
    if not os.path.exists(css_path):
        print(f"CSS not found: {css_path}")
        return match.group(0)
    with open(css_path, 'r', encoding='utf-8') as f:
        css = f.read()

    # replace url(...) references inside the css
    def repl_url(m):
        url = m.group(1).strip(' \"\'')
        if url.startswith('http') or url.startswith('data:'):
            return f'url("{url}")'
        asset_path = os.path.normpath(os.path.join(os.path.dirname(css_path), url))
        data = get_mime_base64(asset_path, skip_large_videos=False)
        if data:
            return f'url("{data}")'
        # If conversion failed, adjust path relative to output file
        rel_to_base = os.path.relpath(asset_path, BASE_DIR)
        return f'url("{rel_to_base}")'

    css = re.sub(r'url\(([^)]+)\)', repl_url, css)
    return f"<style>\n{css}\n</style>"


def inline_js_tag(match):
    src = match.group(1)
    if src.startswith('http') or src.startswith('//'):
        return match.group(0)
    js_path = os.path.normpath(os.path.join(INPUT_DIR, src))
    if not os.path.exists(js_path):
        print(f"JS not found: {js_path}")
        return match.group(0)
    with open(js_path, 'r', encoding='utf-8') as f:
        return f"<script>\n{f.read()}\n</script>"


def inline_src_attr(match):
    """Replace src attributes while preserving other attributes like loading, style, etc."""
    src = match.group(1)
    if src.startswith('http') or src.startswith('//') or src.startswith('data:'):
        return match.group(0)
    asset_path = os.path.normpath(os.path.join(INPUT_DIR, src))
    data = get_mime_base64(asset_path, skip_large_videos=False)
    if data:
        return f'src="{data}"'
    # If conversion failed (e.g., large video), keep original relative path
    # but adjust it relative to the output file location (root of project)
    # Since output is at BASE_DIR and input is at BASE_DIR/html, we need to go into assets/
    if '../assets' in src:
        # Convert ../assets/... to ./assets/...
        new_src = src.replace('../assets', './assets')
        return f'src="{new_src}"'
    return match.group(0)


def replace_inline_style_urls(html):
    # replace style="...url('...')..."
    def repl(m):
        style = m.group(1)
        def repl_url2(n):
            url = n.group(1).strip('\"\'')
            if url.startswith('http') or url.startswith('data:') or url.startswith('//'):
                return f'url("{url}")'
            asset_path = os.path.normpath(os.path.join(INPUT_DIR, url))
            data = get_mime_base64(asset_path, skip_large_videos=False)
            if data:
                return f'url("{data}")'
            # If conversion failed, adjust path
            if '../assets' in url:
                new_url = url.replace('../assets', './assets')
                return f'url("{new_url}")'
            return f'url("{url}")'
        style2 = re.sub(r'url\(([^)]+)\)', repl_url2, style)
        return f'style="{style2}"'
    return re.sub(r'style="([^"]*)"', repl, html)


def bake_project():
    print('--- Creating standalone presentation ---')
    if not os.path.exists(INPUT_FILE):
        print(f'Input file not found: {INPUT_FILE}')
        return
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        html = f.read()

    # Inline local CSS links
    html = re.sub(r'<link[^>]+href="([^"]+)"[^>]*>', inline_css_link, html)

    # Inline local JS
    html = re.sub(r'<script[^>]+src="([^"]+)"[^>]*>\s*</script>', inline_js_tag, html)

    # Replace src attributes (images, video sources) with data: URIs for local files
    html = re.sub(r'src="([^"]+)"', inline_src_attr, html)

    # Replace data-background-image or other attributes that reference files
    def repl_data_bg(m):
        val = m.group(1)
        if val.startswith('http') or val.startswith('//') or val.startswith('data:'):
            return m.group(0)
        asset_path = os.path.normpath(os.path.join(INPUT_DIR, val))
        data = get_mime_base64(asset_path, skip_large_videos=False)
        if data:
            return f'data-background-image="{data}"'
        # If conversion failed, adjust path
        if '../assets' in val:
            new_val = val.replace('../assets', './assets')
            return f'data-background-image="{new_val}"'
        return m.group(0)

    html = re.sub(r'data-background-image="([^"]+)"', repl_data_bg, html)

    # Inline urls inside inline style attributes
    html = replace_inline_style_urls(html)

    # Inline urls inside <style> blocks (for fonts and other resources)
    def inline_style_block_urls(html):
        def repl_style_block(match):
            style_content = match.group(1)
            def repl_url(m):
                url = m.group(1).strip(' "\'')
                if url.startswith('http') or url.startswith('data:') or url.startswith('//'):
                    return f'url("{url}")'
                asset_path = os.path.normpath(os.path.join(INPUT_DIR, url))
                data = get_mime_base64(asset_path, skip_large_videos=False)
                if data:
                    return f'url("{data}")'
                # If conversion failed, try to adjust path
                if '../' in url:
                    new_url = url.replace('../', './')
                    return f'url("{new_url}")'
                return f'url("{url}")'
            style_content = re.sub(r'url\(([^)]+)\)', repl_url, style_content)
            return f'<style>{style_content}</style>'
        return re.sub(r'<style>(.*?)</style>', repl_style_block, html, flags=re.DOTALL)
    
    html = inline_style_block_urls(html)

    # Add CSS fix for parcours layout stability (before </head>)
    css_fix = '''
    <style>
        /* CSS fix for baked presentation: ensure parcours layout is stable with base64 images */
        #parcours-image {
            max-width: 100% !important;
            height: auto !important;
            display: block !important;
            image-rendering: -webkit-optimize-contrast;
            image-rendering: crisp-edges;
        }
        .parcours-container {
            position: relative !important;
            width: 90% !important;
            max-width: 1200px !important;
            margin: 0 auto !important;
        }
        .parcours-overlay {
            position: absolute !important;
            inset: 0 !important;
            top: 0 !important;
            left: 0 !important;
            width: 100% !important;
            height: 100% !important;
        }
        .transparent-backdrop {
            display: block !important;
            position: relative !important;
            width: 100% !important;
        }
        .parcours-container h2 {
            z-index: 100 !important;
            pointer-events: none !important;
        }
    </style>
'''
    html = html.replace('</head>', css_fix + '</head>')

    # Save
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'Standalone file written: {OUTPUT_FILE}')


if __name__ == '__main__':
    bake_project()
