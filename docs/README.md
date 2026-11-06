# Regex as types

Can a pattern describe a set of allowed values? Start with sets and strings, then develop our own small pattern language. A literal value is the simplest pattern; operations on its parts let us describe more values. Later, we can use these foundations to explore type constraints.

This is a teaching draft with proposed notation, not an implemented language. Whole-string acceptance is fixed: every pattern must accept the input from beginning to end. The exact notation is open for review. Each concept has examples and a checkpoint.

## Reading path

1. [Set foundations](sets.html): membership, equality, subsets, the empty set, and describing a set with a rule.
2. [Set operations](set-operations.html): union, intersection, difference, complement, symmetric difference, products, and power sets.
3. [Strings and regexes](regex-introduction.html): strings as values, sets of strings, and whole-string matching versus search.
4. [Our first pattern language](pattern-language.html): quoted literals, a small proposed vocabulary, and fully consuming acceptance without anchors.
5. [Building patterns from sets](regex-building-blocks.html): use our notation for single choices, empty strings, joining, union, and repetition.
6. [Cardinality and mappings](cardinality-and-mappings.html): distinct members, functions and bijections, countable infinity, and why `"a"+` and `"a"+ "b"+` have equal cardinality but different counts by length.
7. [Open design questions](open-design-questions.html): fixed direction, proposed notation, and unresolved decisions about values, operations, and types.
8. [Review this draft](review.html): a lesson checklist, verification scope, and questions for the next pass.

Optional: [supplemental regex translations](regex-translations.html) show how selected patterns can be expressed using existing tools. They are not prerequisites for the main path.

## Scope of this draft

The set lessons start with small finite sets. String examples use finite sequences of Unicode scalar values as an explicit teaching universe; the proposed language's final character model, encoding, and type rules remain [open design questions](open-design-questions.html). The first draft concerns string constraints, without variables or named fragments.

The core examples use our proposed language. Pomsky supplies inspiration for readable literal-and-operation notation; Rust and Pomsky appear in the optional translation companion. Neither defines our rules, and no implementation target has been chosen. Checks of external translations are separate from the proposed language, which has no executable implementation here.

Start with [set foundations](sets.html).
