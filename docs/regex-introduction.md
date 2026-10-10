# Strings and regexes

We now change the values under discussion from small numbers to strings. Keep the [set operations](set-operations.html) in mind: the goal is to understand a pattern by asking which strings it accepts.

## Strings and the empty string

For these lessons, a string is a finite ordered sequence of Unicode scalar values, represented as UTF-8. This matches the input model of Rust's [`Regex`](https://docs.rs/regex/1.12.2/regex/struct.Regex.html) and its [Unicode matching behavior](https://docs.rs/regex/1.12.2/regex/#unicode). We are not using `bytes::Regex`.

Unlike a set, a string preserves order and repetition. `"ab"` differs from `"ba"`, and `"aa"` differs from `"a"`. Quotes in our prose mark string values; they are not part of those values.

The empty string, written `""` in examples and ε in mathematical discussion, has no characters. It is still a value. Thus `{""}` is a set with one element, whereas `∅` has no elements.

"Character" on these pages means a Unicode scalar value, not necessarily a whole visible symbol. The [Rust regex Unicode documentation](https://docs.rs/regex/1.12.2/regex/#unicode) distinguishes codepoint matching from more advanced Unicode support.

**Checkpoint.** Are `{"ab", "ba"}` and `{"ba", "ab"}` equal? Are `"ab"` and `"ba"` equal?

Answer: the sets are equal; the strings are not.

## A pattern as a description of a set

For this draft, choose the universe U to be all finite strings of Unicode scalar values. Define `L(p)` to mean the set of strings that match pattern p **as an entire string**, under our stated engine and flags.

```math
L(p) = \{s \in U \mid s \text{ matches } p \text{ as a whole string}\}
```

This is our mathematical convention for discussing engine patterns, not syntax for the proposed language. A pattern is the description; `L(p)` is the set it describes. Rust's [syntax reference](https://docs.rs/regex/1.12.2/regex/#syntax) supplies the matching rules used in this definition.

For example, the literal pattern `cat` gives `L(cat) = {"cat"}`. Under whole-string matching, `"cats"`, `"a cat"`, and `""` are outside this set.

**Checkpoint.** Can a small pattern describe an infinite set?

Answer: yes. We will see that `a*` accepts any finite number of `a` characters, including none.

## Search versus whole-string membership

Rust's [`Regex::is_match`](https://docs.rs/regex/1.12.2/regex/struct.Regex.html#method.is_match) answers whether a match exists somewhere in its input. It is a search API, not automatically a whole-string validator.

To test membership in `L(p)`, our examples enclose p in `\A(?:p)\z`. The [assertion syntax](https://docs.rs/regex/1.12.2/regex/#empty-matches) defines `\A` as the start of the input and `\z` as its end. The [non-capturing group](https://docs.rs/regex/1.12.2/regex/#grouping-and-flags) keeps all of p between those boundaries, including any alternatives. `p` is a placeholder here, not a literal letter to insert.

This complete example uses `regex` 1.12.2 with default crate features and flags:

```rust
use regex::Regex;

fn main() {
    let search = Regex::new(r"cat").unwrap();
    assert!(search.is_match("a cat!"));

    let whole = Regex::new(r"\A(?:cat)\z").unwrap();
    assert!(whole.is_match("cat"));
    assert!(!whole.is_match("a cat!"));
    assert!(!whole.is_match("cat\n"));
    assert!(!whole.is_match(""));
}
```

Rust's `r"..."` is a [raw string literal](https://doc.rust-lang.org/reference/tokens.html#raw-string-literals). It keeps regex backslashes from needing a second layer of Rust escaping. The raw-string delimiters are Rust code, not regex syntax.

**Checkpoint.** Would an unanchored `cat` accept `"cats"` as a search?

Answer: yes. It finds the substring `"cat"`. Our whole-string check rejects it.

## Character sets versus string sets

A character class such as `[ab]` selects one character, either `a` or `b`, according to Rust's [character-class syntax](https://docs.rs/regex/1.12.2/regex/#character-classes). Under our whole-string convention its language is `{"a", "b"}`.

The literal sequence `ab` instead describes `{"ab"}`. One pattern chooses a character; the other joins two characters in order. This distinction will matter when we connect character-class set operations to operations on entire string languages.

**Checkpoint.** Does `[ab]` accept `"ab"` as a whole string?

Answer: no. A single class consumes only one character.

## Where type constraints could enter

Our proposed direction is to use a set description to restrict allowed values. For example, if a hypothetical constraint allowed exactly `L(cat)`, only the string `"cat"` would satisfy it under this lesson's assumptions.

That is a design proposal, not a rule of Rust or a settled type system. We have not chosen type syntax, decided whether non-string values are included, or defined how inclusion between allowed sets would relate to subtyping. We will return to these questions after the regex foundations.

**Checkpoint.** Have we defined a programming language by defining `L(p)`?

Answer: no. We have chosen a way to discuss matching sets, not language syntax or typing rules.

Next: [Rust regex building blocks](regex-building-blocks.html).
