# Open design questions

This page separates the language's fixed direction from proposed notation and unresolved choices. The lessons use explicit assumptions where the design is still open.

## Fixed direction and first-draft scope

- Teach sets and strings first, then develop our own language rather than teach an existing engine as the language.
- A pattern tests the complete input from start to end. Substring search is not the constraint model, and authors do not add anchors to opt into full consumption.
- Begin with literal string values as singleton-set patterns and operations that combine their parts. The [pattern-language page](pattern-language.html) proposes concrete notation for review.
- Develop those set descriptions into a type-level language for allowed values. The purpose is to connect membership and constraints to type checking, not merely to provide a different regex spelling.
- Use strings as the language-level value model, including numeric values described by digit alphabets and structural constraints. Implementations may optimize internal storage, but must preserve the allowed strings and their observable distinctions. Strings are not merely the first of several unrelated value kinds in this model.
- A pattern type denotes its accepted set. Equal denoted sets mean equal pattern types, even when the expressions use different spellings.
- Define subtyping of pattern types by set inclusion. A narrower guarantee satisfies a broader requirement without conversion or an additional membership check for that requirement.
- Require an explicit check before constrained use when membership is unknown and no prior guarantee establishes it. The core does not prescribe static, dynamic, or mixed enforcement. Failure reporting and native or host checking machinery are deferred implementation/integration concerns, not prerequisites for the theoretical model.
- Prefer backticks for pattern literals and keep double quotes for example string values. The first draft has no interpolation; backticks do not import JavaScript's template semantics.
- Keep adjacency as the current concatenation notation. Whitespace separates parts rather than contributing input characters. If an explicit concatenation operator is added later, `~` is the preferred candidate because it is convenient to reach alongside backticks on the author's keyboard. This preference does not add `~` to the current grammar.
- Prefer `|` for explicit choices of any length and show bracket-delimited character ranges in the core lessons. Optional bracketed choice shorthand remains an open design possibility, not a banned feature. Keep it out of the main teaching path until its form and semantics are specified.
- Use `[]` for the empty set and empty pattern type. It accepts no string, including the empty string. The empty literal remains <code>&#96;&#96;</code>. Empty curly braces `{}` have no assigned pattern meaning; braces continue to express repetition counts. The `[]` decision does not define general nonempty bracketed choice shorthand or reversed-range behavior.
- Keep the first draft small and focused on strings. Variables and named fragments are deferred, not required for these examples.
- Use existing regex tools only as supplemental translations and checks. No engine, compiler target, or syntax compatibility is required.

These points record approved semantic direction and preferred teaching notation, not a complete grammar or checker. Literal escaping, possible shorthand, broader range semantics, and other unresolved details remain below.

## What values do constraints describe?

The all-strings value model is settled for the current design. Numeric types describe structured strings; optimized numeric storage is an implementation choice, not a separate language-level value kind. See [numeric structure and canonical strings](sets-as-types.html#numeric-structure-and-canonical-strings).

1. What is the final character model and encoding? How should constraints define an alphabet or character repertoire beyond the current ASCII range examples?
2. Which operations apply to one-character sets and which to arbitrary string sets? Complement must use a specified string universe.
3. Which numeric string sets should be provided, and what are their canonical forms? The lesson's unsigned ASCII example is illustrative, not a final signed-integer definition. Signs, zero, leading zeroes, and other digit repertoires need explicit rules.
4. Which normalization or arithmetic operations should exist, and how are their input and output string sets specified? Membership checking itself does not rewrite a string.
5. How can internal storage optimizations preserve allowed values, leading-zero distinctions, and unbounded sets without silently introducing machine-range restrictions?

The lessons currently use finite Unicode scalar-value strings. The final character model and representation remain open; UTF-8 is used in the external Rust checks, not required by our notation. Whole-string acceptance is already fixed. See [strings and regexes](regex-introduction.html).

## How do type expressions support checking?

The [sets-as-types lesson](sets-as-types.html) records the approved set-theoretic interpretation: a pattern in a type position denotes `L(p)`, satisfaction is membership, equal denoted sets give equal pattern types, and inclusion defines subtyping. Unknown membership requires an explicit check before constrained use. These choices specify meaning and the required guarantee, not an enforcement strategy or checking algorithm.

1. How does a surrounding program mark a type position and use a pattern there? Can we reuse the notation directly without adding an unnecessary wrapper? Variables and named fragments remain deferred.
2. Which theoretical rules describe the allowed sets of literals and compound expressions, and how do those sets compose?
3. How should the established inclusion rule interact with future mutation or additional program constructs? Variables and named fragments remain deferred; equal-set pattern types are already interchangeable.
4. How are function input and output constraints described if function notation is introduced? No execution or termination model is required by the present set language.

The type-level purpose, string-value model, equal-set type equality, inclusion criterion, and explicit check for unknown membership are fixed direction. Detailed notation and theoretical composition rules remain open. The [external-input example](sets-as-types.html#checking-without-choosing-static-or-dynamic-enforcement) illustrates the check requirement without choosing an execution mechanism. The existing [pattern operations](pattern-language.html#add-parts-to-describe-more-values) do not silently add declarations, control flow, arbitrary predicates, or a compiler.

## Deferred implementation and host integration

These are recorded for possible future integration, not questions that must be answered before continuing the theoretical language. Static versus dynamic enforcement is deliberately left to implementations or hosts; failure must not turn an unaccepted value into an accepted one.

1. Which membership, inclusion, equality, and emptiness questions should an implementation check automatically? How should it handle a guarantee it cannot establish?
2. What native or host machinery executes an explicit check, brings external values into the system, and carries a successful membership guarantee?
3. How should a failed check be surfaced? A diagnostic, exception, optional value, or result-like representation may be considered, but no mechanism or value encoding is selected.
4. If optional or result-like forms are explored, how should they represent success, absence, and failure consistently with the string-value model? The existing pattern quantifier `?` is zero-or-one repetition, not an already-defined optional-value or error mechanism. The empty string is not implicitly absence.

No native primitive, runtime dependency, optional type, result type, or error-handling syntax is introduced by this deferral.

## What notation expresses the operations?

1. With backticks as the preferred delimiter, how should a literal backtick, backslash, or control character be represented? Should multiline literals or other quote forms also be supported? Do not assume JavaScript's escape rules or interpolation.
2. Is the notation for character ranges, alternatives, grouping, and repetition clear enough? Should we retain symbolic quantifiers or use words? Adjacency is accepted for concatenation now. Is an additional explicit operator useful later? If so, `~` is the preferred candidate, not yet supported syntax. The lessons prefer `|` for choices and brackets for ranges; full consumption is inherent.
3. If named fragments are added later, what would they denote: a character set, string set, type, or another construct? They are outside the first draft.
4. Which operations are available for character sets and for arbitrary string sets?
5. How are bounded repetition and numeric ranges represented? How do signs, leading zeroes, and digit repertoires affect textual ranges?
6. Should example strings or executable tests live beside a constraint?
7. Should optional bracketed choice shorthand be supported alongside the preferred alternatives? If so, how would it list characters, combine ranges, or treat whitespace and multi-character literals? Its syntax and semantics are open, not inherited from another regex system.
8. How should we spell Unicode properties and define ranges beyond the ASCII examples? Should reversed character-range endpoints be rejected as invalid notation? The empty-set spelling is settled as `[]`, so an impossible range is not needed to express it. Repetition counts already require nonnegative numbers and ordered bounds; character-range policy remains separate.

The [first pattern language](pattern-language.html) and [building-pattern lesson](regex-building-blocks.html) use our proposed notation as the primary form. The [translation companion](regex-translations.html) shows external equivalents separately. Similarity to Pomsky does not adopt its full grammar or feature set.

## How should cardinality and mappings affect the language?

1. Should constraints expose cardinality, counts by string length, or counts within a length bound? Which questions should be answerable automatically?
2. How should tools present set equality, inclusion, and equal cardinality distinctly? Equal denoted sets define equal pattern types, and inclusion defines subtyping. Equal cardinality alone establishes neither.
3. How are mappings between constrained value sets described? Must a mapping produce an output for every allowed input, or can it fail?
4. Should mappings declare or establish that they are injective, surjective, or bijective? How should a conversion that loses distinctions be distinguished from a reversible encoding?
5. If a bijection exists, must a programmer still supply an explicit mapping? Which properties beyond membership, such as length or internal structure, must it preserve?

The [cardinality lesson](cardinality-and-mappings.html) shows that <code>L(&#96;a&#96;+)</code> and <code>L(&#96;a&#96;+ &#96;b&#96;+)</code> have equal cardinality without equal membership or equal counts by length. These mathematical facts do not decide subtyping, implicit conversion, or which functions the language can express.

## What role do existing regex systems play?

Their supplemental role is settled. Remaining questions are about which comparisons are useful, not which system defines the language:

1. Which additional examples would help readers recognize our notation in a familiar programming language or regex engine?
2. Which examples can be translated faithfully, and what assumptions must each adapter preserve?
3. Which engine-specific features, if any, are worth discussing later rather than leaving outside the teaching path?

The optional companion includes Rust regex 1.12.2 and Pomsky 0.12.0 targeting Rust, alongside JavaScript, Python, Java, .NET (C#), and PCRE2 illustrations. Its [adapters and verification notes](regex-translations.html#preserving-whole-string-acceptance) state the assumptions and distinguish locally tested examples from documentation-backed illustrations. These comparisons do not choose our syntax, character model, or implementation, and need not catalog each engine's extensions.

Return to the [reading path](/#reading-path) or [review this draft](review.html).
