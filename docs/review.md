# Review this draft

This pass tests the reading order and the site's rendering. It does not finalize the language design. Start at the [home page](/) and follow the next-page links.

## Review each section

Use the checkpoint at the end of each section before reading its answer. For each concept, ask whether the explanation makes sense without material from a later section. If it does not, note the missing prerequisite rather than adding a second competing definition.

| Page | Sections to review |
| --- | --- |
| [Set foundations](sets.html) | Membership; equality; universe; empty set; subsets; set-builder notation |
| [Set operations](set-operations.html) | Union; intersection; difference; complement; symmetric difference; Cartesian product; power set; combined operations |
| [Strings and regexes](regex-introduction.html) | Strings and ε; pattern languages; search versus membership; character versus string sets; possible type constraints |
| [Rust regex building blocks](regex-building-blocks.html) | Literals; escaping; classes and ranges; negated classes; wildcard; concatenation; alternation; grouping; repetition; Unicode classes; class set operations; assertions; flags; greediness; captures; combined example |

## Site checks

For the first preview, check these behaviors:

- The sidebar follows the reading order rather than sorting pages alphabetically.
- Every concept appears as a separate heading and can be reached by a heading link.
- Set formulas are typeset, not shown as raw TeX.
- Rust examples have readable highlighting, and table patterns retain their backslashes and vertical bars.
- Previous concepts and next-page links point to the intended pages.
- Site search can find a concept such as "symmetric difference."

The initializer's [Markdown feature sample](examples.html) remains available for reference but is not part of the lesson navigation or an authority on generator behavior. Use [Docgen 0.3.3's upstream documentation](https://github.com/thecodrr/docgen/tree/0.3.3/docs) when checking features.

## Verification scope

Run `just check` and `git diff --check` from the project root to check the production build, generated-file ignores, and whitespace. These checks do not establish mathematical correctness or executable regex behavior.

Regex table examples should be checked with Rust `regex` **1.12.2**, default crate features, and the `\A(?:pattern)\z` wrapper. Run the complete Rust snippets separately as written. Greedy/lazy examples intentionally use substring search. Keep any test crate outside the repository; it is a documentation check, not an implementation of the proposed language.

For the set examples, calculate results with the finite universes shown on each page, including empty-set boundary cases. These finite checks illustrate the definitions. They are not proofs about every possible set.

## First-pass results

The initial local checks passed:

- 42 Rust tests, covering 38 pattern-table rows with 193 accepted/rejected inputs, all three complete Rust snippets, and additional contextual checks. The test crate used `regex = "=1.12.2"`; a locked rerun also passed.
- 28 finite set and string checks, including empty-set cases, products, power sets, and concatenation.
- The production build and Git ignore checks, plus `git diff --check`.
- All six reading-path pages served successfully. An HTML audit checked 35 lesson headings and checkpoints, 110 internal links and heading targets, navigation order, MathML, Rust highlighting, table escaping, and search-index coverage.
- Five external source pages and the cited section fragments were checked. The live preview also returned results for a search for "symmetric difference."

These were one-off checks for this draft, not a maintained regression suite. They support reviewing the examples and rendering; they cannot establish that the teaching flow works for every reader. The next pass should include reading the checkpoints without their answers.

## Questions for the next pass

- Do set foundations and set operations need more worked examples, or do the checkpoints suffice?
- Does showing character classes before repetition make the later examples easier to follow?
- Is the building-block page comfortable to read, or should its sections become separate pages?
- Which concepts need diagrams or exercises before moving into type constraints?
- Should the eventual language use whole-string membership, and what universe of values would its complements use?
- How should string-set intersection and difference be expressed, given that Rust's class operators only operate on characters?

The last two are open language-design questions, not gaps to silently fill in during this documentation pass.

Return to the [reading path](/#reading-path).
