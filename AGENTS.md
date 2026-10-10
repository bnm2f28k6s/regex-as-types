# Agent guide

## Purpose and scope

This repository is a documentation site and teaching tool. It explores regexes as a compact notation for sets, then uses set theory to investigate constraints on types in a possible programming language.

The language's format and semantics are not defined yet. Keep the design abstract and independent of any implementation. Do not add a compiler, interpreter, runtime, or implementation dependencies unless asked. Rust's `regex` crate is the primary reference for regex behavior, not a requirement to implement the proposed language in Rust. Compare JavaScript, Python, Ruby, Perl, and other systems when useful.

## Read before editing

- Read `README.md`, the relevant pages in `docs/`, and `justfile`.
- Check Git status and preserve unrelated work.
- Website content belongs in `docs/`; site settings belong in `docgen.yaml`.
- The root README is the short guide for people using or contributing to the project. This file contains agent working rules.
- `docs/examples.md` is initializer sample content. It is not a specification or an authoritative description of the installed generator. Verify its examples against Docgen before copying them.

## Evidence and citations

- Do not write technical claims from memory alone. Read a relevant source first and cite it near the claim with a descriptive Markdown link, preferably to the exact section.
- Prefer primary documentation or specifications for engine behavior. Start with the [Rust regex crate documentation](https://docs.rs/regex/latest/regex/), the [Regular-Expressions.info tutorial](https://www.regular-expressions.info/tutorial.html), and its [flavor comparison](https://www.regular-expressions.info/refflavors.html). Add appropriate mathematical and type-system sources as those topics arise.
- For JavaScript, Python, Ruby, Perl, or another system, consult that system's documentation before asserting its behavior. Do not assume a pattern has the same meaning across engines.
- Record the engine, relevant version, flags, and matching mode when they affect a claim or example. Prefer version-specific references for version-dependent behavior.
- Separate sourced facts, deductions, and original design proposals. Cite the premises of a deduction and explain the reasoning. Label a new rule or notation as a proposal or open question; do not pretend an external source defines our language.
- If evidence is missing or conflicting, state the uncertainty or leave the claim out. Never invent a source, quotation, test result, or language rule.
- Summarize sources in your own words. Attribute short quotations and do not copy substantial external material without checking its license.

## Teaching and design standards

- Write for a reader learning regexes, not only for specialists. Use plain language, introduce terms before using them, and use precise technical terminology when needed.
- Build from foundations: sets and membership, strings and matching, basic regex operations, then type constraints. Explain prerequisites before relying on them.
- Use small examples with an explanation, accepted values, rejected values, and boundary cases where relevant. Distinguish verified executable examples from illustrative proposed syntax.
- Keep mathematical regular expressions and engine-specific regex features distinct. Source claims about their expressive power rather than assuming every feature describes a regular language.
- Before drawing conclusions about sets or types, make the relevant assumptions explicit: the universe of values, strings versus other values, character encoding, whole-string matching versus substring search, and flags. Do not silently decide these open design questions.
- Distinguish sets of characters from sets of strings, and proposed type operations from engine syntax. Explain the interpretation before presenting equations or notation.
- Show engine differences as comparisons, not as a competition or a claim of universal compatibility. Rust is the main reference, not the only perspective.
- Keep tentative choices visibly tentative. Once a design choice is approved, explain its rationale and update affected pages consistently.

## Markdown and site conventions

The site uses project-local [Docgen](https://github.com/thecodrr/docgen) 0.3.3, a fork of Doctave. Its upstream README documents GitHub-flavored Markdown, tabs, and static code-block highlighting.

- Use descriptive headings, relative links between site pages, and labeled fenced code blocks with supported language identifiers.
- Use tabs for side-by-side language or engine comparisons when helpful. Verify the actual Docgen tab syntax in upstream documentation or source; do not guess it or assume every Doctave feature is compatible.
- Preview new Markdown features, mathematical notation, tabs, and highlighting with the installed binary. A language label is a rendering hint, not evidence that the example runs.
- Keep navigation and cross-references coherent. Do not add custom scripts, plugins, dependencies, or unrelated site styling for a documentation change.

## Checks and handoff

Run commands from the project root:

```sh
just             # list tasks
just serve       # preview at http://127.0.0.1:4001; stop with Ctrl-C
just build       # production site in site/
just check       # production build and generated-file ignore checks
```

If `just` is unavailable and Nix is installed, use `nix shell nixpkgs#just`. If `bin/docgen` is missing, follow the README's pinned installer instructions rather than installing a different generator globally.

- Run `just check` and `git diff --check` after changes. The build does not prove that cited claims or regex examples are correct, and the ignore check is not a general documentation linter.
- Review changed links, citations, and consistency with existing lessons. Preview rendered site changes, especially tabs, formulas, and code blocks.
- When asserting executable behavior, run the example in the stated engine when available and report what was tested. If it cannot be run, say so; do not substitute another engine or describe it as verified.
- Keep `bin/`, `site/`, and `.cache/` untracked. Never include credentials or machine-local files.
- Report changed files, checks actually run, and unresolved questions. Do not commit, push, or publish unless asked.
