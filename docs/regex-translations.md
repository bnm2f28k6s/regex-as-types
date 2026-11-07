# Supplemental regex translations

This optional companion starts with [our proposed pattern language](pattern-language.html) and asks how selected rules could be written using existing tools. You can read the core lessons without learning these translations. They are examples, not a compiler, a target commitment, or the definition of our language.

The comparisons cover Rust `regex`, Pomsky, JavaScript `RegExp`, Python `re`, Java `Pattern`, .NET `Regex` in C#, and PCRE2. The purpose is to recognize our examples in another programming language or regex tool, not to learn each system's full syntax or extensions. Similar-looking examples are not a promise of general compatibility.

Pomsky is a [regex-writing language and compiler](https://github.com/pomsky-lang/pomsky/blob/v0.12.0/README.md#compatibility-and-portability), not a matching engine. Its examples here use **0.12.0** targeting Rust `regex` **1.12.2**. The other systems have their own matching APIs; the short adapters below preserve our whole-string rule without bringing those APIs into the core lessons.

## Translate the meaning, not just the symbols

For these small examples, Rust, JavaScript, Python, Java, .NET, and PCRE2 can use the same regex body. We show that body once rather than repeat identical columns. It is not a complete validator by itself: use the appropriate whole-string API or wrapper from the next section.

The external spellings use literals, character classes, grouping, alternatives, and repetition as documented by [Rust's syntax reference](https://docs.rs/regex/1.12.2/regex/#syntax), [JavaScript's regex reference](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Regular_expressions), [Python's regex syntax](https://docs.python.org/3.9/library/re.html#regular-expression-syntax), [Java's pattern constructs](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/regex/Pattern.html), [.NET's language reference](https://learn.microsoft.com/en-us/dotnet/standard/base-types/regular-expression-language-quick-reference), and [PCRE2's pattern reference](https://pcre2project.github.io/pcre2/doc/pcre2pattern/). This shared subset is enough for the examples, not a definition of our notation.

| Our proposed notation | Pomsky example | Regex body in all six engines |
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

The literal <code>&#96;ab&#96;</code> is one part in our proposal, so repeating it repeats the whole text. Copying its contents into any of these regex bodies as `ab*` would instead repeat only `b`; use `(?:ab)*`. Likewise, our literal <code>&#96;a+b&#96;</code> becomes the body `a\+b`, because the plus must remain literal. These are translations of the intended strings, not symbol-for-symbol copies. Compare the engine references above with Pomsky's [strings](https://pomsky-lang.org/docs/language-tour/strings/), [alternatives](https://pomsky-lang.org/docs/language-tour/alternations/), [character sets](https://pomsky-lang.org/docs/language-tour/character-sets/), and [repetition](https://pomsky-lang.org/docs/language-tour/repetitions/).

Our `[]` spelling is defined by the core language, not by an external engine. This table does not supply its translation; copying the same symbols into another tool is not evidence that it preserves the empty-set meaning.

## Preserving whole-string acceptance

Our notation always checks the complete input. In external tools, a regex body and the API that uses it are separate choices. Here `p` means a translated body and `input` means the complete, unmodified input string. Neither is new variable syntax for our language.

- **Rust `regex` 1.12.2.** Put the body inside `\A(?:p)\z`, then call `is_match(input)`. Use UTF-8 strings with default crate features and flags. See [assertions and grouping](https://docs.rs/regex/1.12.2/regex/#syntax).

- **Pomsky 0.12.0.** Compile with `--flavor rust`, then use the Rust adapter on the compiled body. See [target-flavor selection](https://github.com/pomsky-lang/pomsky/blob/v0.12.0/README.md#compatibility-and-portability).

- **JavaScript `RegExp`.** Put the body inside `/^(?:p)$/u`, then call `.test(input)`. Use only the `u` flag, without multiline or stateful search flags. See [input boundaries](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Regular_expressions/Input_boundary_assertion).

- **Python `re`.** Call `re.fullmatch(body, input)` and check that the result `is not None`. Use Unicode `str` input with no extra flags. See [Python 3.9 fullmatch](https://docs.python.org/3.9/library/re.html#re.fullmatch).

- **Java `Pattern`.** Compile with `Pattern.compile(body)`, create a matcher with `.matcher(input)`, then call `.matches()`. Use default flags and the original full input region. See [Java 25 matching methods](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/regex/Matcher.html#matches()).

- **.NET `Regex`.** Put the body inside `\A(?:p)\z`, then call `Regex.IsMatch`. Use C# string input with `RegexOptions.None`. See [.NET 10 IsMatch](https://learn.microsoft.com/en-us/dotnet/api/system.text.regularexpressions.regex.ismatch?view=net-10.0) and [absolute anchors](https://learn.microsoft.com/en-us/dotnet/standard/base-types/regular-expression-language-quick-reference#anchors).

- **PCRE2.** Put the body inside `(*UTF)\A(?:p)\z`. Use the 8-bit library, a UTF-8 subject, and standard `pcre2_match` from offset zero, with no other options. See [UTF mode](https://pcre2project.github.io/pcre2/doc/pcre2pattern/#utf-support) and [absolute assertions](https://pcre2project.github.io/pcre2/doc/pcre2pattern/#simple-assertions).

JavaScript and Python host strings, Java and C# strings, and Rust raw strings are ways to present a pattern to a tool. They are not delimiters in our proposed notation. Keep the adapters specific to their system rather than assuming that the same anchors or API names work everywhere.

### Rust search versus membership

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

The [label example](regex-building-blocks.html#a-complete-example) requires lowercase ASCII letters, a hyphen, and exactly two ASCII digits. Each tab below illustrates the same intended set. Choose any spelling from this single comparison group; the tab labels wrap onto more rows when needed. The host-language snippets are usage fragments with a Boolean result named `accepted`; they use `"cat-42"` as the example input. Pomsky shows a body to compile and adapt; PCRE2 shows a pattern to pass to its matching API. Neither has a universal host-language string spelling.

<style>
/* Keep this page's comparison tabs together without widening the reading column. */
.docgen-content .tabgroup > .tab-list {
  flex-wrap: wrap;
  gap: 0.5rem 0.25rem;
  padding: 0.5rem 0.5rem 0.75rem;
}
.docgen-content .tabgroup > .tab-list > li {
  padding: 0;
}
.docgen-content .tabgroup > .tab-list > li > label {
  display: block;
  padding: 0.5rem 0.75rem;
  border-bottom: 3px solid transparent;
}
.docgen-content .tabgroup > .tab-list > li > label.active {
  border-bottom-color: var(--primary);
}
</style>

# [Our proposal](#/tab/proposal)

```text
[`a`-`z`]+ `-` [`0`-`9`]{2}
```

# [Pomsky](#/tab/pomsky)

```text
['a'-'z']+ '-' ['0'-'9']{2}
```

# [Rust regex](#/tab/rust)

```rust
use regex::Regex;

let label = Regex::new(r"\A(?:[a-z]+-[0-9]{2})\z").unwrap();
let accepted = label.is_match("cat-42");
```

# [JavaScript](#/tab/javascript)

```javascript
const label = /^(?:[a-z]+-[0-9]{2})$/u;
const accepted = label.test("cat-42");
```

# [Python](#/tab/python)

```python
import re

accepted = re.fullmatch(r"[a-z]+-[0-9]{2}", "cat-42") is not None
```

# [Java](#/tab/java)

```java
import java.util.regex.Pattern;

Pattern label = Pattern.compile("[a-z]+-[0-9]{2}");
boolean accepted = label.matcher("cat-42").matches();
```

# [.NET (C#)](#/tab/dotnet)

```csharp
using System.Text.RegularExpressions;

bool accepted = Regex.IsMatch(
    "cat-42", @"\A(?:[a-z]+-[0-9]{2})\z", RegexOptions.None);
```

# [PCRE2](#/tab/pcre2)

```text
(*UTF)\A(?:[a-z]+-[0-9]{2})\z
```

---

`"cat-42"` belongs; `"cat-042"`, `"cat-٣٤"`, `"Cat-42"`, `"a cat-42"`, `"cat-42\n"`, and `""` do not. The explicit ASCII ranges preserve the intended letter and digit sets without relying on a shorthand such as `\d`. See the syntax references and adapters above. The visual differences mostly come from each host language's literals and matching API, not from a different rule for this label.

### What was checked

The shared table bodies and label were checked with Node.js **26.13.0** (`u` only), CPython **3.9.6** (`str`, default flags), PCRE2 **10.49** (8-bit, UTF mode, standard matching), and Rust `regex` **1.12.2** (default crate features and flags, UTF-8). Pomsky **0.12.0** compiled the authored examples with `--flavor rust`; those outputs passed the same Rust checks. These one-off checks covered empty input, literal punctuation, grouped repetition, extra prefix/suffix text, non-ASCII digits, and trailing line feeds. See [the review page](review.html#verification-scope) for the check procedure.

The Java 25 and .NET 10 examples are documentation-backed illustrations, not locally executed examples. None of these checks executes our proposed notation or proves cross-engine equivalence beyond the tested examples.

## Features we are not importing

External syntax is not automatically a language feature:

- Rust's Unicode-aware `\d`, `\s`, and `\w` have particular [character-set definitions](https://docs.rs/regex/1.12.2/regex/#perl-character-classes-unicode-friendly). A future shorthand in our language would need its own explicit definition.
- Rust has intersection, difference, and symmetric difference [inside character classes](https://docs.rs/regex/1.12.2/regex/#character-classes). That does not define operators on arbitrary string sets in our language.
- Rust's [greedy and lazy quantifiers](https://docs.rs/regex/1.12.2/regex/#repetitions) express search preferences. Our first draft asks only whether the complete input belongs to a set, without exposing a selected match or capture.

The added comparisons illustrate familiar spellings, not a survey of engine extensions. Lookarounds, backreferences, captures, and other tool-specific facilities are not part of our proposal merely because an external tool offers them. Keep new comparisons tied to a lesson example rather than making the main path depend on an engine manual.

Return to [building patterns from sets](regex-building-blocks.html) or [open design questions](open-design-questions.html).
