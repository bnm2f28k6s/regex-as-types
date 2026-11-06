# Building patterns from sets

Read [our first pattern language](pattern-language.html) first. This lesson uses that proposed notation throughout. We start with small string sets and add operations that build larger ones. Every pattern accepts or rejects a complete input; no anchors are needed.

The examples are deductions from our proposed rules, not executable language tests. Existing tools appear only in the optional [translation companion](regex-translations.html). Mathematical set names and equations explain the patterns; they are not extra language syntax.

## Literals describe one value

A literal string describes one string. <code>&#96;cat&#96;</code> describes `{"cat"}`, and <code>&#96;a&#96;</code> describes `{"a"}`. Backticks mark pattern literals; double quotes mark example values. The rule is the same whether the literal has one character or several.

| Pattern | Accepted strings | Rejected strings |
| --- | --- | --- |
| <code>&#96;cat&#96;</code> | `"cat"` | `"Cat"`, `"cats"`, `""` |
| <code>&#96;a&#96;</code> | `"a"` | `"b"`, `"aa"`, `""` |
| <code>&#96;a+b&#96;</code> | `"a+b"` | `"ab"`, `"aaab"`, `""` |
| <code>&#96;${name}&#96;</code> | `"${name}"` | `"name"`, `"cat"`, `""` |

Operator characters inside a literal stand for themselves. We do not need regex escapes to write <code>&#96;.&#96;</code> or <code>&#96;a+b&#96;</code>. There is no interpolation in this draft, so `${name}` is literal text too. Escaping backticks, backslashes, and control characters is a separate [open notation question](open-design-questions.html#what-notation-expresses-the-operations).

**Checkpoint.** Does <code>&#96;a+b&#96;</code> permit several copies of `a` followed by `b`?

Answer: no. The plus is literal text inside the backticks.

## Alternatives add members

The bar `|` means "or." Either alternative can supply the complete string. This implements the [union operation](set-operations.html#union) from the set lesson:

```text
`a` | `b` | `c`
```

The allowed set is `{"a", "b", "c"}`. This is the preferred way to list character choices in the lessons. Optional bracketed choice shorthand remains an open design possibility, not a prerequisite or a prohibited feature. The same bar operator works for longer strings:

```text
`cat` | `dog`
```

Here the allowed set is `{"cat", "dog"}`. Alternatives need not have equal lengths. For example, <code>&#96;a&#96; &#124; &#96;cat&#96;</code> accepts either of those two strings. The length of each accepted value comes from its alternative, not from the bar itself.

| Pattern | Accepted strings | Rejected strings |
| --- | --- | --- |
| <code>&#96;a&#96; &#124; &#96;b&#96;</code> | `"a"`, `"b"` | `"ab"`, `"c"`, `""` |
| <code>&#96;a&#96; &#124; &#96;b&#96; &#124; &#96;c&#96;</code> | `"a"`, `"b"`, `"c"` | `"ab"`, `"d"`, `""` |
| <code>&#96;cat&#96; &#124; &#96;dog&#96;</code> | `"cat"`, `"dog"` | `"catdog"`, `"cow"`, `""` |
| <code>&#96;a&#96; &#124; &#96;cat&#96;</code> | `"a"`, `"cat"` | `"acat"`, `"c"`, `""` |

```math
L(p \mid q) = L(p) \cup L(q)
```

In the equation, p and q stand for patterns in the explanation. This is not variable syntax. The equation is a deduction: accepting either pattern means membership in the union of their allowed sets. Repeating an alternative does not add a new member, so <code>&#96;a&#96; &#124; &#96;a&#96;</code> still describes just `{"a"}`. Parentheses group alternatives into one part, as in <code>(&#96;a&#96; &#124; &#96;b&#96;)</code>; they do not change its allowed set by themselves.

**Checkpoint.** Does <code>&#96;a&#96; &#124; &#96;b&#96;</code> accept the complete string `"ab"`?

Answer: no. It accepts one alternative, not both joined together.

## Character ranges abbreviate consecutive choices

Listing all ten ASCII digits with bars is repetitive. A character range is a shorter way to describe consecutive one-character choices:

```text
[`0`-`9`]
```

A range includes both endpoints and selects exactly one character. <code>[&#96;a&#96;-&#96;c&#96;]</code> describes the same set as <code>&#96;a&#96; &#124; &#96;b&#96; &#124; &#96;c&#96;</code>. A character range does not describe an integer interval or a sequence of several digits.

In the core examples, brackets enclose a range with a single character at each endpoint. To combine ranges, prefer alternatives outside the brackets, such as <code>[&#96;a&#96;-&#96;z&#96;] &#124; [&#96;A&#96;-&#96;Z&#96;]</code>. This does not settle whether optional bracketed shorthand could also list choices or combine ranges. Its rules and broader range semantics remain [open questions](open-design-questions.html#what-notation-expresses-the-operations). These examples use ASCII ordering.

| Pattern | Accepted strings | Rejected strings |
| --- | --- | --- |
| <code>[&#96;a&#96;-&#96;c&#96;]</code> | `"a"`, `"b"`, `"c"` | `"A"`, `"d"`, `""` |
| <code>[&#96;0&#96;-&#96;9&#96;]</code> | `"0"`, `"9"` | `"10"`, `"٣"`, `""` |
| <code>[&#96;a&#96;-&#96;z&#96;] &#124; [&#96;A&#96;-&#96;Z&#96;]</code> | `"a"`, `"z"`, `"A"`, `"Z"` | `"aA"`, `"0"`, `""` |

**Checkpoint.** Does <code>[&#96;0&#96;-&#96;9&#96;]</code> accept the two-character string `"10"`?

Answer: no. It chooses exactly one character. To list nonconsecutive choices, the lessons prefer `|`.

## Empty string and joining choices

The empty string ε has zero characters. The pattern <code>&#96;&#96;</code>, two adjacent backticks with no content, describes the singleton set `{ε}`. It is not the empty set ∅, which has no members. This draft does not yet give the empty set a pattern spelling.

Concatenation joins one string from each set in order. If A = `{"a", "b"}` and B = `{"0", "1"}`, then AB = `{"a0", "a1", "b0", "b1"}`. This is not a Cartesian product of pairs.

```math
AB = \{uv \mid u \in A, v \in B\}
```

Writing patterns next to each other joins them: <code>&#96;a&#96; &#96;b&#96;</code> describes `{"ab"}`, while <code>&#96;b&#96; &#96;a&#96;</code> describes `{"ba"}`. With grouped alternatives, <code>(&#96;a&#96; &#124; &#96;b&#96;) (&#96;0&#96; &#124; &#96;1&#96;)</code> describes the four strings in AB above. The separating space is notation, not a required input character.

Parentheses make each choice one part. For example, <code>&#96;a&#96; (&#96;b&#96; &#124; &#96;c&#96;) &#96;d&#96;</code> joins `a`, either `b` or `c`, then `d`. Joining binds before alternatives, so <code>&#96;a&#96; &#124; &#96;b&#96; &#96;c&#96;</code> means either `"a"` or `"bc"`. Write <code>(&#96;a&#96; &#124; &#96;b&#96;) &#96;c&#96;</code> to require the final `c` after either choice.

| Pattern | Accepted strings | Rejected strings |
| --- | --- | --- |
| <code>&#96;&#96;</code> | `""` | `"a"`, `" "` |
| <code>&#96;a&#96; &#96;b&#96;</code> | `"ab"` | `"a b"`, `"ba"`, `""` |
| <code>(&#96;a&#96; &#124; &#96;b&#96;) (&#96;0&#96; &#124; &#96;1&#96;)</code> | `"a0"`, `"a1"`, `"b0"`, `"b1"` | `"0a"`, `"a"`, `""` |
| <code>&#96;a&#96; (&#96;b&#96; &#124; &#96;c&#96;) &#96;d&#96;</code> | `"abd"`, `"acd"` | `"ab"`, `"ad"`, `""` |
| <code>&#96;a&#96; &#124; &#96;b&#96; &#96;c&#96;</code> | `"a"`, `"bc"` | `"ac"`, `"b"`, `""` |
| <code>(&#96;a&#96; &#124; &#96;b&#96;) &#96;c&#96;</code> | `"ac"`, `"bc"` | `"a"`, `"b"`, `""` |

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
| <code>&#96;a&#96;?</code> | Zero or one | `""`, `"a"` | `"aa"`, `"b"` |
| <code>&#96;a&#96;&#42;</code> | Zero or more | `""`, `"a"`, `"aaa"` | `"b"`, `"ab"` |
| <code>&#96;a&#96;+</code> | One or more | `"a"`, `"aaa"` | `""`, `"b"` |
| <code>&#96;a&#96;{0}</code> | Exactly zero | `""` | `"a"` |
| <code>&#96;a&#96;{2}</code> | Exactly two | `"aa"` | `"a"`, `"aaa"` |
| <code>&#96;a&#96;{2,3}</code> | Two or three | `"aa"`, `"aaa"` | `"a"`, `"aaaa"` |
| <code>&#96;a&#96;{2,}</code> | At least two | `"aa"`, `"aaaa"` | `"a"`, `""` |
| <code>&#96;a&#96; &#96;b&#96;&#42;</code> | One `a`, then zero or more `b`s | `"a"`, `"ab"`, `"abbb"` | `""`, `"abab"` |
| <code>&#96;ab&#96;&#42;</code> | Zero or more copies of `ab` | `""`, `"ab"`, `"abab"` | `"a"`, `"aba"` |
| <code>(&#96;a&#96; &#124; &#96;b&#96;){2}</code> | Two independent choices between `a` and `b` | `"aa"`, `"ab"`, `"ba"`, `"bb"` | `"a"`, `"abc"`, `""` |

For a set A of strings, A* contains every finite concatenation of members of A, including zero copies. Zero copies produce ε. This is different from the power set, which contains subsets.

The entire backtick-delimited literal is one part. Thus <code>&#96;ab&#96;&#42;</code> and <code>(&#96;a&#96; &#96;b&#96;)&#42;</code> have the same meaning, unlike <code>&#96;a&#96; &#96;b&#96;&#42;</code>. Repeating <code>&#96;&#96;</code> any permitted number of times still produces only `""`; different construction choices do not create distinct values.

**Checkpoint.** Does <code>&#96;ab&#96;&#42;</code> accept `"a"`? Does <code>&#96;a&#96; &#96;b&#96;&#42;</code>?

Answer: the first does not; the second does, by choosing zero copies of `b`.

## A complete example

Suppose a label contains one or more lowercase ASCII letters, a hyphen, and exactly two ASCII digits. In our proposed notation:

```text
[`a`-`z`]+ `-` [`0`-`9`]{2}
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

For instance, intersecting `{"a", "b", "c"}` with `{"b", "c", "d"}` gives `{"b", "c"}` by the [intersection definition](set-operations.html#intersection). Whether to give that operation notation for whole string sets or a restricted one-character case remains an [open design question](open-design-questions.html#what-notation-expresses-the-operations). Neither bracketed choice shorthand nor set operations inside brackets are required by these lessons; their possible designs remain separate questions. Variables and type relationships can wait until the small pattern vocabulary is clear.

**Checkpoint.** Have we given every set operation a pattern operator?

Answer: no. A mathematical operation and a proposed language feature are different things.

Next: [cardinality and mappings](cardinality-and-mappings.html), including why <code>&#96;a&#96;+</code> and <code>&#96;a&#96;+ &#96;b&#96;+</code> both describe countably infinite sets.
