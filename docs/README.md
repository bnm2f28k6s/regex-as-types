# Regex as types

Can a regex describe a set of allowed values? Start with sets, then learn how Rust regex patterns describe sets of strings. Later, we can use these foundations to explore type constraints.

This is a first teaching draft, not a language specification. Each concept has its own section, examples, and a checkpoint so we can review the order and explanations separately.

## Reading path

1. [Set foundations](sets.html): membership, equality, subsets, the empty set, and describing a set with a rule.
2. [Set operations](set-operations.html): union, intersection, difference, complement, symmetric difference, products, and power sets.
3. [Strings and regexes](regex-introduction.html): strings as values, sets of strings, and whole-string matching versus search.
4. [Rust regex building blocks](regex-building-blocks.html): literals, character classes, combinations, repetition, assertions, and flags.
5. [Review this draft](review.html): a lesson checklist, verification scope, and questions for the next pass.

## Scope of this draft

The set lessons start with small finite sets. The regex lessons use Rust's `regex` crate 1.12.2, with Unicode enabled and other flags at their defaults unless stated. We use UTF-8 strings, not byte regexes. Most examples check the entire string, not whether a matching substring exists.

Rust is our reference format for now. Its [crate documentation](https://docs.rs/regex/1.12.2/regex/) describes the supported syntax and notes that look-around and backreferences are not supported. Comparisons with other engines can come later.

These assumptions organize the lessons. They do not settle the proposed language's value universe, encoding, syntax, or type rules.

Start with [set foundations](sets.html).
