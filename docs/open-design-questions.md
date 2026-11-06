# Open design questions

This page separates the language's fixed direction from proposed notation and unresolved choices. The lessons use explicit assumptions where the design is still open.

## Fixed direction and first-draft scope

- Teach sets and strings first, then develop our own language rather than teach an existing engine as the language.
- A pattern tests the complete input from start to end. Substring search is not the constraint model, and authors do not add anchors to opt into full consumption.
- Begin with literal string values as singleton-set patterns and operations that combine their parts. The [pattern-language page](pattern-language.html) proposes concrete notation for review.
- Keep the first draft small and focused on strings. Variables and named fragments are deferred, not required for these examples.
- Use existing regex tools only as supplemental translations and checks. No engine, compiler target, or syntax compatibility is required.

These points record the current project direction. The exact symbols proposed for literals, character choices, joining, grouping, alternatives, and repetition are not yet a finalized grammar.

## What values do constraints describe?

1. What is the universe of values: strings only, or other values as well?
2. If strings are included, what is the character model and encoding?
3. Should future constraints include non-string values, and how would their literal forms denote allowed sets?
4. Which universe defines complement, and which set operations apply to character sets versus string sets?
5. How does inclusion between allowed-value sets relate to subtyping?

The lessons currently use finite Unicode scalar-value strings. The final character model and representation remain open; UTF-8 is used in the external Rust checks, not required by our notation. Whole-string acceptance is already fixed. See [strings and regexes](regex-introduction.html).

## What notation expresses the operations?

1. Should we adopt the proposed double-quoted literals? How are quotes, backslashes, and control characters escaped? Are other quote forms useful?
2. Is the proposed notation for joining, character choices, alternatives, grouping, and repetition clear enough? Should we retain symbolic quantifiers or use words? Full consumption is inherent, not an open anchor choice.
3. If named fragments are added later, what would they denote: a character set, string set, type, or another construct? They are outside the first draft.
4. Which operations are available for character sets and for arbitrary string sets?
5. How are bounded repetition and numeric ranges represented? How do signs, leading zeroes, and digit repertoires affect textual ranges?
6. Should example strings or executable tests live beside a constraint?
7. How should we spell the empty set, empty character choices, Unicode properties, and any broader character ranges? None has a proposed spelling in this first draft.

The [first pattern language](pattern-language.html) and [building-pattern lesson](regex-building-blocks.html) use our proposed notation as the primary form. The [translation companion](regex-translations.html) shows external equivalents separately. Similarity to Pomsky does not adopt its full grammar or feature set.

## How should cardinality and mappings affect the language?

1. Should constraints expose cardinality, counts by string length, or counts within a length bound? Which questions should be answerable automatically?
2. How should the language distinguish set equality, inclusion, and equal cardinality? What role, if any, should each play in type relationships?
3. How are mappings between constrained value sets described? Must a mapping produce an output for every allowed input, or can it fail?
4. Should mappings declare or establish that they are injective, surjective, or bijective? How should a conversion that loses distinctions be distinguished from a reversible encoding?
5. If a bijection exists, must a programmer still supply an explicit mapping? Which properties beyond membership, such as length or internal structure, must it preserve?

The [cardinality lesson](cardinality-and-mappings.html) shows that `L("a"+)` and `L("a"+ "b"+)` have equal cardinality without equal membership or equal counts by length. These mathematical facts do not decide subtyping, implicit conversion, or which functions the language can express.

## What role do existing regex systems play?

Their supplemental role is settled. Remaining questions are about which comparisons are useful, not which system defines the language:

1. Which additional translations would answer a concrete design question?
2. Which examples can be translated faithfully, and what assumptions must each adapter preserve?
3. Which engine-specific features, if any, are worth discussing later rather than leaving outside the teaching path?

The optional companion uses Rust regex 1.12.2 and Pomsky 0.12.0 targeting Rust. These versions bound external checks only. They do not choose our syntax, character model, or implementation.

Return to the [reading path](/#reading-path) or [review this draft](review.html).
