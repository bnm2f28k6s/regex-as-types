# Set operations

An operation builds a new set from existing sets. If you are unsure about membership or subsets, review [set foundations](sets.html) first.

The standard definitions come from the textbook's [set notation](https://discrete.openmathbooks.org/dmoi3/sec_intro-sets.html#subsec_notation) and [operations on sets](https://discrete.openmathbooks.org/dmoi3/sec_intro-sets.html#sec_intro-sets-5). We use our own worked examples throughout this page.

For union through symmetric difference, keep these sets fixed:

- `U = {1, 2, 3, 4, 5}`
- `A = {1, 2, 3}`
- `B = {3, 4}`

## Union

The union contains values in A **or** B, including values in both.

```math
A \cup B = \{x \in U \mid x \in A \text{ or } x \in B\}
```

Our result is `{1, 2, 3, 4}`. The shared value `3` appears only once. `5` is excluded because it is in neither set. See the [union definition](https://discrete.openmathbooks.org/dmoi3/sec_intro-sets.html#subsec_notation).

**Checkpoint.** What is `A ∪ ∅`?

Answer: A. Adding no elements changes nothing.

## Intersection

The intersection contains values in A **and** B.

```math
A \cap B = \{x \in U \mid x \in A \text{ and } x \in B\}
```

Our result is `{3}`. `2` is excluded because it is not in B; `4` is excluded because it is not in A. See the [intersection definition](https://discrete.openmathbooks.org/dmoi3/sec_intro-sets.html#subsec_notation).

**Checkpoint.** What is `A ∩ ∅`?

Answer: `∅`. No value can belong to the empty set.

## Difference

The difference keeps values in A that are not in B.

```math
A \setminus B = \{x \in U \mid x \in A \text{ and } x \notin B\}
```

Our result is `{1, 2}`. In the other direction, `B ∖ A = {4}`. The order matters. See the [difference definition](https://discrete.openmathbooks.org/dmoi3/sec_intro-sets.html#subsec_notation).

**Checkpoint.** What is `A ∖ A`?

Answer: `∅`. Every element would be removed.

## Complement

The complement contains everything in the chosen universe that is not in A. We write it as `U ∖ A` to keep that universe visible.

```math
U \setminus A = \{x \in U \mid x \notin A\}
```

Our result is `{4, 5}`. If we instead chose `U = {1, 2, 3, 4, 5, 6}`, it would be `{4, 5, 6}`. Complement depends on U. See the [complement definition](https://discrete.openmathbooks.org/dmoi3/sec_intro-sets.html#subsec_notation).

**Checkpoint.** What is `U ∖ U`?

Answer: `∅`. Nothing in U is outside U.

## Symmetric difference

Keep values belonging to exactly one of the sets, not both. We denote this operation by `A △ B` and define it using difference and union:

```math
A \triangle B = (A \setminus B) \cup (B \setminus A)
```

Using the [definitions of difference and union](https://discrete.openmathbooks.org/dmoi3/sec_intro-sets.html#subsec_notation), we can derive our result: `{1, 2} ∪ {4} = {1, 2, 4}`. The shared value `3` is excluded. Whether our language should give this operation its own notation is a later [design question](open-design-questions.html#what-notation-expresses-the-operations).

**Checkpoint.** What is `A △ A`?

Answer: `∅`. Every element belongs to both sets, not exactly one.

## Cartesian product

A Cartesian product contains ordered pairs. Each pair takes its first element from one set and its second from the other. This is the textbook's [product definition](https://discrete.openmathbooks.org/dmoi3/sec_intro-sets.html#subsec_notation).

For this example, choose `C = {"a", "b"}` and `D = {"0", "1"}`.

```math
C \times D = \{(c,d) \mid c \in C \text{ and } d \in D\}
```

The result is `{("a", "0"), ("a", "1"), ("b", "0"), ("b", "1")}`. `("0", "a")` is excluded because its first element is not in C.

A pair is not a joined string: `("a", "0")` and `"a0"` are different values. Regex concatenation will join strings instead of building pairs.

**Checkpoint.** What is `C × ∅`?

Answer: `∅`. There is no second element available for any pair.

## Power set

The power set of A is the set of all subsets of A, including the empty set and A itself. See the textbook's [power-set definition](https://discrete.openmathbooks.org/dmoi3/sec_intro-sets.html#subsec_notation).

For a small example, choose `E = {1, 2}`.

```math
P(E) = \{∅, \{1\}, \{2\}, \{1,2\}\}
```

The elements of this result are sets, not individual numbers. `{1}` is in the power set; `{3}` is not, because it is not a subset of E. A power set is not regex repetition.

**Checkpoint.** What is the power set of `∅`?

Answer: `{∅}`. The empty set has exactly one subset, itself.

## Combining operations

Parentheses make the grouping explicit. For our original A and B:

`(A ∪ B) ∖ {3} = {1, 2, 4}`.

This is a deduction from the earlier definitions: first collect values in either set, then remove `3`. It happens to equal `A △ B` in this example because `3` is their only shared value.

**Checkpoint.** Does swapping A and B change union? Does it change difference?

Answer: union is unchanged because "in A or B" is symmetric. Difference can change because it removes values from a specified starting set.

Next: [strings and regexes](regex-introduction.html).
