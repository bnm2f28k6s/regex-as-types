# Strings and regexes

We now change the values under discussion from small numbers to strings. Keep the [set operations](set-operations.html) in mind: the goal is to understand a pattern by asking which strings it accepts.

## Strings and the empty string

Our language uses strings as its value model, including numeric values described by constrained string sets. For these lessons, a string is a finite sequence of Unicode scalar values. The scalar-value definition is a teaching assumption, not a requirement to use a particular encoding, library, or storage format. The final character model and representation remain [open design questions](open-design-questions.html#what-values-do-constraints-describe). Whole-string acceptance is fixed.

Unlike a set, a string preserves order and repetition. `"ab"` differs from `"ba"`, and `"aa"` differs from `"a"`. Quotes in our prose mark string values; they are not part of those values.

The empty string, written `""` in examples and ε in mathematical discussion, has no characters. It is still a value. Thus `{""}` is a set with one element, whereas `∅` has no elements.

"Character" on these pages means a Unicode scalar value, not necessarily a whole visible symbol. For a technical reference on this distinction, see the [Unicode Standard's definitions of scalar values and grapheme clusters](https://www.unicode.org/versions/Unicode17.0.0/core-spec/chapter-3/#G2212). The first pattern examples use ASCII characters so we can concentrate on set building.

**Checkpoint.** Are `{"ab", "ba"}` and `{"ba", "ab"}` equal? Are `"ab"` and `"ba"` equal?

Answer: the sets are equal; the strings are not.

## A pattern as a description of a set

For this draft, choose the universe U to be all finite strings of Unicode scalar values. Define `L(p)` to mean the set of complete strings accepted by pattern p. This asks about membership, not where a match occurs in a larger text.

```text
L(p) = {s ∈ U | s matches p as a whole string}
```

This is the [set-builder idea](sets.html#describing-a-set-with-a-rule) applied to strings. A pattern is the description; `L(p)` is the set it describes. The letter p is a placeholder in our mathematical discussion, not variable notation in the proposed language.

For example, a pattern that means "exactly the text cat" describes `{"cat"}`. The strings `"cats"`, `"a cat"`, and `""` are outside this set. The [next lesson](pattern-language.html) writes that pattern as <code>&#96;cat&#96;</code>: a literal value used as a description of the set containing it. Backticks mark pattern notation; double quotes continue to mark example string values.

**Checkpoint.** Can a small pattern describe an infinite set?

Answer: yes. A rule saying "any finite number of a characters, including none" describes infinitely many finite strings. We will give it notation after introducing literals.

## Search versus whole-string membership

A search asks whether some part of the input fits a pattern. Whole-string membership asks whether the entire input fits. These are different questions:

| Input | Contains the text cat? | Is exactly the text cat? |
| --- | --- | --- |
| `"cat"` | Yes | Yes |
| `"cats"` | Yes | No |
| `"a cat!"` | Yes | No |
| `""` | No | No |

Our language uses the second question. It must consume the input from beginning to end, without ignoring extra text, spaces, or a trailing line feed. This rule does not need a special symbol in each pattern.

External regex tools may provide search APIs. Rust's [`Regex::is_match`](https://docs.rs/regex/1.12.2/regex/struct.Regex.html#method.is_match), for example, reports whether a match exists somewhere in the input. Adapting such an API to our whole-string rule belongs in the optional [translation companion](regex-translations.html#preserving-whole-string-acceptance), not in the core notation.

**Checkpoint.** Would finding cat inside `"cats"` establish membership in the singleton set `{"cat"}`?

Answer: no. The input is the value `"cats"`, not the value `"cat"`.

## Character sets versus string sets

A character choice selects one character, for example either `a` or `b`. As a complete-string constraint, it describes `{"a", "b"}`.

The literal string `"ab"` instead gives the singleton set `{"ab"}`. One description chooses one character; the other requires two characters in order. We can understand the distinction before choosing how to spell the descriptions.

**Checkpoint.** Does choosing one character from `{a,b}` accept the whole string `"ab"`?

Answer: no. The choice supplies only one character.

## Where type constraints enter

A set description restricts allowed values. A constraint whose set is `{"cat"}` accepts only that string. Our language describes such string sets directly so we can use the notation at the type level. The later [sets-as-types lesson](sets-as-types.html) explains the approved rules: a type expression denotes its allowed-value set, equal denoted sets give equal pattern types, and inclusion defines subtyping. Unknown membership requires an explicit check before constrained use. Detailed expression rules remain [open questions](open-design-questions.html#how-do-type-expressions-support-checking); static or dynamic enforcement and failure reporting are [deferred integration concerns](open-design-questions.html#deferred-implementation-and-host-integration).

**Checkpoint.** Have we defined a programming language by defining `L(p)`?

Answer: no. We have chosen a way to discuss allowed string sets and fixed whole-string acceptance. We still need notation and, later, typing rules.

Next: [our first pattern language](pattern-language.html).
