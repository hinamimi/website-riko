#!/usr/bin/env python3
"""Insert a YouTube embed into an existing static video page."""
import argparse
import html
from pathlib import Path
import re
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- youtube-embed:start -->'
END = '<!-- youtube-embed:end -->'


def video_id(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {'https', 'http'}:
        raise ValueError('YouTubeのhttps URLを指定してください')
    parts = parsed.path.strip('/').split('/')
    if parsed.netloc == 'youtu.be' and len(parts) == 1:
        value = parts[0]
    elif parsed.netloc in {'youtube.com', 'www.youtube.com', 'm.youtube.com'}:
        if parsed.path == '/watch':
            value = parse_qs(parsed.query).get('v', [''])[0]
        elif len(parts) == 2 and parts[0] in {'shorts', 'embed', 'live'}:
            value = parts[1]
        else:
            value = ''
    else:
        raise ValueError('YouTubeまたはyoutu.beのURLを指定してください')
    if not re.fullmatch(r'[A-Za-z0-9_-]{11}', value):
        raise ValueError('YouTube動画IDを確認してください')
    return value


def insert_embed(page: Path, url: str) -> None:
    identifier = video_id(url)
    source = page.read_text(encoding='utf-8')
    if source.count(START) != 1 or source.count(END) != 1 or source.index(START) > source.index(END):
        raise ValueError('埋め込み位置のコメントが見つかりません')
    title = re.search(r'<title>(.*?)</title>', source, re.S)
    label = html.escape(html.unescape(title.group(1)) if title else 'YouTube動画', quote=True)
    embed = f'''{START}
        <iframe class="video-frame" width="360" height="640"
          src="https://www.youtube-nocookie.com/embed/{identifier}"
          title="{label}" loading="lazy"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
          referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
        <p class="video-external"><a href="https://www.youtube.com/watch?v={identifier}">YouTubeで見る ↗</a></p>
        {END}'''
    before, remainder = source.split(START)
    _, after = remainder.split(END)
    page.write_text(before + embed + after, encoding='utf-8')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('slug', choices=['complex-impedance', 'lumped-circuit', 'gnd-return-earth', 'led-solar-duality', 'current-voltage-electrons'])
    parser.add_argument('url', help='YouTube watch / shorts / youtu.be URL')
    args = parser.parse_args()
    try:
        insert_embed(ROOT / 'public' / 'videos' / args.slug / 'index.html', args.url)
    except ValueError as error:
        parser.error(str(error))
    print(f'Updated public/videos/{args.slug}/index.html')


if __name__ == '__main__':
    main()
