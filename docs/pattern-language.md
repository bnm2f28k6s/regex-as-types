# Our first pattern language

The [strings lesson](regex-introduction.html) gave us the question: does a complete string belong to the set a pattern describes? We can now choose notation for asking it without learning a particular regex engine first.

This page proposes a small notation for our language. It is a documentation design, not an implemented compiler or a finished programming language. The fixed requirement is **whole-string acceptance**. The particular symbols below are a proposal for review.

## Start with a literal

A quoted string is itself a pattern that accepts exactly that string:

```text
"cat"
```

Its allowed set is `{"cat"}`. It accepts `"cat"` and rejects `"cats"`, `"a cat"`, and `""`. The quotes delimit the literal in the pattern; they are not characters required in the input.

This is the starting rule: a literal value describes the singleton set containing that value. There is no separate regex string inside it. For example, `"a+b"` accepts the literal text `a+b`; the plus inside quotes is not an instruction to repeat anything.

The quoted-literal approach is inspired by [Pomsky's strings](https://pomsky-lang.org/docs/language-tour/strings/). That is a source of notation ideas, not a requirement to adopt Pomsky's other features or matching behavior.

**Checkpoint.** Does `"a+b"` accept `"aaab"`?

Answer: no. Everything inside these quotes is literal text.

## Add parts to describe more values

Here is the proposed vocabulary. The next lesson explains each operation with accepted and rejected values.

| Purpose | Proposed notation | Meaning |
| --- | --- | --- |
| Literal | `"cat"` | Exactly the string `"cat"` |
| Empty string | `""` | Exactly the zero-character string |
| One-character choice | `["a" "b"]` | One character, either `a` or `b` |
| Character range | `["0"-"9"]` | One ASCII digit, including both endpoints |
| Join parts | `"cat" "s"` | The first part followed by the second |
| Alternatives | <code>&quot;cat&quot; &#124; &quot;dog&quot;</code> | Either complete string |
| Grouping | <code>(&quot;cat&quot; &#124; &quot;dog&quot;) &quot;s&quot;</code> | Join `"s"` to either alternative |
| Optional | `"a"?` | Zero or one copy of the preceding part |
| Repetition | `"a"*`, `"a"+` | Zero or more, or one or more copies |
| Counted repetition | `"a"{2}`, `"a"{2,3}`, `"a"{2,}` | Exactly two, two through three, or at least two copies |

Whitespace outside literals separates notation and contributes no input characters. `"cat" "s"` accepts `"cats"`, not `"cat s"`. A required space is written inside a literal, as in `"cat" " " "dog"`.

A postfix repetition operator applies to the preceding literal, character choice, or parenthesized group. Thus `"ab"*` repeats the entire string `ab`, while `"a" "b"*` repeats only `b`. Repetition binds before joining, and joining binds before alternatives. Parentheses can make that order explicit. Grouping does not extract a capture.

We borrow familiar notation from Pomsky's [alternatives and grouping](https://pomsky-lang.org/docs/language-tour/alternations/), [character sets](https://pomsky-lang.org/docs/language-tour/character-sets/), and [repetition](https://pomsky-lang.org/docs/language-tour/repetitions/). The meanings in this draft are defined here and in [building patterns from sets](regex-building-blocks.html), not inherited wholesale from another system. For now, character choices list one-character literals and ranges; compact forms such as `["ab"]` are not proposed.

**Checkpoint.** Which pattern requires a space: `"a" "b"` or `"a b"`?

Answer: `"a b"`. The other pattern accepts `"ab"`.

## Always check the complete input

Every pattern on the main teaching path is fully consuming. The question is whether the pattern accepts the input from start to end, with nothing left over. Authors do not add anchors or opt into a validation mode.

| Pattern | Input | Accepted? |
| --- | --- | --- |
| `"cat"` | `"cat"` | Yes |
| `"cat"` | `"a cat"` | No |
| `"cat"` | `"cats"` | No |
| `"cat"` | `"cat\n"` | No |
| `""` | `""` | Yes |
| `""` | `"cat"` | No |

In input examples, `\n` denotes a line feed. This is a display convention for values, not a decision about escape syntax in our language. No whitespace is trimmed and no case conversion is implicit. Whether a particular external API defaults to substring search is a separate translation concern.

**Checkpoint.** Should a reader write start and end assertions to make `"cat"` reject `"cats"`?

Answer: no. Whole-string acceptance is already the language rule.

## Keep the first version small

The first draft describes string sets with literals, character choices, joining, alternatives, grouping, and repetition. Examples use finite Unicode scalar-value strings as their explicit teaching universe. The final character model and encoding remain [open questions](open-design-questions.html#what-values-do-constraints-describe); the basic examples use ASCII so they do not depend on those choices.

Variables, named fragments, captures, search preferences, flags, and engine-specific extensions are outside this first draft. Letters such as A and B in mathematical explanations name sets in the prose; they are not variable syntax in the language. We also leave literal escaping, broader character ranges, and notation for further set operations open rather than importing another system's rules silently.

[Supplemental translations](regex-translations.html) show how selected examples can be expressed with existing tools. They are optional and do not define our language. Successful tests of those translations are evidence about the examples, not execution of this proposed notation.

**Checkpoint.** Do we need variables before we can describe a label with letters, a hyphen, and two digits?

Answer: no. We can write those parts directly and join them.

Next: [building patterns from sets](regex-building-blocks.html).
