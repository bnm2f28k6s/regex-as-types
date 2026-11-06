# Open design questions

This page separates the language's fixed direction from proposed notation and unresolved choices. The lessons use explicit assumptions where the design is still open.

## Fixed direction and first-draft scope

- Teach sets and strings first, then develop our own language rather than teach an existing engine as the language.
- A pattern tests the complete input from start to end. Substring search is not the constraint model, and authors do not add anchors to opt into full consumption.
- Begin with literal string values as singleton-set patterns and operations that combine their parts. The [pattern-language page](pattern-language.html) proposes concrete notation for review.
- Prefer backticks for pattern literals and keep double quotes for example string values. The first draft has no interpolation; backticks do not import JavaScript's template semantics.
- Prefer `|` for explicit choices of any length and show bracket-delimited character ranges in the core lessons. Optional bracketed choice shorthand remains an open design possibility, not a banned feature. Keep it out of the main teaching path until its form and semantics are specified.
- Keep the first draft small and focused on strings. Variables and named fragments are deferred, not required for these examples.
- Use existing regex tools only as supplemental translations and checks. No engine, compiler target, or syntax compatibility is required.

These points record the current project direction and preferred teaching notation, not a complete grammar. Literal escaping, possible shorthand, broader range semantics, and other unresolved details remain below.

## What values do constraints describe?

1. What is the universe of values: strings only, or other values as well?
2. If strings are included, what is the character model and encoding?
3. Should future constraints include non-string values, and how would their literal forms denote allowed sets?
4. Which universe defines complement, and which set operations apply to character sets versus string sets?
5. How does inclusion between allowed-value sets relate to subtyping?

The lessons currently use finite Unicode scalar-value strings. The final character model and representation remain open; UTF-8 is used in the external Rust checks, not required by our notation. Whole-string acceptance is already fixed. See [strings and regexes](regex-introduction.html).

## What notation expresses the operations?

1. With backticks as the preferred delimiter, how should a literal backtick, backslash, or control character be represented? Should multiline literals or other quote forms also be supported? Do not assume JavaScript's escape rules or interpolation.
2. Is the proposed notation for joining, character ranges, alternatives, grouping, and repetition clear enough? Should we retain symbolic quantifiers or use words? The lessons prefer `|` for choices and brackets for ranges; full consumption is inherent.
3. If named fragments are added later, what would they denote: a character set, string set, type, or another construct? They are outside the first draft.
4. Which operations are available for character sets and for arbitrary string sets?
5. How are bounded repetition and numeric ranges represented? How do signs, leading zeroes, and digit repertoires affect textual ranges?
6. Should example strings or executable tests live beside a constraint?
7. Should optional bracketed choice shorthand be supported alongside the preferred alternatives? If so, how would it list characters, combine ranges, or treat whitespace and multi-character literals? Its syntax and semantics are open, not inherited from another regex system.
8. How should we spell the empty set and Unicode properties, and define ranges beyond the ASCII examples? An empty bracket form, if any, would also need an explicit meaning distinct from the empty string.

The [first pattern language](pattern-language.html) and [building-pattern lesson](regex-building-blocks.html) use our proposed notation as the primary form. The [translation companion](regex-translations.html) shows external equivalents separately. Similarity to Pomsky does not adopt its full grammar or feature set.

## How should cardinality and mappings affect the language?

1. Should constraints expose cardinality, counts by string length, or counts within a length bound? Which questions should be answerable automatically?
2. How should the language distinguish set equality, inclusion, and equal cardinality? What role, if any, should each play in type relationships?
3. How are mappings between constrained value sets described? Must a mapping produce an output for every allowed input, or can it fail?
4. Should mappings declare or establish that they are injective, surjective, or bijective? How should a conversion that loses distinctions be distinguished from a reversible encoding?
5. If a bijection exists, must a programmer still supply an explicit mapping? Which properties beyond membership, such as length or internal structure, must it preserve?

The [cardinality lesson](cardinality-and-mappings.html) shows that <code>L(&#96;a&#96;+)</code> and <code>L(&#96;a&#96;+ &#96;b&#96;+)</code> have equal cardinality without equal membership or equal counts by length. These mathematical facts do not decide subtyping, implicit conversion, or which functions the language can express.

## What role do existing regex systems play?

Their supplemental role is settled. Remaining questions are about which comparisons are useful, not which system defines the language:

1. Which additional translations would answer a concrete design question?
2. Which examples can be translated faithfully, and what assumptions must each adapter preserve?
3. Which engine-specific features, if any, are worth discussing later rather than leaving outside the teaching path?

The optional companion uses Rust regex 1.12.2 and Pomsky 0.12.0 targeting Rust. These versions bound external checks only. They do not choose our syntax, character model, or implementation.

Return to the [reading path](/#reading-path) or [review this draft](review.html).
