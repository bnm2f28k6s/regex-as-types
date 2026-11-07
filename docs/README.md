# Regex as types

Can a pattern describe a type's allowed values? Start with sets and strings, then develop our own small pattern language. A literal value is the simplest pattern; operations on its parts let us describe more values. We use that notation as a type-level language: membership checks a value, equal denoted sets give equal pattern types, and inclusion defines subtyping. The [sets-as-types lesson](sets-as-types.html) explains these approved rules, requires explicit checking of unknown membership, and leaves static or dynamic enforcement and failure reporting to implementations or host integration.

This is a teaching draft with proposed notation, not an implemented language. Whole-string acceptance is fixed: every pattern must accept the input from beginning to end. The exact notation is open for review. Each concept has examples and a checkpoint.

## Reading path

1. [Set foundations](sets.html): membership, equality, subsets, the empty set, and describing a set with a rule.
2. [Set operations](set-operations.html): union, intersection, difference, complement, symmetric difference, products, and power sets.
3. [Strings and regexes](regex-introduction.html): strings as values, sets of strings, and whole-string matching versus search.
4. [Our first pattern language](pattern-language.html): backtick-delimited literals, a small proposed vocabulary, and fully consuming acceptance without anchors.
5. [Building patterns from sets](regex-building-blocks.html): literals, alternatives, character ranges, `[]` as the empty set, empty strings, joining, and repetition including zero-copy boundaries.
6. [Cardinality and mappings](cardinality-and-mappings.html): distinct members, functions and bijections, countable infinity, and why <code>&#96;a&#96;+</code> and <code>&#96;a&#96;+ &#96;b&#96;+</code> have equal cardinality but different counts by length.
7. [Sets as types](sets-as-types.html): type-level expressions, equal-set type equality, numeric and canonical string forms, membership versus static checking, and semantic subtyping by inclusion.
8. [Open design questions](open-design-questions.html): fixed direction, proposed notation, and unresolved decisions about values, operations, and types.
9. [Review this draft](review.html): a lesson checklist, verification scope, and questions for the next pass.

Optional: [supplemental regex translations](regex-translations.html) show how selected patterns can be expressed using existing tools. They are not prerequisites for the main path.

## Scope of this draft

The set lessons start with small finite sets. The language-level value model is strings, including numeric values described by digit alphabets and structural constraints. Implementations may optimize internal storage without changing the allowed strings or their meaning. We use finite Unicode scalar-value strings as a teaching universe; the final character model, encoding, and detailed expression typing rules remain [open design questions](open-design-questions.html). Variables and named fragments remain deferred. The first compatibility examples use unchanged, immutable values, not implicit normalization.

The core examples use our proposed language. Pomsky supplies inspiration for readable literal-and-operation notation; the optional translation companion shows Rust `regex`, Pomsky, JavaScript, Python, Java, .NET (C#), and PCRE2. These comparisons illustrate how our examples look in familiar tools, not an engine-feature survey. None defines our rules, and no implementation target has been chosen. Checks of external translations are separate from the proposed language, which has no executable implementation here.

Start with [set foundations](sets.html).
