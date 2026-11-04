# Regex as types

A teaching project exploring regexes as a compact notation for sets, and how those sets could constrain the values allowed by a type.

We are developing the documentation for a possible programming language, not building an implementation yet. Its notation and rules are still open questions. The goal is to explain the foundations first, then work toward a design that could be implemented later without tying it to a particular language or runtime.

Rust's `regex` crate is our main reference. We will also compare JavaScript, Python, Ruby, Perl, and other regex systems where they help explain an idea or reveal a difference. [Pomsky](https://pomsky-lang.org/) joins the comparison list as a regex language and compiler, not a matching engine. Its [compatibility guide](https://github.com/pomsky-lang/pomsky/blob/v0.12.0/README.md#compatibility-and-portability) explains target-flavor selection.

## Read and contribute

The website's pages live in `docs/`. Start with `docs/README.md`. The first draft follows sets, set operations, strings, Rust regex building blocks, and tabbed Pomsky comparisons, with one concept per section and checkpoints for review. `docs/pomsky-comparison.md` compares Pomsky, Rust regex, and our mathematical set notation without selecting language syntax. `docs/review.md` records the review scope and open questions; `docs/examples.md` is an initializer sample, not a language specification.

Contributions should explain ideas in plain language, build on earlier lessons, and link to sources for technical claims. Mark new design ideas as proposals rather than settled rules. Agents should read [AGENTS.md](AGENTS.md) before working on the project.

Starting references:

- [Rust regex crate documentation](https://docs.rs/regex/latest/regex/)
- [Pomsky language tour](https://pomsky-lang.org/docs/language-tour/strings/) and [0.12.0 release notes](https://github.com/pomsky-lang/pomsky/blob/v0.12.0/CHANGELOG.md)
- [Regular-Expressions.info tutorial](https://www.regular-expressions.info/tutorial.html) and [flavor comparison](https://www.regular-expressions.info/refflavors.html)
- [Docgen](https://github.com/thecodrr/docgen), the documentation site generator used here

The set lessons also use Oscar Levin's [Discrete Mathematics: An Open Introduction, section 0.3](https://discrete.openmathbooks.org/dmoi3/sec_intro-sets.html). Type-system sources can be added when those lessons develop.

## Local development

Run these commands from the project root. You need Python 3.9 or newer, [just](https://github.com/casey/just), and the project-local Docgen 0.3.3 executable. If `bin/docgen` is missing, follow the reinstall instructions below. If just isn't installed and you have Nix, use `nix shell nixpkgs#just` to enter a temporary shell with it available. Run `just` to list tasks.

```sh
just serve  # http://127.0.0.1:4001/regex-as-types/, with live reload
just build  # production output in site/
just test   # checker regression tests and installer shell syntax
just check  # tests, production build, rendered-site, ignore, and whitespace checks
```

Edit Markdown in `docs/` and site settings in `docgen.yaml`. Docgen supports [GitHub-flavored Markdown, static syntax highlighting, and tabs](https://github.com/thecodrr/docgen#features). Use tabs when comparing regex systems, and check the preview to confirm they render correctly.

For [tabs in Docgen 0.3.3](https://github.com/thecodrr/docgen/blob/0.3.3/docs/features/tabs.md), use headings such as `# [Pomsky](#/tab/pomsky)` and end each group with a horizontal rule. Reusing tab IDs synchronizes the selection across the page. The comparison page uses plain-text fences for Pomsky because this binary has no Pomsky highlighter; do not label it as another language merely to add color.

Use relative `.html` links between site pages and `/` for the home page. The installed 0.3.3 generator leaves relative `.md` links unchanged in production HTML, as its [link-rewriter source](https://github.com/thecodrr/docgen/blob/0.3.3/src/markdown/extensions/link_rewriter.rs) also shows. Check the built output, not just the development server. In regex table cells containing `|`, use inline HTML such as `<code>cat&#124;dog</code>`; this version renders a backslash literally when using a Markdown-escaped pipe inside backticks.

The project-local executable is `bin/docgen`. The entire `bin/` directory, generated `site/`, and `.cache/` are Git-ignored. No global Docgen installation is required. Stop the development server with Ctrl-C when running it in a terminal.

## Reinstall the binary

Prerequisites: Git, Nix with flakes enabled, and macOS command-line developer tools. From the project root:

```sh
sh scripts/install-docgen.sh
```

The installer builds the upstream 0.3.3 tag at commit `b2d0cfc77110b524f5e5ab547bd8eb5b1dbd28fb` with its existing Cargo lockfile and a pinned Nix Rust toolchain. It checks the commit before building. Build sources are temporary and ignored. Cargo's normal dependency cache remains outside this project.

The initial binary was built and tested on Apple Silicon macOS. Upstream's precompiled macOS release is Intel-only and cannot run here without Rosetta. The native build links only macOS system libraries; Nix is needed for rebuilding, not serving. Other platforms have not been verified. Upstream produces compiler warnings, but the build succeeds.

Docgen serves the preview and live reload on loopback only.

## Checks and GitHub Pages

The [GitHub Actions workflow](.github/workflows/pages.yml) runs on pull requests and pushes to `main`. It checks installer shell syntax, runs the checker's regression tests, builds with Docgen 0.3.3, checks the rendered site, and checks Git ignores and whitespace. GitHub actions are commit-pinned. The Linux release archive has a recorded SHA-256 digest, which detects archive changes but is not an independently signed upstream verification.

The offline [rendered-site checker](scripts/check-site.py) is adapted from the prisoner's dilemma project. It checks authored-page coverage, local page links, HTML/SVG fragments, directly referenced assets, and the configured project prefix. It resolves Docgen's extensionless sidebar URLs to `.html`, matching GitHub Pages; a different host needs the same routing. It also checks Docgen's tab markup and math-rendering error markers. Its regression tests include deliberately broken fixtures and a nonzero CLI exit, so accepting every input cannot pass the suite.

The checker uses Python's standard library and makes no network requests. External links, CSS-internal resources, JavaScript-generated links, interactive tab behavior, accessibility, and the mathematical or regex correctness of lesson examples need separate review. A passing site check is not proof of the lesson content.

For an existing production build, run `python3 scripts/check-site.py`. Isolated checks can use `--site PATH --docs PATH --base-path /PROJECT`; otherwise the prefix comes from `docgen.yaml`. A missing or empty build fails rather than silently skipping checks.

The workflow uploads and deploys `site/` only after a successful build on `main`. Pull requests have read-only permissions and skip both upload and deployment. A passing PR does not merge itself or publish a preview. In GitHub Settings > Pages, select GitHub Actions as the publishing source. The site will be at <https://bnm2f28k6s.github.io/regex-as-types/> after this workflow is merged and a deployment succeeds.

The [`base_path` setting](https://github.com/thecodrr/docgen/blob/0.3.3/docs/configuration.md#base_path) is `/regex-as-types/`. The installed binary requires the trailing slash. Keep authored root links such as `/` free of that prefix; Docgen adds it during rendering. Relative `.html` page links stay relative. The Pages marker in `docs/_include/.nojekyll` is copied to the site using [Docgen's static-asset mechanism](https://github.com/thecodrr/docgen/blob/0.3.3/docs/deployment.md#disable-jekyll-builds).

A project-wide reuse license has not been selected. Public visibility alone does not grant an open-source or open-content license. Docgen retains its separate upstream license; its binary and source are not committed here.
