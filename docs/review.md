# Review this draft

This pass makes the lessons language-first. Start at the [home page](/) and follow the next-page links. Whole-string acceptance is fixed; the small notation is proposed for review, without an implementation. Existing regex tools belong in an optional translation companion.

## Review each section

Use the checkpoint at the end of each section before reading its answer. For each concept, ask whether the explanation makes sense without material from a later section. If it does not, note the missing prerequisite rather than adding a second competing definition.

| Page | Sections to review |
| --- | --- |
| [Set foundations](sets.html) | Membership; equality; universe; empty set; subsets; set-builder notation |
| [Set operations](set-operations.html) | Union; intersection; difference; complement; symmetric difference; Cartesian product; power set; combined operations |
| [Strings and regexes](regex-introduction.html) | Strings and ε; pattern languages; search versus membership; character versus string sets; value constraints |
| [Our first pattern language](pattern-language.html) | Literal values as singleton patterns; proposed vocabulary; whitespace; grouping and binding; full consumption; deferred variables |
| [Building patterns from sets](regex-building-blocks.html) | Literals; alternatives as union; character ranges; empty string; concatenation; finite and unbounded repetition; a complete label; further set operations |
| [Cardinality and mappings](cardinality-and-mappings.html) | Distinct members; functions and images; injections, surjections, and bijections; countable infinity; diagonal listing; counts by length; concatenation collisions; power-set boundary; language-design implications |
| [Open design questions](open-design-questions.html) | Fixed direction versus proposals; character model; type relationship; operation scope; notation; cardinality and mappings |
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
- On the supplemental page, switch the label example between our proposal, Pomsky, and Rust regex. The proposed form should be the initial panel.
- Open the design-question links from the lessons and verify they reach the relevant question.

The initializer's [Markdown feature sample](examples.html) remains available for reference but is not part of the lesson navigation or an authority on generator behavior. Use [Docgen 0.3.3's upstream documentation](https://github.com/thecodrr/docgen/tree/0.3.3/docs) when checking features.

## Verification scope

Run `just check` and `git diff --check` from the project root to check the regression tests, production build, generated-file ignores, rendered examples, and whitespace. These checks do not establish mathematical correctness or executable regex behavior.

Our proposed notation has no executable implementation. Review its examples against the stated set-building rules. Separately check hand-authored translations with Rust `regex` **1.12.2**, default crate features and flags, and the `\A(?:pattern)\z` wrapper. Test the accepted/rejected tables, empty strings, trailing line feeds, literal operator characters, grouping, and repetition of entire literals. Passing translations is not proof of a compiler or execution of our language. Keep any test crate outside the repository.

Run the complete Rust snippet in the supplemental companion unchanged. Its search call intentionally differs from the anchored membership calls.

For the set examples, calculate results with the finite universes shown on each page, including empty-set boundary cases. These finite checks illustrate the definitions. They are not proofs about every possible set.

For the cardinality lesson, check its finite tables and mapping examples separately from its infinite-set arguments. Use the stated Rust version for membership and counts by length. Check that the diagonal-listing rule reaches every pair exactly once; testing a finite prefix alone cannot prove countability. The functions in the lesson are mathematical descriptions, not proposed language syntax or claims about which mappings Rust regex can express.

For Pomsky translations, use Pomsky **0.12.0** with `--flavor rust`. Test compiled patterns with Rust `regex = "=1.12.2"` and whole-string matching. Neither tool selects an implementation for our language.

## Questions for the next review

- Do set foundations and set operations need more worked examples, or do the checkpoints suffice?
- Can a reader distinguish the pattern <code>&#96;cat&#96;</code> from the value `"cat"`, and explain <code>&#96;a+b&#96;</code> and whole-string acceptance without knowing regex syntax?
- Is it clear that `|` is preferred for choices and brackets illustrate ranges, without ruling out optional bracketed shorthand later?
- Does <code>&#96;${name}&#96;</code> clearly mean literal text rather than JavaScript-style interpolation?
- Does grouping make repeated or joined alternatives clear, and are symbolic repetition counts readable?
- Is the difference between <code>&#96;ab&#96;&#42;</code> and <code>&#96;a&#96; &#96;b&#96;&#42;</code> clear?
- Can readers complete the main path without opening the supplemental translations?
- Is the building-pattern sequence comfortable to read, or should sections become separate pages?
- Which concepts need diagrams or exercises before moving into type constraints?

Design decisions belong on [open design questions](open-design-questions.html), not in this review checklist.

Return to the [reading path](/#reading-path).
