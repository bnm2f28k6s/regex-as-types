# Regex as types

A teaching project exploring regexes as a compact notation for sets, and how those sets could constrain the values allowed by a type.

We are developing the documentation for a possible programming language, not building an implementation yet. Its notation and rules are still open questions. The goal is to explain the foundations first, then work toward a design that could be implemented later without tying it to a particular language or runtime.

Rust's `regex` crate is our main reference. We will also compare JavaScript, Python, Ruby, Perl, and other regex systems where they help explain an idea or reveal a difference.

## Read and contribute

The website's pages live in `docs/`. Start with `docs/README.md`; `docs/examples.md` is a generated Markdown feature example, not a language specification.

Contributions should explain ideas in plain language, build on earlier lessons, and link to sources for technical claims. Mark new design ideas as proposals rather than settled rules. Agents should read [AGENTS.md](AGENTS.md) before working on the project.

Starting references:

- [Rust regex crate documentation](https://docs.rs/regex/latest/regex/)
- [Regular-Expressions.info tutorial](https://www.regular-expressions.info/tutorial.html) and [flavor comparison](https://www.regular-expressions.info/refflavors.html)
- [Docgen](https://github.com/thecodrr/docgen), the documentation site generator used here

We will compile more sources as the lessons develop, including references for set theory and type systems.

## Local development

Run these commands from the project root. You need [just](https://github.com/casey/just) and the project-local Docgen 0.3.3 executable. If `bin/docgen` is missing, follow the reinstall instructions below. If just isn't installed and you have Nix, use `nix shell nixpkgs#just` to enter a temporary shell with it available. Run `just` to list tasks.

```sh
just serve  # http://127.0.0.1:4001, with live reload
just build  # production output in site/
just check  # production build and Git ignore checks
```

Edit Markdown in `docs/` and site settings in `docgen.yaml`. Docgen supports [GitHub-flavored Markdown, static syntax highlighting, and tabs](https://github.com/thecodrr/docgen#features). Use tabs when comparing regex systems, and check the preview to confirm they render correctly.

The project-local executable is `bin/docgen`. The entire `bin/` directory, generated `site/`, and `.cache/` are Git-ignored. No global Docgen installation is required. Stop the development server with Ctrl-C when running it in a terminal.

## Reinstall the binary

Prerequisites: Git, Nix with flakes enabled, and macOS command-line developer tools. From the project root:

```sh
sh scripts/install-docgen.sh
```

The installer builds the upstream 0.3.3 tag at commit `b2d0cfc77110b524f5e5ab547bd8eb5b1dbd28fb` with its existing Cargo lockfile and a pinned Nix Rust toolchain. It checks the commit before building. Build sources are temporary and ignored. Cargo's normal dependency cache remains outside this project.

The initial binary was built and tested on Apple Silicon macOS. Upstream's precompiled macOS release is Intel-only and cannot run here without Rosetta. The native build links only macOS system libraries; Nix is needed for rebuilding, not serving. Other platforms have not been verified. Upstream produces compiler warnings, but the build succeeds.

Docgen serves the preview and live reload on loopback only. This repository is local; no hosting, remote, or publication is configured.
