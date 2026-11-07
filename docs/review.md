# Review this draft

This pass connects the language-first lessons to type checking. Start at the [home page](/) and follow the next-page links. The approved direction uses strings as language-level values, equal denoted sets as equal pattern types, and inclusion as subtyping without conversion. Whole-string acceptance is fixed. Unknown membership requires an explicit check before constrained use. Static or dynamic enforcement, failure reporting, and native machinery are deferred to implementations or host integration; detailed expression rules remain open. Existing regex tools remain in an optional translation companion.

## Review each section

Use the checkpoint at the end of each section before reading its answer. For each concept, ask whether the explanation makes sense without material from a later section. If it does not, note the missing prerequisite rather than adding a second competing definition.

| Page | Sections to review |
| --- | --- |
| [Set foundations](sets.html) | Membership; equality; universe; empty set; subsets; set-builder notation |
| [Set operations](set-operations.html) | Union; intersection; difference; complement; symmetric difference; Cartesian product; power set; combined operations |
| [Strings and regexes](regex-introduction.html) | Strings and ε; pattern languages; search versus membership; character versus string sets; value constraints |
| [Our first pattern language](pattern-language.html) | Literal values as singleton patterns; vocabulary; `[]` as no possible value; whitespace; grouping and binding; full consumption; deferred variables |
| [Building patterns from sets](regex-building-blocks.html) | Literals; alternatives as union; ranges; empty set versus empty string; concatenation; repetition and empty-set zero-copy boundaries; a complete label; further set operations |
| [Cardinality and mappings](cardinality-and-mappings.html) | Distinct members; functions and images; injections, surjections, and bijections; countable infinity; diagonal listing; counts by length; concatenation collisions; power-set boundary; language-design implications |
| [Sets as types](sets-as-types.html) | Values versus expressions and denoted sets; equal sets as equal pattern types; singleton and refinement types; numeric and canonical strings; storage versus semantics; explicit check for unknown membership; enforcement-neutral semantics; semantic subtyping; deferred native machinery and failure reporting |
| [Open design questions](open-design-questions.html) | Fixed direction versus proposals; character model; type-position syntax; checking guarantees and runtime validation; subtyping; operation scope; cardinality and mappings |
| [Supplemental translations](regex-translations.html), optional | Our notation first; equivalent external patterns; whole-string adapters; external features not imported into the language |

## Site checks

For the first preview, check these behaviors:

- The sidebar follows the reading order rather than sorting pages alphabetically.
- Every concept appears as a separate heading and can be reached by a heading link.
- Short set equations use spaced Unicode text displays, not raw TeX or a dependence on MathML layout. Verify `|`, `∪`, `∩`, `∖`, `∈`, `∉`, `<`, and the superscript in `A⁺` remain visible and distinct.
- Proposed notation remains plain text, Rust examples have readable highlighting in the companion, and table patterns retain backtick delimiters, backslashes, and vertical bars. Double-quoted input values must remain distinct from patterns, including the empty value `""` and its two-backtick literal pattern.
- Previous concepts and next-page links point to the intended pages.
- Site search can find a concept such as "symmetric difference."
- The main pattern lessons use our notation without requiring engine tabs. Check the set formulas and accepted/rejected tables alongside it.
- The new type lesson follows cardinality in both the sidebar and next-page links. Its membership and inclusion tables preserve `∈`, `⊆`, `<:`, literal backticks, and the distinction between ∅ and `{""}`.
- On the supplemental page, switch the single label comparison group through our proposal, Pomsky, Rust regex, JavaScript, Python, Java, .NET (C#), and PCRE2. Our proposal should be selected initially. Check that exactly one panel is visible, the tab labels wrap within their container at narrow widths, and external snippets preserve literal quotes, backslashes, and host-language delimiters. The companion's page-local CSS enables wrapping without changing tabs elsewhere.
- Check the supplemental adapter list at narrow and desktop widths, including browser zoom. Its text and inline code should wrap within the reading column without overlapping the right-hand navigation. Long call chains belong in prose steps or locally scrollable code blocks, not table cells that force the whole table wider.
- Open the design-question links from the lessons and verify they reach the relevant question.

The initializer's [Markdown feature sample](examples.html) remains available for reference but is not part of the lesson navigation or an authority on generator behavior. Use [Docgen 0.3.3's upstream documentation](https://github.com/thecodrr/docgen/tree/0.3.3/docs) when checking features.

## Verification scope

Run `just check` and `git diff --check` from the project root to check the regression tests, production build, generated-file ignores, rendered examples, and whitespace. These checks do not establish mathematical correctness or executable regex behavior.

Our proposed notation has no executable implementation. Review its examples against the stated set-building rules. Separately check hand-authored translations with Rust `regex` **1.12.2**, default crate features and flags, and the `\A(?:pattern)\z` wrapper. Test the accepted/rejected tables, empty strings, trailing line feeds, literal operator characters, grouping, and repetition of entire literals. Passing translations is not proof of a compiler or execution of our language. Keep any test crate outside the repository.

Run the complete Rust snippet in the supplemental companion unchanged. Its search call intentionally differs from the anchored membership calls. The later label snippets are usage fragments, not standalone programs. Check the shared translation table with each available engine's stated whole-string adapter, including the label's accepted and rejected inputs. Use the companion's [verification notes](regex-translations.html#what-was-checked) to distinguish executed checks from documentation-backed Java and .NET illustrations; do not report an unavailable engine as tested. These are small translation examples, not a comprehensive compatibility or extension suite.

For the set examples, calculate results with the finite universes shown on each page, including empty-set boundary cases. These finite checks illustrate the definitions. They are not proofs about every possible set.

For the cardinality lesson, check its finite tables and mapping examples separately from its infinite-set arguments. Use the stated Rust version for membership and counts by length. Check that the diagonal-listing rule reaches every pair exactly once; testing a finite prefix alone cannot prove countability. The functions in the lesson are mathematical descriptions, not proposed language syntax or claims about which mappings Rust regex can express.

For the type lesson, check the finite membership and inclusion tables against their stated sets, and compute its union, intersection, and difference examples. Check that the alternative and range examples denote the same set, and that every proposed canonical decimal string satisfies the permissive form while leading-zero examples distinguish the sets. Treat these as deductions from our pattern rules, not execution of the notation. Read external type-system sources separately from reviewing our design choices. Verify that unknown input is not called invalid, equal cardinality is not used as subtyping, storage optimizations do not erase string distinctions, and explicit checking of unknown membership is distinguished from deferred enforcement and failure-reporting machinery. These checks do not verify a compiler, subtyping algorithm, or type-safety theorem.

For Pomsky translations, use Pomsky **0.12.0** with `--flavor rust`. Test compiled patterns with Rust `regex = "=1.12.2"` and whole-string matching. Neither tool selects an implementation for our language.

## Questions for the next review

- Do set foundations and set operations need more worked examples, or do the checkpoints suffice?
- Can a reader distinguish the pattern <code>&#96;cat&#96;</code> from the value `"cat"`, and explain <code>&#96;a+b&#96;</code> and whole-string acceptance without knowing regex syntax?
- Is it clear that `|` is preferred for choices, brackets illustrate ranges, and `[]` denotes the empty set, without defining optional nonempty bracketed shorthand?
- Can readers explain why `[]` rejects the empty string, but <code>[]&#42;</code>, `[]?`, and `[]{0}` accept it? Are `{}` and reversed ranges kept separate from the approved empty-set spelling?
- Does <code>&#96;${name}&#96;</code> clearly mean literal text rather than JavaScript-style interpolation?
- Does grouping make repeated or joined alternatives clear, and are symbolic repetition counts readable?
- Is the difference between <code>&#96;ab&#96;&#42;</code> and <code>&#96;a&#96; &#96;b&#96;&#42;</code> clear?
- Can readers complete the main path without opening the supplemental translations?
- Is the building-pattern sequence comfortable to read, or should sections become separate pages?
- Does the type lesson explain why we built the sets, and distinguish a value, a type expression, and its denoted set?
- Is "pattern-constrained string type" understandable before introducing refinement types and semantic subtyping?
- Can readers explain why checking one value differs from establishing a guarantee for all possible results of an expression?
- Is the subtyping direction clear: a smaller allowed-value set gives a stronger guarantee, not a conversion?
- Is it clear that strings are the value model, while the final character model remains open and numeric storage may be optimized?
- Can readers distinguish equal pattern sets, canonical string forms, and internal storage representations? Does the Rust alias/newtype comparison avoid confusing those ideas?
- Does the file-input example explain why an unchecked value may be valid without yet carrying the required guarantee?
- Is the explicit check requirement clear without prescribing static or dynamic enforcement, native machinery, or an error representation?
- Is optional/result representation visibly deferred and distinct from the pattern quantifier `?` and the empty string?
- Which theoretical set operation, type notation, or numeric constraint should we design next?

Design decisions belong on [open design questions](open-design-questions.html), not in this review checklist.

Return to the [reading path](/#reading-path).
