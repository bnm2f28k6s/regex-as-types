"""Offline checker regression tests using isolated sites, never network requests."""

import importlib.util
from html import escape
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('site_check', ROOT / 'scripts/check-site.py')
assert SPEC is not None and SPEC.loader is not None
site_check = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(site_check)


class SiteCheckTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=os.environ.get('TMPDIR'))
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.site = self.root / 'site'
        self.docs = self.root / 'docs'
        self.write(self.site, '.nojekyll', '')
        self.write(self.site, 'index.html', '<h1 id="home">Home</h1>')
        self.write(self.docs, 'README.md', '# Home')

    def write(self, root, name, text):
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        return path

    def errors(self, base='/project'):
        return site_check.check_site(self.site, base, self.docs)[0]

    def test_explicit_html_relative_links_queries_and_encoded_anchors(self):
        self.write(self.site, 'index.html', '<h1 id="home">Home</h1><a href="/project/nested/guide.html?mode=1#hello%20world">Guide</a>')
        self.write(self.site, 'nested/guide.html', '<h1 id="hello world">Guide</h1><a href="../index.html#home">Home</a><a href="#hello%20world">Again</a>')
        self.write(self.docs, 'nested/guide.md', '# Guide')
        self.assertEqual(self.errors(), [])

    def test_clean_navigation_urls_resolve_to_html(self):
        self.write(self.site, 'index.html', '<a href="/project/guide#ok">Guide</a>')
        self.write(self.site, 'guide.html', '<h1 id="ok">Guide</h1>')
        self.assertEqual(self.errors(), [])

    def test_missing_clean_url_and_markdown_link_fail(self):
        self.write(self.site, 'index.html', '<a href="missing">Missing</a><a href="guide.md">Markdown</a>')
        self.write(self.site, 'guide.html', '<h1>Guide</h1>')
        self.assertEqual(len(self.errors()), 2)
        self.assertTrue(all('target does not exist' in error for error in self.errors()))

    def test_html_filename_is_canonical_even_for_same_page_query(self):
        self.write(self.site, 'guide.html', '<h1 id="ok">Guide</h1><a href="?q=1#ok">Again</a>')
        self.assertEqual(self.errors(), [])

    def test_nested_readme_directory_indexes_and_project_home(self):
        self.write(self.site, 'index.html', '<a href="/project/levels/">Levels</a><a href="/project">Home</a>')
        self.write(self.site, 'levels/index.html', '<h1 id="levels">Levels</h1><a href="#levels">Again</a>')
        self.write(self.docs, 'levels/README.md', '# Levels')
        self.assertEqual(self.errors(), [])

    def test_direct_assets_encoded_paths_and_svg_fragments(self):
        self.write(self.site, 'index.html', '<img src="/project/my%20chart.svg#cell"><script src="app.js"></script><link href="style.css" rel="stylesheet">')
        self.write(self.site, 'my chart.svg', '<svg xmlns="http://www.w3.org/2000/svg"><g id="cell"/></svg>')
        self.write(self.site, 'app.js', '')
        self.write(self.site, 'style.css', '')
        self.assertEqual(self.errors(), [])
        self.write(self.site, 'my chart.svg', '<svg xmlns="http://www.w3.org/2000/svg"/>')
        self.assertIn('SVG fragment does not exist', self.errors()[0])
        self.write(self.site, 'my chart.svg', '<svg>')
        self.assertTrue(self.errors())

    def test_missing_page_asset_and_fragment_fail(self):
        self.write(self.site, 'index.html', '<a href="missing.html">Missing</a><img src="missing.svg"><a href="#missing">Anchor</a>')
        errors = self.errors()
        self.assertEqual(len(errors), 3)
        self.assertEqual(sum('target does not exist' in error for error in errors), 2)
        self.assertIn('HTML fragment does not exist', errors[2])

    def test_missing_project_prefix_and_double_prefix_fail(self):
        self.write(self.site, 'index.html', '<a href="/guide.html">Wrong root</a><a href="/project/project/guide.html">Double</a>')
        self.write(self.site, 'guide.html', '<h1>Guide</h1>')
        errors = self.errors()
        self.assertEqual(len(errors), 2)
        self.assertIn('outside the configured project prefix', errors[0])
        self.assertIn('target does not exist', errors[1])

    def test_encoded_path_escape_and_symlink_escape_fail(self):
        outside = self.write(self.root, 'outside.html', '<h1>Outside</h1>')
        (self.site / 'escape.html').symlink_to(outside)
        (self.site / 'nested').mkdir()
        (self.site / 'nested/index.html').symlink_to(outside)
        self.write(self.site, 'index.html', '<a href="/project/%2e%2e/outside.html">Escape</a>'
                   '<a href="escape.html">Symlink</a><a href="escape">Clean</a><a href="nested/">Index</a>')
        errors = self.errors()
        self.assertEqual(len(errors), 4)
        self.assertTrue(all('escapes the site directory' in error for error in errors))

    def test_external_links_are_not_checked(self):
        self.write(self.site, 'index.html', '<a href="https://unreachable.invalid/no-page">External</a><a href="//unreachable.invalid/">External</a><a href="mailto:test@example.invalid">Mail</a><img src="data:image/png;base64,abc">')
        self.assertEqual(self.errors(), [])

    def test_authored_coverage_excludes_include_assets(self):
        self.write(self.docs, '_include/raw.md', '# Copied asset')
        self.assertEqual(self.errors(), [])
        self.write(self.docs, 'unlinked.md', '# Unlinked')
        self.assertIn('missing built page for unlinked.md', self.errors())

    def test_empty_and_missing_build_fail(self):
        (self.site / 'index.html').unlink()
        (self.site / '.nojekyll').unlink()
        for errors in [self.errors(), site_check.check_site(self.root / 'absent', '/project', self.docs)[0]]:
            self.assertIn('missing built homepage: index.html', errors)
            self.assertIn('missing Pages marker: .nojekyll', errors)

    def test_empty_and_missing_docs_fail(self):
        (self.docs / 'README.md').unlink()
        self.write(self.docs, '_include/asset.md', '# Not authored')
        self.assertIn('no authored Markdown pages found', self.errors())
        self.assertIn('no authored Markdown pages found', site_check.check_site(self.site, '', self.root / 'absent')[0])

    def test_root_hosting_and_named_anchor(self):
        self.write(self.site, 'index.html', '<a name="old"></a><a href="/#old">Root</a>')
        self.assertEqual(self.errors('/'), [])
        self.assertEqual(self.errors(''), [])

    def test_optional_config_scalar_and_validation(self):
        config = self.root / 'docgen.yaml'
        for scalar, expected in [('title: Test', ''), ('base_path: /project', '/project'), ('base_path: "/project" # comment', '/project'), ("base_path: ''", '')]:
            config.write_text(scalar)
            self.assertEqual(site_check.configured_base_path(config), expected)
        config.write_text('base_path: [unsupported]')
        with self.assertRaises(ValueError):
            site_check.normalize_base_path(site_check.configured_base_path(config))
        for base in ['project', '/project/../elsewhere', '/project?query', '//project', '/project%2fother', '/bad path']:
            with self.subTest(base=base), self.assertRaises(ValueError):
                self.errors(base)

    def test_generated_label_tabs(self):
        self.write(self.site, 'index.html', '<label id="rust" role="tab">Rust</label><div class="tab-panel active" data-tab-id="rust">Code</div>')
        self.assertEqual(self.errors(), [])
        self.write(self.site, 'index.html', '<label id="rust" role="tab">Rust</label>')
        self.assertIn('invalid tab control', self.errors()[0])

    def test_hash_tab_controls_require_matching_nonempty_markers(self):
        self.write(self.site, 'index.html', '<a href="#/tab/rust" data-tab="rust">Rust</a><div class="tab-panel" data-tab-id="rust">Code</div>')
        self.assertEqual(self.errors(), [])
        for markup in ['<a href="#/tab/">Empty</a>', '<a href="#/tab/missing" data-tab="missing">Missing</a>', '<a href="#/tab/rust">Unmarked</a><div class="tab-panel" data-tab-id="rust"></div>']:
            with self.subTest(markup=markup):
                self.write(self.site, 'index.html', markup)
                self.assertIn('invalid tab control', self.errors()[0])

    def test_math_errors_fail_but_code_examples_do_not(self):
        for markup in ['<div class="math">PARSE ERROR: bad formula</div>', '<math><merror><mtext>bad</mtext></merror></math>', '<div>PARSE <span>ERROR</span></div>']:
            with self.subTest(markup=markup):
                self.write(self.site, 'index.html', markup)
                self.assertTrue(any('math' in error.lower() for error in self.errors()))
        self.write(self.site, 'index.html', '<p>The formulas rendered without parse errors.</p><pre><code>PARSE ERROR <merror>example</merror></code></pre><code>PARSE ERROR</code><script>PARSE ERROR</script><style>PARSE ERROR</style>')
        self.assertEqual(self.errors(), [])

    def test_fenced_equations_preserve_spaces_symbols_and_superscripts(self):
        equation = 'L(p | q) = L(p) ∪ L(q)\nA = {x ∈ U | x < 4}\nA⁺ = A ∪ AA'
        self.write(self.docs, 'README.md', '# Home\n\n```text\n' + equation + '\n```\n')
        self.write(self.site, 'index.html', '<pre><code>' + escape(equation) + '\n</code></pre>')
        self.assertEqual(self.errors(), [])
        for broken in [equation.replace(' | ', '|'), equation.replace('∪', 'u'),
                       equation.replace('<', ''), equation.replace('⁺', '+')]:
            with self.subTest(broken=broken):
                self.write(self.site, 'index.html', '<pre><code>' + escape(broken) + '\n</code></pre>')
                self.assertTrue(any('authored code' in error for error in self.errors()))

    def test_inline_html_code_preserves_backticks_operators_and_quotes(self):
        self.write(self.docs, 'README.md', '# Home\n<code>&#96;ab&#96;&#42;</code> and <code>&quot;cat&quot;</code>\n')
        correct = '<code>`ab`*</code> and <code>&quot;cat&quot;</code>'
        self.write(self.site, 'index.html', correct)
        self.assertEqual(self.errors(), [])
        for broken in [correct.replace('*', ''), correct.replace('`', ''),
                       correct.replace('&quot;cat&quot;', '“cat”')]:
            with self.subTest(broken=broken):
                self.write(self.site, 'index.html', broken)
                self.assertTrue(any('authored code' in error for error in self.errors()))

    def test_markdown_emphasis_inside_code_fails_even_without_source_binding(self):
        self.write(self.site, 'index.html', '<code>`ab`<em></code> and <code>(`a` `b`)</em></code>')
        self.assertTrue(any('formatting inside code' in error for error in self.errors()))

    def test_highlighting_spans_preserve_code_but_dropped_duplicate_fails(self):
        self.write(self.docs, 'README.md', '# Home\n```rust\nlet x = 1;\n```\n<code>x</code> and <code>x</code>\n')
        correct = '<pre><code><span>let</span> x = <span>1</span>;\n</code></pre><code>x</code><code>x</code>'
        self.write(self.site, 'index.html', correct)
        self.assertEqual(self.errors(), [])
        self.write(self.site, 'index.html', correct.removesuffix('<code>x</code>'))
        self.assertTrue(any('authored code' in error for error in self.errors()))

    def test_html_code_in_a_fence_is_not_also_an_inline_example(self):
        self.write(self.docs, 'README.md', '# Home\n```text\n<code>example</code>\n```\n')
        self.write(self.site, 'index.html', '<pre><code>&lt;code&gt;example&lt;/code&gt;\n</code></pre>')
        self.assertEqual(self.errors(), [])

    def test_math_and_diagram_fences_are_not_literal_code_examples(self):
        self.write(self.docs, 'README.md', '# Home\n```math\nx + y\n```\n```mermaid\ngraph TD; A-->B;\n```\n')
        self.assertEqual(self.errors(), [])

    def test_command_returns_nonzero_then_passes_when_fixed(self):
        self.write(self.site, 'index.html', '<a href="missing.html">Broken</a>')
        command = [sys.executable, str(ROOT / 'scripts/check-site.py'), '--site', str(self.site), '--docs', str(self.docs), '--base-path', '/project']
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('target does not exist', result.stdout)
        self.assertIn('Failed: 1 site check errors', result.stdout)
        self.write(self.site, 'missing.html', '<h1>Now present</h1>')
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
