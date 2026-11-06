# Building patterns from sets

Read [our first pattern language](pattern-language.html) first. This lesson uses that proposed notation throughout. We start with small string sets and add operations that build larger ones. Every pattern accepts or rejects a complete input; no anchors are needed.

The examples are deductions from our proposed rules, not executable language tests. Existing tools appear only in the optional [translation companion](regex-translations.html). Mathematical set names and equations explain the patterns; they are not extra language syntax.

## Literals describe one value

A literal string describes one string. `"cat"` describes `{"cat"}`, and `"a"` describes `{"a"}`. The rule is the same whether the literal has one character or several.

| Pattern | Accepted strings | Rejected strings |
| --- | --- | --- |
| `"cat"` | `"cat"` | `"Cat"`, `"cats"`, `""` |
| `"a"` | `"a"` | `"b"`, `"aa"`, `""` |
| `"a+b"` | `"a+b"` | `"ab"`, `"aaab"`, `""` |

Operator characters inside a literal stand for themselves. We do not need regex escapes to write `"."` or `"a+b"`. Escaping quotes and backslashes is a separate [open notation question](open-design-questions.html#what-notation-expresses-the-operations).

**Checkpoint.** Does `"a+b"` permit several copies of `a` followed by `b`?

Answer: no. The plus is literal text inside the quotes.

## Alternatives add members

The bar `|` means "or." Either alternative can supply the complete string. This implements the [union operation](set-operations.html#union) from the set lesson:

```text
"a" | "b" | "c"
```

The allowed set is `{"a", "b", "c"}`. This is how we list character choices; we do not introduce a separate bracketed list syntax. The same operator works for longer strings:

```text
"cat" | "dog"
```

Here the allowed set is `{"cat", "dog"}`. Alternatives need not have equal lengths. For example, `"a" | "cat"` accepts either of those two strings. The length of each accepted value comes from its alternative, not from the bar itself.

| Pattern | Accepted strings | Rejected strings |
| --- | --- | --- |
| <code>&quot;a&quot; &#124; &quot;b&quot;</code> | `"a"`, `"b"` | `"ab"`, `"c"`, `""` |
| <code>&quot;a&quot; &#124; &quot;b&quot; &#124; &quot;c&quot;</code> | `"a"`, `"b"`, `"c"` | `"ab"`, `"d"`, `""` |
| <code>&quot;cat&quot; &#124; &quot;dog&quot;</code> | `"cat"`, `"dog"` | `"catdog"`, `"cow"`, `""` |
| <code>&quot;a&quot; &#124; &quot;cat&quot;</code> | `"a"`, `"cat"` | `"acat"`, `"c"`, `""` |

```math
L(p \mid q) = L(p) \cup L(q)
```

In the equation, p and q stand for patterns in the explanation. This is not variable syntax. The equation is a deduction: accepting either pattern means membership in the union of their allowed sets. Repeating an alternative does not add a new member, so `"a" | "a"` still describes just `{"a"}`. Parentheses group alternatives into one part, as in `("a" | "b")`; they do not change its allowed set by themselves.

**Checkpoint.** Does `"a" | "b"` accept the complete string `"ab"`?

Answer: no. It accepts one alternative, not both joined together.

## Character ranges abbreviate consecutive choices

Listing all ten ASCII digits with bars is repetitive. A character range is a shorter way to describe consecutive one-character choices:

```text
["0"-"9"]
```

A range includes both endpoints and selects exactly one character. `["a"-"c"]` describes the same set as `"a" | "b" | "c"`. It does not describe an integer interval or a sequence of several digits.

In this draft, brackets enclose only one range with a single character at each endpoint. They are not general character classes or choice lists. Use alternatives outside the brackets to combine ranges, such as `["a"-"z"] | ["A"-"Z"]`, rather than putting several ranges or individual choices inside one pair of brackets. These examples use ASCII ordering; broader range semantics remain an [open question](open-design-questions.html#what-notation-expresses-the-operations).

| Pattern | Accepted strings | Rejected strings |
| --- | --- | --- |
| `["a"-"c"]` | `"a"`, `"b"`, `"c"` | `"A"`, `"d"`, `""` |
| `["0"-"9"]` | `"0"`, `"9"` | `"10"`, `"٣"`, `""` |
| <code>[&quot;a&quot;-&quot;z&quot;] &#124; [&quot;A&quot;-&quot;Z&quot;]</code> | `"a"`, `"z"`, `"A"`, `"Z"` | `"aA"`, `"0"`, `""` |

**Checkpoint.** Does `["0"-"9"]` accept the two-character string `"10"`?

Answer: no. It chooses exactly one character. To list nonconsecutive choices, use `|` rather than brackets.

## Empty string and joining choices

The empty string ε has zero characters. The pattern `""` describes the singleton set `{ε}`. It is not the empty set ∅, which has no members. This draft does not yet give the empty set a pattern spelling.

Concatenation joins one string from each set in order. If A = `{"a", "b"}` and B = `{"0", "1"}`, then AB = `{"a0", "a1", "b0", "b1"}`. This is not a Cartesian product of pairs.

```math
AB = \{uv \mid u \in A, v \in B\}
```

Writing patterns next to each other joins them: `"a" "b"` describes `{"ab"}`, while `"b" "a"` describes `{"ba"}`. With grouped alternatives, `("a" | "b") ("0" | "1")` describes the four strings in AB above. The separating space is notation, not a required input character.

Parentheses make each choice one part. For example, `"a" ("b" | "c") "d"` joins `a`, either `b` or `c`, then `d`. Joining binds before alternatives, so `"a" | "b" "c"` means either `"a"` or `"bc"`. Write `("a" | "b") "c"` to require the final `c` after either choice.

| Pattern | Accepted strings | Rejected strings |
| --- | --- | --- |
| `""` | `""` | `"a"`, `" "` |
| `"a" "b"` | `"ab"` | `"a b"`, `"ba"`, `""` |
| <code>(&quot;a&quot; &#124; &quot;b&quot;) (&quot;0&quot; &#124; &quot;1&quot;)</code> | `"a0"`, `"a1"`, `"b0"`, `"b1"` | `"0a"`, `"a"`, `""` |
| <code>&quot;a&quot; (&quot;b&quot; &#124; &quot;c&quot;) &quot;d&quot;</code> | `"abd"`, `"acd"` | `"ab"`, `"ad"`, `""` |
| <code>&quot;a&quot; &#124; &quot;b&quot; &quot;c&quot;</code> | `"a"`, `"bc"` | `"ac"`, `"b"`, `""` |
| <code>(&quot;a&quot; &#124; &quot;b&quot;) &quot;c&quot;</code> | `"ac"`, `"bc"` | `"a"`, `"b"`, `""` |

**Checkpoint.** What does concatenating a set A with `{ε}` do?

Answer: it leaves A unchanged, because joining the empty string adds no characters.

## Repetition: finite and unbounded counts

A repetition operator, also called a quantifier, applies to the preceding literal, character range, or group. Counts are nonnegative whole numbers; a bounded range includes both endpoints and requires its lower bound to be no greater than its upper bound. Unbounded repetition still produces only finite strings.

For a set A of strings, A+ joins one or more choices from A. Each copy makes its own choice; it need not repeat the same selected member:

```math
A^+ = A \cup AA \cup AAA \cup \cdots
```

| Pattern | Count | Accepted strings | Rejected strings |
| --- | --- | --- | --- |
| `"a"?` | Zero or one | `""`, `"a"` | `"aa"`, `"b"` |
| `"a"*` | Zero or more | `""`, `"a"`, `"aaa"` | `"b"`, `"ab"` |
| `"a"+` | One or more | `"a"`, `"aaa"` | `""`, `"b"` |
| `"a"{0}` | Exactly zero | `""` | `"a"` |
| `"a"{2}` | Exactly two | `"aa"` | `"a"`, `"aaa"` |
| `"a"{2,3}` | Two or three | `"aa"`, `"aaa"` | `"a"`, `"aaaa"` |
| `"a"{2,}` | At least two | `"aa"`, `"aaaa"` | `"a"`, `""` |
| `"a" "b"*` | One `a`, then zero or more `b`s | `"a"`, `"ab"`, `"abbb"` | `""`, `"abab"` |
| `"ab"*` | Zero or more copies of `ab` | `""`, `"ab"`, `"abab"` | `"a"`, `"aba"` |
| <code>(&quot;a&quot; &#124; &quot;b&quot;){2}</code> | Two independent choices between `a` and `b` | `"aa"`, `"ab"`, `"ba"`, `"bb"` | `"a"`, `"abc"`, `""` |

For a set A of strings, A* contains every finite concatenation of members of A, including zero copies. Zero copies produce ε. This is different from the power set, which contains subsets.

The entire quoted literal is one part. Thus `"ab"*` and `("a" "b")*` have the same meaning, unlike `"a" "b"*`. Repeating `""` any permitted number of times still produces only `""`; different construction choices do not create distinct values.

**Checkpoint.** Does `"ab"*` accept `"a"`? Does `"a" "b"*`?

Answer: the first does not; the second does, by choosing zero copies of `b`.

## A complete example

Suppose a label contains one or more lowercase ASCII letters, a hyphen, and exactly two ASCII digits. In our proposed notation:

```text
["a"-"z"]+ "-" ["0"-"9"]{2}
```

Read the parts in order: choose a letter at least once, require the literal hyphen, and choose a digit exactly twice. No variables or named fragments are needed.

In mathematical discussion, let A be the set of one-character strings from `"a"` through `"z"`, H be `{"-"}`, and D be the set of one-character ASCII digit strings. The language is:

```math
A^+ H D D
```

| Accepted strings | Rejected strings |
| --- | --- |
| `"a-00"`, `"cat-42"` | `"-42"`, `"Cat-42"`, `"cat-4"`, `"cat-042"`, `"cat-٣٤"`, `""` |

The explicit digit range excludes non-ASCII digits. Whole-string acceptance rejects extra text before or after the label, including a trailing line feed. The [translation companion](regex-translations.html#a-label-in-existing-tools) shows external spellings of this rule without making them prerequisites.

**Checkpoint.** Why does `"cat-042"` fail?

Answer: the rule requires exactly two digits after the hyphen.

## Beyond the first building blocks

We have used singleton sets, joining, union, and finite repetition. Earlier [set operations](set-operations.html) also included intersection, difference, complement, and symmetric difference. Knowing those mathematical operations does not yet give them language syntax.

For instance, intersecting `{"a", "b", "c"}` with `{"b", "c", "d"}` gives `{"b", "c"}` by the [intersection definition](set-operations.html#intersection). Whether to give that operation notation for whole string sets or a restricted one-character case remains an [open design question](open-design-questions.html#what-notation-expresses-the-operations). It does not add operations inside range brackets. Variables and type relationships can wait until the small pattern vocabulary is clear.

**Checkpoint.** Have we given every set operation a pattern operator?

Answer: no. A mathematical operation and a proposed language feature are different things.

Next: [cardinality and mappings](cardinality-and-mappings.html), including why `"a"+` and `"a"+ "b"+` both describe countably infinite sets.
