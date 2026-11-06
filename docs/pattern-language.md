# Our first pattern language

The [strings lesson](regex-introduction.html) gave us the question: does a complete string belong to the set a pattern describes? We can now choose notation for asking it without learning a particular regex engine first.

This page proposes a small notation for our language. It is a documentation design, not an implemented compiler or a finished programming language. The fixed requirement is **whole-string acceptance**. The particular symbols below are a proposal for review.

## Start with a literal

A string between backticks is a pattern that accepts exactly that string:

```text
`cat`
```

Its allowed set is `{"cat"}`. It accepts `"cat"` and rejects `"cats"`, `"a cat"`, and `""`. The backticks delimit the pattern literal; they are not characters required in the input. We keep double quotes for example string values, so <code>&#96;cat&#96;</code> is the pattern and `"cat"` is its accepted value.

This is the starting rule: a literal value describes the singleton set containing that value. There is no separate regex string inside it. For example, <code>&#96;a+b&#96;</code> accepts the literal text `a+b`; the plus inside the delimiters is not an instruction to repeat anything.

The literal-and-operation approach is inspired by [Pomsky's strings](https://pomsky-lang.org/docs/language-tour/strings/), but backticks are our preferred spelling. They visually distinguish pattern literals from the example values and external syntaxes in these lessons.

We borrow the delimiter, not [JavaScript's template-literal behavior](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals). Our first draft has no interpolation: <code>&#96;${name}&#96;</code> describes the literal string `"${name}"`, not a variable lookup. How to include a backtick or represent control characters remains an explicit [escaping question](open-design-questions.html#what-notation-expresses-the-operations).

**Checkpoint.** Does <code>&#96;a+b&#96;</code> accept `"aaab"`?

Answer: no. The plus is literal text, not repetition syntax.

## Add parts to describe more values

Here is the proposed vocabulary. The next lesson explains each operation with accepted and rejected values.

| Purpose | Proposed notation | Meaning |
| --- | --- | --- |
| Literal | <code>&#96;cat&#96;</code> | Exactly the string `"cat"` |
| Empty string | <code>&#96;&#96;</code> | Exactly the zero-character string |
| Alternatives | <code>&#96;a&#96; &#124; &#96;b&#96;</code> | Either complete string, here one character each |
| Character range | <code>[&#96;0&#96;-&#96;9&#96;]</code> | One ASCII digit, including both endpoints |
| Join parts | <code>&#96;cat&#96; &#96;s&#96;</code> | The first part followed by the second |
| Longer alternatives | <code>&#96;cat&#96; &#124; &#96;dog&#96;</code> | The same choice operation, applied to words |
| Grouping | <code>(&#96;cat&#96; &#124; &#96;dog&#96;) &#96;s&#96;</code> | Join `"s"` to either alternative |
| Optional | <code>&#96;a&#96;?</code> | Zero or one copy of the preceding part |
| Repetition | <code>&#96;a&#96;&#42;</code>, <code>&#96;a&#96;+</code> | Zero or more, or one or more copies |
| Counted repetition | <code>&#96;a&#96;{2}</code>, <code>&#96;a&#96;{2,3}</code>, <code>&#96;a&#96;{2,}</code> | Exactly two, two through three, or at least two copies |

Whitespace outside literals separates notation and contributes no input characters. <code>&#96;cat&#96; &#96;s&#96;</code> accepts `"cats"`, not `"cat s"`. A required space is written inside a literal, as in <code>&#96;cat&#96; &#96; &#96; &#96;dog&#96;</code>.

A postfix repetition operator applies to the preceding literal, character range, or parenthesized group. Thus <code>&#96;ab&#96;&#42;</code> repeats the entire string `ab`, while <code>&#96;a&#96; &#96;b&#96;&#42;</code> repeats only `b`. Repetition binds before joining, and joining binds before alternatives. Parentheses can make that order explicit. Grouping does not extract a capture.

We borrow familiar notation from Pomsky's [alternatives and grouping](https://pomsky-lang.org/docs/language-tour/alternations/), [character ranges](https://pomsky-lang.org/docs/language-tour/character-sets/#character-ranges), and [repetition](https://pomsky-lang.org/docs/language-tour/repetitions/). The meanings in this draft are defined here and in [building patterns from sets](regex-building-blocks.html), not inherited wholesale from another system.

Use `|` as the preferred explicit choice notation, whether the alternatives are characters, words, or larger patterns. The lessons use square brackets for character ranges, with one character at each endpoint. To combine ranges, prefer <code>[&#96;a&#96;-&#96;z&#96;] &#124; [&#96;A&#96;-&#96;Z&#96;]</code>. This teaching convention does not rule out optional bracketed choice shorthand later; its exact form and semantics remain [open](open-design-questions.html#what-notation-expresses-the-operations). The core examples do not require it. In the core notation, adjacency means joining parts, not choosing between them.

**Checkpoint.** Which pattern requires a space: <code>&#96;a&#96; &#96;b&#96;</code> or <code>&#96;a b&#96;</code>?

Answer: <code>&#96;a b&#96;</code>. The other pattern accepts `"ab"`.

## Always check the complete input

Every pattern on the main teaching path is fully consuming. The question is whether the pattern accepts the input from start to end, with nothing left over. Authors do not add anchors or opt into a validation mode.

| Pattern | Input | Accepted? |
| --- | --- | --- |
| <code>&#96;cat&#96;</code> | `"cat"` | Yes |
| <code>&#96;cat&#96;</code> | `"a cat"` | No |
| <code>&#96;cat&#96;</code> | `"cats"` | No |
| <code>&#96;cat&#96;</code> | `"cat\n"` | No |
| <code>&#96;&#96;</code> | `""` | Yes |
| <code>&#96;&#96;</code> | `"cat"` | No |

In input examples, `\n` denotes a line feed. This is a display convention for values, not a decision about escape syntax in our language. No whitespace is trimmed and no case conversion is implicit. Whether a particular external API defaults to substring search is a separate translation concern.

**Checkpoint.** Should a reader write start and end assertions to make <code>&#96;cat&#96;</code> reject `"cats"`?

Answer: no. Whole-string acceptance is already the language rule.

## Keep the first version small

The first draft describes string sets with literals, alternatives, character ranges, joining, grouping, and repetition. Examples use finite Unicode scalar-value strings as their explicit teaching universe. The final character model and encoding remain [open questions](open-design-questions.html#what-values-do-constraints-describe); the basic examples use ASCII so they do not depend on those choices.

Variables, named fragments, captures, search preferences, flags, and engine-specific extensions are outside this first draft. Letters such as A and B in mathematical explanations name sets in the prose; they are not variable syntax in the language. We also leave literal escaping, broader character ranges, and notation for further set operations open rather than importing another system's rules silently.

[Supplemental translations](regex-translations.html) show how selected examples can be expressed with existing tools. They are optional and do not define our language. Successful tests of those translations are evidence about the examples, not execution of this proposed notation.

**Checkpoint.** Do we need variables before we can describe a label with letters, a hyphen, and two digits?

Answer: no. We can write those parts directly and join them.

Next: [building patterns from sets](regex-building-blocks.html).
