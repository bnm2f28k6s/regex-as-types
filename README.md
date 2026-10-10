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

Run these commands from the project root. You need [just](https://github.com/casey/just) and the project-local Docgen 0.3.3 executable. If `bin/docgen` is missing, follow the reinstall instructions below. If just isn't installed and you have Nix, use `nix shell nixpkgs#just` to enter a temporary shell with it available. Run `just` to list tasks.

```sh
just serve  # http://127.0.0.1:4001, with live reload
just build  # production output in site/
just check  # production build and Git ignore checks
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

Docgen serves the preview and live reload on loopback only. This repository is local; no hosting, remote, or publication is configured.
