# Cardinality and mappings

The patterns `"a"+` and `"a"+ "b"+` both describe countably infinite sets. Yet the second has two independently chosen repetition counts, where the first has only one. How can they have the same size?

This lesson separates the number of distinct values from the structure of those values. Read [building patterns from sets](regex-building-blocks.html) first. We use our proposed notation, whole-string acceptance, and finite Unicode scalar-value strings as the teaching universe. Infinite sets here allow arbitrarily long finite strings; they do not assume a particular machine's storage limit. No engine syntax is required.

The definitions follow Oscar Levin's [functions lesson](https://discrete.openmathbooks.org/dmoi3/sec_intro-functions.html) and Richard Hammack's [*Book of Proof*, sections 14.1–14.3](https://richardhammack.github.io/BookOfProof/Main.pdf#page=281). The pattern examples, mappings, and counting arguments below are our worked deductions from those definitions and our proposed [set-building rules](regex-building-blocks.html). Mathematical names and functions in this lesson are not variable or function syntax for the language.

## Cardinality counts distinct members

The cardinality of a finite set is its number of distinct elements. Write it as `|A|`. This notation measures the set, not the length of its members. See Hammack's [introduction to cardinality](https://richardhammack.github.io/BookOfProof/Main.pdf#page=281).

For example:

- `|∅| = 0`.
- `|{""}| = 1`. An empty string is still one value.
- `|{"a", "aa", "aaa"}| = 3`, even though the strings have different lengths.
- `|L("a"{1,3})| = 3` under whole-string acceptance.

Different descriptions can name the same member. `"a" | "a"` still describes just `{"a"}`. Counting alternatives, repetition choices, or ways to match is not necessarily counting distinct strings.

**Checkpoint.** How many members does `{"ab", "ab", "ba"}` have?

Answer: two. Repeated entries do not add members.

## Functions map inputs to outputs

A function `f: X → Y` assigns exactly one output in Y to each input in X. X is its **domain**; Y is its **codomain**. Its **image**, written `f(X)`, is the set of outputs it actually produces. The image may be smaller than the codomain. These are Levin's [function definitions](https://discrete.openmathbooks.org/dmoi3/sec_intro-functions.html).

Take `X = {"a", "aa", "aaa"}` and `Y = {1, 2, 3, 4}`. Let f return a string's length:

| Input | Output |
| --- | --- |
| `"a"` | 1 |
| `"aa"` | 2 |
| `"aaa"` | 3 |

Then `f(X) = {1, 2, 3}`. The codomain permits `4`, but no input produces it. Different inputs may share an output in a function: mapping every member of X to `1` would also be a function, but would discard their differences.

**Checkpoint.** Is a rule that sends `"a"` to both `1` and `2` a function?

Answer: no. Each input must have exactly one output. A function can instead return a single pair such as `(1, 2)`, if pairs belong to its codomain.

## Equal cardinality means a bijection exists

Three properties describe how a function reaches its codomain:

- **Injective**, or one-to-one: different inputs never share an output.
- **Surjective**, or onto: every member of the codomain is an output.
- **Bijective**: both injective and surjective. Every member of the codomain is paired with exactly one input.

See Levin's [injections, surjections, and bijections](https://discrete.openmathbooks.org/dmoi3/sec_intro-functions.html#subsec_surj-inj-bij). The length function above is injective but not surjective onto `{1, 2, 3, 4}`. With codomain `{1, 2, 3}` instead, it is bijective.

Two sets have equal cardinality when there exists a bijection between them. This is the [definition for finite and infinite sets](https://richardhammack.github.io/BookOfProof/Main.pdf#page=281). One failed candidate mapping does not show that their cardinalities differ; another mapping might work.

Equal cardinality does not mean equal membership. `{"a", "b"}` and `{0, 1}` can be paired perfectly, but they are different sets.

**Checkpoint.** Does a function sending both `"a"` and `"b"` to `0` establish equal cardinality with `{0, 1}`?

Answer: no. It repeats `0` and misses `1`. The alternative mapping `"a" → 0`, `"b" → 1` is a bijection.

## Countably infinite sets can be listed

Write `N+ = {1, 2, 3, ...}` for the positive integers. A set is **countably infinite** if there is a bijection from N+ to it. Its cardinality is written ℵ₀, pronounced "aleph naught." We use **countable** to include finite sets as well. See Hammack's [section 14.2](https://richardhammack.github.io/BookOfProof/Main.pdf#page=287).

The practical test is whether the members can be arranged in an endless list with every member at a finite position, appearing exactly once. You never finish the list, but no particular member waits until "after infinity."

For `A = L("a"+)`, use the mapping `n → aⁿ`, where `aⁿ` means the string with n copies of `a`. This is mathematical repetition notation, not additional pattern-language syntax.

| Position n | Member of A |
| --- | --- |
| 1 | `"a"` |
| 2 | `"aa"` |
| 3 | `"aaa"` |
| … | … |

Every positive length gives a different string, and every string in A has one such length. The mapping is therefore a bijection, so A is countably infinite. No member is itself infinitely long.

**Checkpoint.** Does adding the empty string make `L("a"*)` a larger cardinality?

Answer: no. List `""`, `"a"`, `"aa"`, and so on. It is still countably infinite, even though `L("a"+)` is a proper subset of it.

## Why two repetition counts are still countable

Let `B = L("a"+ "b"+)`. Its members have the form `aⁱbʲ`, where i and j are independently chosen positive integers. For instance, `"aabbb"` corresponds to `(2, 3)`. `"a"`, `"b"`, `"ba"`, and `""` are excluded.

The mapping `(i, j) → aⁱbʲ` is a bijection from `N+ × N+` to B: the transition from `a` to `b` lets us recover both counts uniquely. B contains strings, not pairs, but the pairs give us a way to index them.

Trying to list all pairs with `i = 1` before moving to `i = 2` fails. The first row never ends. Instead, list by increasing sum `i + j`, and within each sum by increasing i:

| Sum | Pairs | Strings |
| --- | --- | --- |
| 2 | `(1, 1)` | `"ab"` |
| 3 | `(1, 2)`, `(2, 1)` | `"abb"`, `"aab"` |
| 4 | `(1, 3)`, `(2, 2)`, `(3, 1)` | `"abbb"`, `"aabb"`, `"aaab"` |
| … | … | … |

Every diagonal is finite. Any chosen pair has a finite sum, so we reach it after finitely many earlier entries. Every pair appears once. This is the diagonal-listing argument behind the [countability of a product of two countably infinite sets](https://richardhammack.github.io/BookOfProof/Main.pdf#page=290).

Now pair the first member of A with the first member of B, the second with the second, and so on:

| Member of A | Corresponding member of B |
| --- | --- |
| `"a"` | `"ab"` |
| `"aa"` | `"abb"` |
| `"aaa"` | `"aab"` |
| `"aaaa"` | `"abbb"` |
| `"aaaaa"` | `"aabb"` |
| `"aaaaaa"` | `"aaab"` |

The listing rule, not just this finite table, defines a bijection. Hence `|A| = |B| = ℵ₀`. It need not preserve string length or the counts inside a string. These sets are not equal, and neither contains the other.

A tempting alternative, `aⁿ → aⁿbⁿ`, is injective but not surjective onto B. It misses `"abb"` and `"aab"`. Equal cardinality guarantees that some bijection exists, not that every natural-looking mapping is one.

**Checkpoint.** Why does `"aabbb"` eventually appear in the diagonal list?

Answer: its pair `(2, 3)` is on the finite diagonal with sum 5. Only finitely many entries precede it.

## What the intuition about size is noticing

Cardinality ignores length and the internal organization of members. We can retain length information by counting accepted strings of each length. For a language L, define `c_L(n)` to be the number of its members with exactly n characters. This is a counting tool for the lesson, not proposed language syntax.

For positive n, our patterns give these counts:

| Exact length n | `"a"+` | `"a"+ "b"+` | `["a" "b"]+` |
| --- | --- | --- | --- |
| 1 | 1 | 0 | 2 |
| 2 | 1 | 1 | 4 |
| 3 | 1 | 2 | 8 |
| 4 | 1 | 3 | 16 |
| 5 | 1 | 4 | 32 |

These are deductions from our proposed [character-choice and repetition rules](regex-building-blocks.html#repetition-finite-and-unbounded-counts):

- `"a"+` has one string at each positive length.
- `"a"+ "b"+` has `n − 1` strings of length n: choose the split after one of the first `n − 1` characters.
- `["a" "b"]+` has `2ⁿ` strings of length n: choose `a` or `b` independently at each position.

All three languages are countably infinite, but their counts at each length differ. Up to length N, the first has N members and the second has `N(N − 1)/2`. The latter follows by summing the counts `0 + 1 + ... + (N − 1)`. A length bound makes the difference finite and directly comparable.

There is another warning about counting choices. For `"a"+ "a"+`, pairs `(1, 2)` and `(2, 1)` both concatenate to `"aaa"`. This pattern's two repetition counts do not uniquely identify distinct output strings. Its language is just `L("a"{2,})`, with one string at each length of at least two. The map from pairs to strings is surjective onto that language but not injective.

**Checkpoint.** How many distinct strings of length 4 match `"a"+ "a"+`? How many match `"a"+ "b"+`?

Answer: one (`"aaaa"`) versus three (`"abbb"`, `"aabb"`, `"aaab"`). Ways to split a match are not additional members.

## The limit of finite-string cardinalities

For any fixed nonempty finite alphabet, all finite strings can be listed by increasing length and then in a fixed order within each length. Each length contributes only finitely many strings, so every string appears at a finite position. This proves that their universe is countably infinite. Unicode scalar values also form a finite alphabet; Rust's [character definition](https://doc.rust-lang.org/std/primitive.char.html#validity-and-layout) gives its bounded code-point ranges.

Consequently, every set of strings in our lesson universe is finite or countably infinite, whether or not a regex can describe it. This follows from the listing argument and the [countability of infinite subsets of countable sets](https://richardhammack.github.io/BookOfProof/Main.pdf#page=294). Faster growth at each length does not create an uncountable set of finite strings.

That does not mean every infinite set has the same cardinality. The **power set** P(U), whose elements are all subsets of this string universe, has strictly greater cardinality than U by [Cantor's theorem](https://richardhammack.github.io/BookOfProof/Main.pdf#page=293). It is therefore uncountable. A string, a set of strings, and the set of all such sets are different kinds of object. Repetition builds finite strings; it is not the power-set operation.

**Checkpoint.** Does listing all finite strings also list every subset of those strings?

Answer: no. The first list contains individual strings. P(U) contains sets of strings, and cannot be put into such a countable list.

## What this gives us for language design

The preceding results are mathematics under our stated universe, not typing or conversion rules. They let us ask different questions without confusing them:

| Question | What to examine |
| --- | --- |
| Is this particular value allowed? | Membership |
| Are all values allowed by one constraint allowed by another? | Set inclusion |
| Can the sets be paired without collisions or omissions? | A bijection |
| How many values are available within a length bound? | Counts by length and their sums |
| Does a particular mapping lose distinctions or miss outputs? | Injectivity and surjectivity of that mapping |

For example, removing all `b`s defines a function from B to A. It is surjective, since `aⁱb` maps to `aⁱ` for every positive i. It is not injective: `"ab"` and `"abb"` both map to `"a"`. This particular conversion loses the `b` count, despite the sets having equal cardinality.

Likewise, equal cardinality alone does not establish inclusion or make unchanged values interchangeable: `"a"` belongs to A but not B. Whether to provide explicit encodings, conversions, or type relationships is recorded under [cardinality and mappings in the open design questions](open-design-questions.html#how-should-cardinality-and-mappings-affect-the-language).

**Checkpoint.** Does the existence of a bijection authorize an implicit conversion in the proposed language?

Answer: no. It establishes a mathematical possibility. Which mappings the language supports, and which properties they must preserve, remain design decisions.

Next: [open design questions](open-design-questions.html).
