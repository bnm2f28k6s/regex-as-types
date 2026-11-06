# Supplemental regex translations

This optional companion starts with [our proposed pattern language](pattern-language.html) and asks how selected rules could be written using existing tools. You can read the core lessons without learning these translations. They are examples, not a compiler, a target commitment, or the definition of our language.

The reference tools here are Rust `regex` **1.12.2**, with default crate features and flags, and Pomsky **0.12.0**, compiled with `--flavor rust`. Rust checks use UTF-8 strings, Unicode enabled, and the whole-string wrapper explained below. Pomsky is a [regex-writing language and compiler](https://github.com/pomsky-lang/pomsky/blob/v0.12.0/README.md#compatibility-and-portability), not a matching engine.

## Translate the meaning, not just the symbols

These Rust patterns are bodies to put inside the whole-string wrapper, not complete validators by themselves.

| Our proposed notation | Pomsky example | Rust regex body |
| --- | --- | --- |
| <code>&#96;cat&#96;</code> | `'cat'` | `cat` |
| <code>&#96;&#96;</code> | `''` | Empty body |
| <code>&#96;a+b&#96;</code> | `'a+b'` | `a\+b` |
| <code>&#96;a&#96; &#124; &#96;b&#96;</code> | <code>&#39;a&#39; &#124; &#39;b&#39;</code> | `[ab]` |
| <code>[&#96;a&#96;-&#96;c&#96;]</code> | `['a'-'c']` | `[a-c]` |
| <code>&#96;a&#96; &#96;b&#96;</code> | `'a' 'b'` | `ab` |
| <code>&#96;cat&#96; &#124; &#96;dog&#96;</code> | <code>&#39;cat&#39; &#124; &#39;dog&#39;</code> | <code>cat&#124;dog</code> |
| <code>&#96;a&#96; (&#96;b&#96; &#124; &#96;c&#96;) &#96;d&#96;</code> | <code>&#39;a&#39; (&#39;b&#39; &#124; &#39;c&#39;) &#39;d&#39;</code> | <code>a(?:b&#124;c)d</code> |
| <code>&#96;a&#96;+</code> | `'a'+` | `a+` |
| <code>&#96;a&#96; &#96;b&#96;&#42;</code> | `'a' 'b'*` | `ab*` |
| <code>&#96;ab&#96;&#42;</code> | `'ab'*` | `(?:ab)*` |

Our preferred notation uses backtick-delimited literals and `|` for explicit choices; the core lessons use brackets for character ranges and `[]` for the empty set. Optional bracketed choice shorthand remains an open design possibility. An external translation may still use a character class: Rust's `[ab]` selects either `a` or `b`, as defined by its [character-class rules](https://docs.rs/regex/1.12.2/regex/#character-classes). That equivalent target spelling does not decide the syntax or semantics of possible shorthand in our language.

The literal <code>&#96;ab&#96;</code> is one part in our proposal, so repeating it repeats the whole text. Copying its contents into Rust as `ab*` would instead repeat only `b`. Similarly, literal operator characters need escaping in Rust regex bodies. See Rust's [repetitions](https://docs.rs/regex/1.12.2/regex/#repetitions), [grouping](https://docs.rs/regex/1.12.2/regex/#grouping-and-flags), and [escape sequences](https://docs.rs/regex/1.12.2/regex/#escape-sequences), alongside Pomsky's [strings](https://pomsky-lang.org/docs/language-tour/strings/), [alternatives](https://pomsky-lang.org/docs/language-tour/alternations/), [character sets](https://pomsky-lang.org/docs/language-tour/character-sets/), and [repetition](https://pomsky-lang.org/docs/language-tour/repetitions/).

Our `[]` spelling is defined by the core language, not by an external engine. This table does not supply its translation; copying the same symbols into another tool is not evidence that it preserves the empty-set meaning.

## Preserving whole-string acceptance

Rust's [`Regex::is_match`](https://docs.rs/regex/1.12.2/regex/struct.Regex.html#method.is_match) reports whether a match exists somewhere in its input. To use it for membership examples, enclose a translated body p in `\A(?:p)\z`. Here p is a placeholder for the body, not a literal letter to insert.

Rust's [assertions](https://docs.rs/regex/1.12.2/regex/#empty-matches) define `\A` as input start and `\z` as input end. The [non-capturing group](https://docs.rs/regex/1.12.2/regex/#grouping-and-flags) keeps all alternatives inside those boundaries. For example, the body `cat|dog` becomes `\A(?:cat|dog)\z`. This adapter supplies an existing tool with the whole-string rule our language already has.

This complete Rust example demonstrates the distinction:

```rust
use regex::Regex;

fn main() {
    let search = Regex::new(r"cat").unwrap();
    assert!(search.is_match("a cat!"));

    let whole = Regex::new(r"\A(?:cat)\z").unwrap();
    assert!(whole.is_match("cat"));
    assert!(!whole.is_match("a cat!"));
    assert!(!whole.is_match("cats"));
    assert!(!whole.is_match("cat\n"));
    assert!(!whole.is_match(""));
}
```

Rust's `r"..."` is a [raw string literal](https://doc.rust-lang.org/reference/tokens.html#raw-string-literals). It keeps backslashes from requiring another layer of Rust escaping. These delimiters belong to the host Rust program, not to regex syntax or our proposed language.

## A label in existing tools

The [label example](regex-building-blocks.html#a-complete-example) requires lowercase ASCII letters, a hyphen, and exactly two ASCII digits. Each tab below describes the same intended set. The external patterns are bodies, so apply the whole-string adapter after compilation or translation.

# [Our proposal](#/tab/proposal)

```text
[`a`-`z`]+ `-` [`0`-`9`]{2}
```

# [Pomsky](#/tab/pomsky)

```text
['a'-'z']+ '-' ['0'-'9']{2}
```

# [Rust regex](#/tab/rust)

```text
[a-z]+-[0-9]{2}
```

---

`"cat-42"` belongs; `"cat-042"`, `"cat-٣٤"`, and `"cat-42\n"` do not. The explicit ASCII ranges preserve the intended letter and digit sets. Rust's [character classes](https://docs.rs/regex/1.12.2/regex/#character-classes) and [repetition syntax](https://docs.rs/regex/1.12.2/regex/#repetitions) define the target behavior.

## Features we are not importing

External syntax is not automatically a language feature:

- Rust's Unicode-aware `\d`, `\s`, and `\w` have particular [character-set definitions](https://docs.rs/regex/1.12.2/regex/#perl-character-classes-unicode-friendly). A future shorthand in our language would need its own explicit definition.
- Rust has intersection, difference, and symmetric difference [inside character classes](https://docs.rs/regex/1.12.2/regex/#character-classes). That does not define operators on arbitrary string sets in our language.
- Rust's [greedy and lazy quantifiers](https://docs.rs/regex/1.12.2/regex/#repetitions) express search preferences. Our first draft asks only whether the complete input belongs to a set, without exposing a selected match or capture.

We do not need a survey of engine features before developing our small notation. Additional comparisons can be added when a concrete design question needs them.

Return to [building patterns from sets](regex-building-blocks.html) or [open design questions](open-design-questions.html).
