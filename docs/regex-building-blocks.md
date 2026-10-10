# Rust regex building blocks

Read [strings and regexes](regex-introduction.html) first. This page uses Rust's `regex` crate 1.12.2, default features, Unicode enabled, and other flags at their defaults unless a pattern changes them.

In the tables, a pattern is shown without its whole-string wrapper. Test it as `\A(?:pattern)\z`, as explained in the [matching convention](regex-introduction.html#search-versus-whole-string-membership). Every listed accepted and rejected string is a membership example, not a substring search. `""` is the empty string; `"\n"` contains a newline; `"\t"` contains a tab. Quotes are not part of the input.

## Literals

A literal matches itself. The pattern `cat` describes the singleton set `{"cat"}` under whole-string matching. Rust permits [Unicode characters directly in patterns](https://docs.rs/regex/1.12.2/regex/#unicode), so literals are not restricted to ASCII.

| Pattern | Accepted strings | Rejected strings |
| --- | --- | --- |
| `cat` | `"cat"` | `"Cat"`, `"cats"`, `""` |
| `é` | `"é"` | `"e"`, `"éé"`, `""` |

**Checkpoint.** Is literal matching case-sensitive by default?

Answer: yes. We will explicitly enable a flag when we want case-insensitive matching.

## Escaping special characters

Some characters instruct the engine rather than matching themselves. For example, `.` is a wildcard; `\.` matches a literal dot. Rust documents these forms in its [escape sequences](https://docs.rs/regex/1.12.2/regex/#escape-sequences).

| Pattern | Accepted strings | Rejected strings |
| --- | --- | --- |
| `\.` | `"."` | `"a"`, `".."`, `""` |
| `a\+b` | `"a+b"` | `"ab"`, `"aaab"`, `""` |

In Rust source, write a regex backslash directly inside a raw string: `r"\."`. That is different from the ordinary Rust string `"\\."`, although both supply the same pattern. See the crate's [literal-dot example](https://docs.rs/regex/1.12.2/regex/#example-find-a-middle-initial).

**Checkpoint.** Does `a\+b` repeat the letter `a`?

Answer: no. The escaped plus sign is a literal character.

## Character classes and ranges

A class chooses one character from a set. `[abc]` chooses `a`, `b`, or `c`; `[a-c]` describes the same choices with a range. `[0-9]` selects one ASCII digit. These are Rust's [character-class rules](https://docs.rs/regex/1.12.2/regex/#character-classes).

| Pattern | Accepted strings | Rejected strings |
| --- | --- | --- |
| `[abc]` | `"a"`, `"b"`, `"c"` | `"ab"`, `"d"`, `""` |
| `[a-c]` | `"a"`, `"b"`, `"c"` | `"A"`, `"d"`, `""` |
| `[0-9]` | `"0"`, `"9"` | `"10"`, `"٣"`, `""` |

**Checkpoint.** How many characters does one `[0-9]` consume?

Answer: exactly one. It is not an entire multi-digit number.

## Negated character classes

`[^ab]` selects one character other than `a` or `b`. This is complement at the **character** level, as defined in Rust's [class syntax](https://docs.rs/regex/1.12.2/regex/#character-classes).

| Pattern | Accepted strings | Rejected strings |
| --- | --- | --- |
| `[^ab]` | `"c"`, `"é"`, `"\n"` | `"a"`, `"b"`, `"cc"`, `""` |

It is not the complement of the string set `{"a", "b"}` in our universe of all strings. That string-set complement also contains `""` and `"cc"`, but this one-character pattern rejects both. This distinction follows from the class rule and our [chosen universe](regex-introduction.html#a-pattern-as-a-description-of-a-set).

**Checkpoint.** Does negation make a class accept strings of any length?

Answer: no. It changes which character is allowed, not how many are consumed.

## The wildcard

By default, `.` matches one Unicode scalar value other than newline (`\n`). It does not mean "any string." See Rust's [one-character syntax](https://docs.rs/regex/1.12.2/regex/#matching-one-character) and [Unicode model](https://docs.rs/regex/1.12.2/regex/#unicode).

| Pattern | Accepted strings | Rejected strings |
| --- | --- | --- |
| `.` | `"a"`, `"é"`, `"🙂"` | `""`, `"ab"`, `"\n"` |

**Checkpoint.** Will a multi-byte UTF-8 character such as `é` require several dots?

Answer: no. In our Unicode-enabled string regex, one dot can match the scalar value `é`.

## Concatenation

Writing patterns next to each other joins their matched strings in order. Rust calls this [concatenation](https://docs.rs/regex/1.12.2/regex/#composites).

| Pattern | Accepted strings | Rejected strings |
| --- | --- | --- |
| `ab` | `"ab"` | `"a"`, `"ba"`, `""` |
| `[ab][01]` | `"a0"`, `"a1"`, `"b0"`, `"b1"` | `"0a"`, `"a"`, `"a00"`, `""` |

For sets of strings A and B, we define their concatenation as the set of strings obtained by joining one string from A to one from B. This is our set interpretation of the engine rule:

```math
AB = \{uv \mid u \in A \text{ and } v \in B\}
```

Here `uv` means joined strings, not multiplication. The second example uses `A = {"a", "b"}` and `B = {"0", "1"}`. Compare it with the [Cartesian product](set-operations.html#cartesian-product): concatenation produces `"a0"`, not `("a", "0")`.

**Checkpoint.** Do `ab` and `ba` describe the same set?

Answer: no. String order matters.

## Alternation

The vertical bar chooses between patterns. `cat|dog` accepts either complete word. Rust defines this in its [composite syntax](https://docs.rs/regex/1.12.2/regex/#composites).

| Pattern | Accepted strings | Rejected strings |
| --- | --- | --- |
| <code>cat&#124;dog</code> | `"cat"`, `"dog"` | `"catdog"`, `"cow"`, `""` |
| <code>ab&#124;cd</code> | `"ab"`, `"cd"` | `"abd"`, `"acd"`, `""` |

Under our whole-string membership convention, alternation corresponds to union: a string is accepted if it belongs to either alternative's set. This is a deduction from Rust's alternation rule and the [union definition](set-operations.html#union).

Alternation has lower precedence than concatenation: `ab|cd` means either `ab` or `cd`, not `a` followed by either `b` or `c`, followed by `d`. See the [alternation tutorial](https://www.regular-expressions.info/alternation.html); grouping makes that distinction explicit in the next section.

**Checkpoint.** Is `cat|dog` the same as `[catdog]`?

Answer: no. Alternation chooses a word; that class chooses one of the listed characters.

## Grouping

`(?:...)` groups a pattern without recording a capture. Parentheses let us choose which part an operation acts on. See Rust's [grouping syntax](https://docs.rs/regex/1.12.2/regex/#grouping-and-flags).

| Pattern | Accepted strings | Rejected strings |
| --- | --- | --- |
| <code>a(?:b&#124;c)d</code> | `"abd"`, `"acd"` | `"ab"`, `"cd"`, `"ad"`, `""` |

**Checkpoint.** Does a non-capturing group add literal parentheses to the accepted string?

Answer: no. It organizes the pattern.

## Repetition

A quantifier sets how many times the preceding item or group may match. Rust's [repetition syntax](https://docs.rs/regex/1.12.2/regex/#repetitions) defines these counts:

| Pattern | Count of the preceding item | Accepted strings | Rejected strings |
| --- | --- | --- | --- |
| `a?` | Zero or one | `""`, `"a"` | `"aa"`, `"b"` |
| `a*` | Zero or more | `""`, `"a"`, `"aaa"` | `"b"`, `"ab"` |
| `a+` | One or more | `"a"`, `"aaa"` | `""`, `"b"` |
| `a{2}` | Exactly two | `"aa"` | `"a"`, `"aaa"`, `""` |
| `a{2,3}` | Two through three | `"aa"`, `"aaa"` | `"a"`, `"aaaa"`, `""` |
| `a{2,}` | At least two | `"aa"`, `"aaaa"` | `"a"`, `""`, `"b"` |
| `ab*` | One a, then zero or more b | `"a"`, `"ab"`, `"abbb"` | `""`, `"abab"` |
| `(?:ab)*` | Zero or more copies of ab | `""`, `"ab"`, `"abab"` | `"a"`, `"aba"` |

For an assertion-free pattern describing a string set A, we can interpret star as all finite concatenations of strings from A, including zero strings. This is our deduction from the repetition and concatenation rules. Zero repetitions produce ε, so `a*` accepts the empty string. This is not the [power set](set-operations.html#power-set), which contains subsets rather than joined strings.

**Checkpoint.** Why does `ab*` accept `"a"`, while `(?:ab)*` also accepts `""`?

Answer: in the first pattern, only `b` repeats. In the second, the entire group can occur zero times.

## Shorthand and Unicode classes

Rust's [shorthand classes](https://docs.rs/regex/1.12.2/regex/#perl-character-classes-unicode-friendly) include `\d` for a Unicode decimal digit, `\s` for Unicode whitespace, and `\w` for its Unicode word-character definition. In particular, `\w` is not limited to ASCII letters and includes digits and underscore. [Unicode properties](https://docs.rs/regex/1.12.2/regex/#unicode) provide more explicit categories such as `\p{Letter}`.

| Pattern | Accepted strings | Rejected strings |
| --- | --- | --- |
| `\d` | `"3"`, `"٣"` | `"a"`, `"33"`, `""` |
| `\s` | `" "`, `"\t"`, `"\n"` | `"a"`, `"\t\t"`, `""` |
| `\w` | `"a"`, `"é"`, `"3"`, `"_"` | `"-"`, `"ab"`, `""` |
| `\p{Letter}` | `"a"`, `"é"`, `"β"` | `"3"`, `"_"`, `""` |

Use `[0-9]` when the rule specifically requires ASCII digits. Do not silently replace it with `\d`.

**Checkpoint.** Do `[0-9]` and `\d` describe the same choices here?

Answer: no. The Unicode digit `٣` is accepted only by the latter.

## Set operations inside character classes

Rust supports union, intersection (`&&`), difference (`--`), and symmetric difference (`~~`) inside [character classes](https://docs.rs/regex/1.12.2/regex/#character-classes).

| Pattern | Accepted strings | Rejected strings |
| --- | --- | --- |
| `[a-cx-z]` | `"a"`, `"c"`, `"x"`, `"z"` | `"d"`, `"ax"`, `""` |
| `[[a-c]&&[b-d]]` | `"b"`, `"c"` | `"a"`, `"d"`, `"bc"`, `""` |
| `[[a-d]--[bc]]` | `"a"`, `"d"` | `"b"`, `"c"`, `"ad"`, `""` |
| `[[ab]~~[bc]]` | `"a"`, `"c"` | `"b"`, `"ac"`, `""` |
| `[a&&b]` | None | `"a"`, `"b"`, `""` |

These operate on sets of characters. They do not provide operators for intersecting or subtracting arbitrary multi-character regexes. For example, `[cat&&dog]` intersects the letters in the two classes; it does not compare the words `"cat"` and `"dog"`. This follows from the class grammar and its one-character matching rule.

Nested brackets keep grouping visible. Class operators have their own precedence rules; do not assume they follow mathematical notation.

**Checkpoint.** Can an empty character class match the empty string?

Answer: no. Rust explicitly distinguishes [an empty class from an empty regex](https://docs.rs/regex/1.12.2/regex/#empty-matches).

## Assertions and anchors

An assertion checks a position without consuming a character. Rust's [empty-match syntax](https://docs.rs/regex/1.12.2/regex/#empty-matches) includes `\A` for the beginning of input, `\z` for its end, and `\b` for a word boundary.

| Pattern | Accepted strings | Rejected strings |
| --- | --- | --- |
| `\Acat\z` | `"cat"` | `"cat\n"`, `"a cat"`, `""` |
| `\bcat\b` | `"cat"` | `"cats"`, `"cat!"`, `""` |
| Empty pattern | `""` | `"a"`, `"\n"` |

These rows still use our whole-string wrapper. Without it, searching with `\bcat\b` also finds `"cat"` inside `"a cat!"`.

`^` and `$` normally refer to the beginning and end of input, but [multi-line mode](https://docs.rs/regex/1.12.2/regex/#grouping-and-flags) makes them refer to line boundaries too. `\A` and `\z` keep their input-boundary meaning, which is why we use them for membership checks.

**Checkpoint.** Does `\A` consume the first character?

Answer: no. It checks the position before it.

## Flags

Flags change interpretation. Rust's [flag syntax](https://docs.rs/regex/1.12.2/regex/#grouping-and-flags) includes `i` for case-insensitive matching, `s` to let dot match newline, `m` for line anchors, and `x` for insignificant whitespace and comments. Unicode (`u`) is enabled by default.

Scoped forms such as `(?i:cat)` change only the enclosed group.

| Pattern | Accepted strings | Rejected strings |
| --- | --- | --- |
| `(?i:cat)` | `"cat"`, `"CAT"`, `"Cat"` | `"cats"`, `""` |
| `(?s:.)` | `"a"`, `"\n"` | `""`, `"ab"` |
| `(?x:a b)` | `"ab"` | `"a b"`, `""` |

In verbose mode, whitespace is ignored even inside classes. An intended literal space must be represented explicitly, for example by `\x20`.

**Checkpoint.** Does `(?x:a b)` require a space in the input?

Answer: no. The space helps format the pattern; it is not matched.

## Greedy and lazy matching

Greedy repetition prefers more repetitions; lazy repetition, such as `+?`, prefers fewer. Rust documents both in its [repetition rules](https://docs.rs/regex/1.12.2/regex/#repetitions). Preference concerns which match a search returns, not just yes-or-no membership.

This example deliberately uses **substring search**, unlike the tables:

```rust
use regex::Regex;

fn main() {
    let greedy = Regex::new(r"a+").unwrap();
    let lazy = Regex::new(r"a+?").unwrap();
    assert_eq!(greedy.find("aaa").unwrap().as_str(), "aaa");
    assert_eq!(lazy.find("aaa").unwrap().as_str(), "a");
}
```

When used alone in our whole-string wrapper, both `a+` and `a+?` accept `"aaa"`: the end anchor requires consuming the entire input. This is a deduction from the preference and anchor rules, not a claim that every search API produces the same result.

**Checkpoint.** Does lazy `a+?` mean "only one a is allowed"?

Answer: no. It changes preference, not the permitted repetition counts.

## Capturing groups

A capture records part of a match. `(ab)` captures by number, while `(?<name>ab)` gives it a name. `(?:ab)` only groups. See Rust's [group syntax](https://docs.rs/regex/1.12.2/regex/#grouping-and-flags).

```rust
use regex::Regex;

fn main() {
    let re = Regex::new(r"\A(?<letter>[ab])(?<digit>[0-9])\z").unwrap();
    let captures = re.captures("a7").unwrap();
    assert_eq!(&captures["letter"], "a");
    assert_eq!(&captures["digit"], "7");
    assert!(re.captures("a77").is_none());
}
```

For this example, capturing and non-capturing versions accept the same strings. Captures add extracted information, not a new membership condition. They do not enable backreferences, which the [crate overview](https://docs.rs/regex/1.12.2/regex/) says are unsupported. Look-around is also outside this engine's syntax.

**Checkpoint.** Does naming the digit group make it match the group name itself?

Answer: no. It still matches the enclosed `[0-9]` pattern.

## Putting the pieces together

Consider a small label format: one or more lowercase ASCII letters, then a hyphen, then exactly two ASCII digits.

| Pattern | Accepted strings | Rejected strings |
| --- | --- | --- |
| `[a-z]+-[0-9]{2}` | `"a-00"`, `"cat-42"` | `"-42"`, `"Cat-42"`, `"cat-4"`, `"cat-042"`, `"cat-٣٤"`, `""` |

The letter class chooses each letter, `+` repeats it, concatenation places the literal hyphen next, and `{2}` requires two digits. The whole-string wrapper excludes extra text. This is a deduction from the class, concatenation, and repetition rules above.

This checks a textual format. It does not turn a string into a number or define a type in our proposed language.

**Checkpoint.** Why reject `"cat-٣٤"` even though its ending contains two digits?

Answer: our rule specifies ASCII digits, and `[0-9]` expresses that restriction.

Next: [review this draft](review.html).
