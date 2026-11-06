#!/usr/bin/env python3
"""Check Docgen output offline, not external URLs, CSS URLs, or JavaScript behavior."""

import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import unquote, urljoin, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.anchors = set()
        self.links = []
        self.panels = set()
        self.controls = []
        self.math_errors = []
        self.stack = []
        self.visible_text = []
        self.feed(text)
        if re.search(r'\bPARSE\s+ERROR\b', ''.join(self.visible_text)):
            self.math_errors.append('visible generated math PARSE ERROR')

    def handle_starttag(self, tag, attrs):
        attrs = {key: value or '' for key, value in attrs}
        ignored = tag in {'pre', 'code', 'script', 'style', 'template'} or any(value for _, value in self.stack)
        if tag not in {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}:
            self.stack.append((tag, ignored))
        if attrs.get('id'):
            self.anchors.add(attrs['id'])
        if tag == 'a' and attrs.get('name'):
            self.anchors.add(attrs['name'])
        if 'tab-panel' in attrs.get('class', '').split() and attrs.get('data-tab-id'):
            self.panels.add(attrs['data-tab-id'])
        if tag == 'label' and attrs.get('role') == 'tab':
            self.controls.append(attrs.get('id', ''))
        if tag == 'a' and attrs.get('href', '').startswith('#/tab/'):
            tab = unquote(attrs['href'][len('#/tab/'):])
            self.controls.append(tab if attrs.get('data-tab') == tab else '')
        else:
            key = {'a': 'href', 'link': 'href', 'img': 'src', 'script': 'src',
                   'iframe': 'src', 'source': 'src', 'video': 'src', 'audio': 'src',
                   'use': 'href', 'image': 'href'}.get(tag)
            if key and attrs.get(key):
                self.links.append(attrs[key])
        if tag == 'video' and attrs.get('poster'):
            self.links.append(attrs['poster'])
        if tag == 'merror' and not ignored:
            self.math_errors.append('generated MathML merror')

    def handle_startendtag(self, tag, attrs):
        depth = len(self.stack)
        self.handle_starttag(tag, attrs)
        del self.stack[depth:]

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        if not any(value for _, value in self.stack):
            self.visible_text.append(data)


def configured_base_path(config=None):
    # Only a top-level scalar is needed; avoid adding a YAML dependency.
    config = ROOT / 'docgen.yaml' if config is None else Path(config)
    text = config.read_text(encoding='utf-8')
    match = re.search(r'^base_path:\s*(.*?)\s*$', text, re.MULTILINE)
    if match is None:
        return ''
    scalar = match.group(1)
    match = re.fullmatch(r'''(?:"([^"\n]*)"|'([^'\n]*)'|([^\s#"']*))\s*(?:#.*)?''', scalar)
    if match is None:
        raise ValueError('Cannot read base_path from docgen.yaml; pass --base-path explicitly')
    return next(value for value in match.groups() if value is not None)


def normalize_base_path(base_path):
    if base_path == '':
        return ''
    if not base_path.startswith('/') or any(c in base_path for c in ['?', '#', '%', '\\']) or any(c.isspace() for c in base_path):
        raise ValueError('base path must be an absolute URL path without query or encoding')
    if any(part in ['.', '..'] for part in base_path.split('/')) or '//' in base_path:
        raise ValueError('base path must not contain dot segments or repeated slashes')
    return base_path.rstrip('/')


def page_url(path, site, base_path):
    # Keep .html: Docgen relative links resolve against the generated filename.
    return 'https://site.invalid' + base_path + '/' + path.relative_to(site).as_posix()


def target_path(url_path, site, base_path):
    decoded = unquote(url_path)
    if base_path and decoded != base_path and not decoded.startswith(base_path + '/'):
        raise ValueError('local URL is outside the configured project prefix')
    relative = decoded[len(base_path):].lstrip('/')
    target = (site / relative).resolve()
    if not target.is_relative_to(site):
        raise ValueError('local URL escapes the site directory')
    if target.is_dir():
        target = target / 'index.html'
    # Docgen emits clean sidebar URLs; GitHub Pages resolves these to .html.
    elif not target.exists() and not target.suffix:
        target = target.with_suffix('.html')
    target = target.resolve()
    if not target.is_relative_to(site):
        raise ValueError('local URL escapes the site directory')
    return target


def check_site(site, base_path='', docs=None):
    site = Path(site).resolve()
    base_path = normalize_base_path(base_path)
    errors = []
    pages = {path: Page(path.read_text(encoding='utf-8')) for path in sorted(site.rglob('*.html'))}
    if site / 'index.html' not in pages:
        errors.append('missing built homepage: index.html')
    if not (site / '.nojekyll').is_file():
        errors.append('missing Pages marker: .nojekyll')
    if docs is not None:
        docs = Path(docs)
        sources = sorted(path for path in docs.rglob('*.md') if '_include' not in path.relative_to(docs).parts)
        if not sources:
            errors.append('no authored Markdown pages found')
        for source in sources:
            relative = source.relative_to(docs)
            output = relative.with_name('index.html') if source.name == 'README.md' else relative.with_suffix('.html')
            if site / output not in pages:
                errors.append(f'missing built page for {relative.as_posix()}')
    checked = 0
    for source, page in pages.items():
        name = source.relative_to(site).as_posix()
        errors.extend(f'{name}: {error}' for error in page.math_errors)
        for tab in page.controls:
            if not tab or tab not in page.panels:
                errors.append(f'{name}: invalid tab control {tab!r}: matching nonempty tab panel required')
        origin = page_url(source, site, base_path)
        for link in page.links:
            try:
                raw = urlsplit(link)
                if raw.scheme or raw.netloc:
                    continue
                checked += 1
                url = urlsplit(urljoin(origin, link))
                target = target_path(url.path, site, base_path)
                if not target.is_file():
                    raise ValueError('target does not exist')
                fragment = unquote(url.fragment)
                if fragment and target.suffix == '.html':
                    if fragment not in pages[target].anchors:
                        raise ValueError('HTML fragment does not exist')
                if fragment and target.suffix == '.svg':
                    anchors = {node.get('id') for node in ET.parse(target).iter()}
                    if fragment not in anchors:
                        raise ValueError('SVG fragment does not exist')
            except (ValueError, KeyError, OSError, ET.ParseError) as error:
                errors.append(f'{name}: {link!r}: {error}')
    return errors, len(pages), checked


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', type=Path, default=ROOT / 'site')
    parser.add_argument('--docs', type=Path, default=ROOT / 'docs')
    parser.add_argument('--base-path', help='defaults to optional base_path in docgen.yaml, otherwise root')
    args = parser.parse_args()
    try:
        base_path = args.base_path if args.base_path is not None else configured_base_path()
        errors, pages, links = check_site(args.site, base_path, args.docs)
    except (ValueError, OSError) as error:
        parser.error(str(error))
    for error in errors:
        print(error)
    if errors:
        print(f'Failed: {len(errors)} site check errors.')
        return 1
    print(f'Checked {pages} built HTML pages and {links} local links/assets; fragments and page coverage passed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
