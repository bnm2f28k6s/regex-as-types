# Pomsky and regex syntax comparisons

[Pomsky](https://pomsky-lang.org/) is a language for writing regexes, not a matching engine. Its compiler produces a pattern for a selected regex flavor; that engine then performs the matching. The [Pomsky 0.12.0 compatibility guide](https://github.com/pomsky-lang/pomsky/blob/v0.12.0/README.md#compatibility-and-portability) lists targets including Rust, JavaScript, Python, Ruby, Java, .NET, PCRE, and RE2.

Read [Rust regex building blocks](regex-building-blocks.html) first. Here we compare ways to describe the same allowed strings, then ask which syntax ideas might suit this project.

## Engines and syntaxes in our comparison list

- **Rust's `regex` crate** is our primary matching reference, currently version 1.12.2. Its [syntax documentation](https://docs.rs/regex/1.12.2/regex/#syntax) defines the patterns used in these lessons.
- **JavaScript, Python, Ruby, and Perl regex systems** remain comparison candidates. Each future example needs its own engine documentation, version, flags, and matching mode. We are not claiming that they interpret every pattern alike.
- **Pomsky** is a comparison syntax and compiler. We use version 0.12.0 and explicitly select its `rust` target flavor, rather than treating it as an independent engine.
- **Our set notation** describes the allowed values mathematically. It is not executable syntax or an approved notation for the possible programming language.

This separation lets us compare readability without confusing source syntax, generated patterns, and matching behavior.

## How to read the tabs

Each example has **Pomsky**, **Rust regex**, and **Our set notation** tabs. Select a tab to compare representations. The same selection applies to all example groups on this page, using [Docgen 0.3.3's synchronized tabs](https://github.com/thecodrr/docgen/blob/0.3.3/docs/features/tabs.md#synced-tabs).

The code panels show unanchored expressions. Rust panels define a pattern constant, not a complete program. For membership checks, compile the Pomsky expression with `--flavor rust` and wrap both its output and the Rust pattern in `\A(?:pattern)\z`. This follows our [whole-string convention](regex-introduction.html#search-versus-whole-string-membership), not Pomsky's default search behavior.

All checks use UTF-8 strings, Unicode enabled, case-sensitive matching, and other engine flags at their defaults. The universe U is all finite strings of Unicode scalar values. Input quotes in the tables are not part of the strings; `""` is the empty string and `"\n"` contains a newline.

Pomsky panels use plain-text fences because the installed Docgen has no Pomsky highlighter. Rust panels use Rust highlighting; set panels use plain text or the site's math renderer. A rendering choice is not evidence that an expression executes.

## Quoted literals

Pomsky puts literal text in quotes and ignores formatting whitespace outside strings, as its [string lesson](https://pomsky-lang.org/docs/language-tour/strings/) explains. This makes the literal plus sign visible without regex escaping. Rust instead uses an [escaped plus](https://docs.rs/regex/1.12.2/regex/#escape-sequences).

# [Pomsky](#/tab/pomsky)

```text
'a+b'
```

# [Rust regex](#/tab/rust)

```rust
const PATTERN: &str = r"a\+b";
```

# [Our set notation](#/tab/sets)

```text
L = {"a+b"}
```

---

The set panel contains one string, not three characters to choose from.

| Accepted strings | Rejected strings |
| --- | --- |
| `"a+b"` | `"ab"`, `"aaab"`, `"a+b!"`, `""` |

**Checkpoint.** Is the plus a repetition operator in either of these examples?

Answer: no. It is quoted in Pomsky and escaped in the Rust pattern.

## Alternatives as union

Pomsky's [alternation syntax](https://pomsky-lang.org/docs/language-tour/alternations/) uses `|`, as does Rust's [composite syntax](https://docs.rs/regex/1.12.2/regex/#composites). Under whole-string matching, the set interpretation is the union of the two singleton sets, using our [union definition](set-operations.html#union).

# [Pomsky](#/tab/pomsky)

```text
'cat' | 'dog'
```

# [Rust regex](#/tab/rust)

```rust
const PATTERN: &str = r"cat|dog";
```

# [Our set notation](#/tab/sets)

```math
L = \{\text{cat}\} \cup \{\text{dog}\}
```

---

| Accepted strings | Rejected strings |
| --- | --- |
| `"cat"`, `"dog"` | `"catdog"`, `"cow"`, `"a cat"`, `"cat\n"`, `""` |

**Checkpoint.** Would these unanchored patterns reject `"a cat"` during substring search?

Answer: no. The whole-string wrapper is what makes that input fail our membership check.

## Named fragments, concatenation, and repetition

Pomsky's [`let` declarations](https://pomsky-lang.org/docs/language-tour/variables/) name expressions that are expanded into the generated regex. They are reusable pattern fragments, not captures or types. Its [character sets](https://pomsky-lang.org/docs/language-tour/character-sets/) and [repetition operators](https://pomsky-lang.org/docs/language-tour/repetitions/) let us restate the label format from the [combined Rust example](regex-building-blocks.html#putting-the-pieces-together).

# [Pomsky](#/tab/pomsky)

```text
let letter = ['a'-'z'];
let digit = ['0'-'9'];
letter+ '-' digit{2}
```

# [Rust regex](#/tab/rust)

```rust
const PATTERN: &str = r"[a-z]+-[0-9]{2}";
```

# [Our set notation](#/tab/sets)

```math
L = A^+ H D D
```

---

Here A is the set of one-character strings `{"a", ..., "z"}`, H is `{"-"}`, and D is `{"0", ..., "9"}`. We write `A+` for one or more concatenated members of A. Juxtaposition concatenates string sets in order, not tuples or numbers. Thus `A+ H D D` takes a nonempty lowercase word, a hyphen, and two digits. The formula is our deduction from the [concatenation and repetition rules](regex-building-blocks.html#concatenation), not Pomsky or proposed type syntax.

| Accepted strings | Rejected strings |
| --- | --- |
| `"a-00"`, `"cat-42"` | `"-42"`, `"Cat-42"`, `"cat-4"`, `"cat-042"`, `"cat-٣٤"`, `"cat-42\n"`, `""` |

We use an explicit ASCII digit range. Replacing it with a Unicode digit shorthand would change the rule; compare Rust's [Unicode-friendly classes](https://docs.rs/regex/1.12.2/regex/#perl-character-classes-unicode-friendly).

**Checkpoint.** Does a Pomsky variable declaration create a new runtime value or a type?

Answer: neither in this example. It names a pattern fragment that the compiler expands.

## Character-set intersection

Pomsky 0.12 added `&` for intersecting character sets. Its [intersection reference](https://pomsky-lang.org/docs/reference/constructs/intersection/) limits the operands to character sets or variables resolving to them. Rust places `&&` inside [character classes](https://docs.rs/regex/1.12.2/regex/#character-classes).

# [Pomsky](#/tab/pomsky)

```text
['a'-'c'] & ['b'-'d']
```

# [Rust regex](#/tab/rust)

```rust
const PATTERN: &str = r"[[a-c]&&[b-d]]";
```

# [Our set notation](#/tab/sets)

```math
L = \{\text{a},\text{b},\text{c}\} \cap \{\text{b},\text{c},\text{d}\}
  = \{\text{b},\text{c}\}
```

---

Each listed element is a one-character string. This set interpretation follows from the engines' one-character class rules and our [intersection definition](set-operations.html#intersection).

| Accepted strings | Rejected strings |
| --- | --- |
| `"b"`, `"c"` | `"a"`, `"d"`, `"bc"`, `""` |

Pomsky also expresses character-set subtraction by intersecting with a negated class, for example `['a'-'d'] & !['bc']`, as the [0.12.0 release notes](https://github.com/pomsky-lang/pomsky/blob/v0.12.0/CHANGELOG.md#new) describe. Neither this nor `&` supplies general intersection or complement of arbitrary string languages. That remains an [open design question](review.html#questions-for-the-next-pass) here.

**Checkpoint.** Can we replace these classes with `'cat' & 'dog'` to intersect whole words?

Answer: no. That is outside Pomsky's supported intersection operands.

## Numeric ranges still describe strings

Pomsky's [`range` notation](https://pomsky-lang.org/docs/language-tour/ranges/) describes textual numbers across several digits. It is different from a character range such as `['0'-'9']`. The Rust panel below is a hand-written equivalent using the crate's [alternation and repetition syntax](https://docs.rs/regex/1.12.2/regex/#syntax), not a claim about the exact pattern Pomsky emits.

# [Pomsky](#/tab/pomsky)

```text
range '0'-'255'
```

# [Rust regex](#/tab/rust)

```rust
const PATTERN: &str = r"0|[1-9][0-9]?|1[0-9]{2}|2[0-4][0-9]|25[0-5]";
```

# [Our set notation](#/tab/sets)

```math
L = \{\operatorname{decimal}(n) \mid n \in \mathbb{Z},\ 0 \leq n \leq 255\}
```

---

For this formula, `decimal(n)` means the ordinary ASCII base-10 spelling of the integer n, with no leading zeroes except the string `"0"`. We use integers to describe the set, but its members are strings. Matching `"42"` does not parse it into an integer or impose a numeric type.

| Accepted strings | Rejected strings |
| --- | --- |
| `"0"`, `"9"`, `"10"`, `"99"`, `"100"`, `"249"`, `"250"`, `"255"` | `"256"`, `"999"`, `"00"`, `"042"`, `"-1"`, `"+1"`, `"٢٥٥"`, `"255\n"`, `""` |

**Checkpoint.** Does the range include the string `"042"`?

Answer: no. This example uses the spelling without leading zeroes. A different textual representation needs a different expression and set definition.

## Tests beside the expression

Pomsky can keep examples in a [`test` block](https://pomsky-lang.org/docs/reference/constructs/tests/). `match` and `reject` without `in` assert whole-string behavior; forms using `in` instead test substring search. This is worth considering for our documentation and any future syntax.

For example, this is a complete Pomsky source file for the label rule:

```text
test {
    match 'a-00';
    match 'cat-42';
    reject '';
    reject 'cat-4';
    reject 'cat-042';
    reject 'cat-٣٤';
}

let letter = ['a'-'z'];
let digit = ['0'-'9'];
letter+ '-' digit{2}
```

Test-engine selection matters. The [0.12.0 release notes](https://github.com/pomsky-lang/pomsky/blob/v0.12.0/CHANGELOG.md#new) add Rust test support; the website's test reference still describes PCRE2-only execution. Check the actual binary and state which engine ran, rather than assuming these accounts agree or using a different engine as proof of Rust behavior.

The complete file above passed with the downloaded Pomsky 0.12.0 release binary using `pomsky test --flavor rust --engine rust --path label.pomsky`. We also checked its cases separately with Rust `regex` 1.12.2; selecting Rust in Pomsky does not itself pin that crate version.

**Checkpoint.** Is a successful PCRE2 test sufficient to call a Rust example verified?

Answer: no. Compile and run the generated pattern with the stated Rust engine as well.

## Ideas to adapt, not rules we have adopted

These are proposals for discussion, based on the syntax comparisons above:

- **Quote literal strings.** Make literal text visibly different from names and operators. Decide how escaping works before settling a syntax.
- **Allow named set or pattern fragments.** Pomsky's `let` gives a useful readability model. We still need to decide whether our names refer to character sets, string sets, types, or several distinct kinds of thing.
- **Keep character and string operations distinct.** A readable `&` must not conceal which universe and operand kinds it supports. General string-set intersection needs its own semantics, not an assumption that Pomsky already supplies it.
- **Use descriptive range notation.** A compact numeric-looking rule is useful, but distinguish a set of textual representations from a set of numeric values. Leading zeroes and signs must remain explicit choices.
- **Keep accepted and rejected examples near the rule.** Pomsky's test blocks offer a model for documentation that could later become executable. We have not chosen test syntax or added a compiler here.

Captures and lookaround may be useful in later comparisons, but they are not prerequisites for these membership examples. Pomsky cannot make an unsupported target feature available merely by changing its spelling; Rust's [crate overview](https://docs.rs/regex/1.12.2/regex/) excludes lookaround and backreferences.

**Checkpoint.** Have these comparisons selected our language's syntax or type rules?

Answer: no. They give us concrete alternatives to discuss while the design remains open.

Next: [review this draft](review.html).
