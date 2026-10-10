# Set foundations

A set lets us ask a simple question: is this value allowed? Before using regexes to answer that question for strings, we need a vocabulary for sets.

The definitions below follow Oscar Levin's [*Discrete Mathematics: An Open Introduction*, section 0.3](https://discrete.openmathbooks.org/dmoi3/sec_intro-sets.html). The small examples and checkpoints are our own.

## Sets and membership

A set is a collection of distinct elements. Write its elements inside braces. For example, `A = {1, 2, 3}` contains the numbers `1`, `2`, and `3`.

`2 ∈ A` means "2 is an element of A." `4 ∉ A` means "4 is not an element of A." Membership is a yes-or-no question, not a position in a list. These are the textbook's [membership conventions](https://discrete.openmathbooks.org/dmoi3/sec_intro-sets.html#subsec_notation).

**Checkpoint.** Is `3 ∈ A` true? Is `0 ∈ A` true?

Answer: the first is true; the second is false.

## Equality, order, and duplicates

Two sets are equal when they have exactly the same elements. Order and repeated entries do not change a set, as explained in the textbook's [introduction to sets](https://discrete.openmathbooks.org/dmoi3/sec_intro-sets.html).

`{1, 2, 3}`, `{3, 1, 2}`, and `{1, 1, 2, 3}` therefore describe the same set. But `{1, 2}` is different because it has no `3`.

**Checkpoint.** Are `{2, 2, 3}` and `{3, 2}` equal?

Answer: yes. Both contain exactly `2` and `3`.

## The universe of discussion

The universe, written `U`, is the set of values under discussion. It is not a claim that there is a set of absolutely everything. The textbook introduces a universe alongside its [special sets](https://discrete.openmathbooks.org/dmoi3/sec_intro-sets.html#subsec_notation).

For our first examples, choose `U = {1, 2, 3, 4, 5}`. A question about "everything outside A" now has a boundary. If `A = {1, 2, 3}`, the values in this universe outside A are `4` and `5`.

Later we will choose a different universe: strings. That is a lesson assumption, not an approved language design.

**Checkpoint.** Would adding `6` to U change which values are outside A?

Answer: yes. `6` would also be outside A within the new universe.

## The empty set

The empty set, written `∅` or `{}`, contains no elements. This is the textbook's [empty-set definition](https://discrete.openmathbooks.org/dmoi3/sec_intro-sets.html#subsec_notation).

Be careful about three different objects:

- `∅` has no elements.
- `{∅}` has one element, which is itself the empty set.
- `{""}` has one element, which is an empty string. We will introduce strings in the [regex introduction](regex-introduction.html#strings-and-the-empty-string).

**Checkpoint.** Does `∅` contain the number `0`?

Answer: no. Having no elements is different from containing a zero.

## Subsets and proper subsets

`A ⊆ B` means that every element of A is also in B. Equality is allowed. We write `A ⊊ B` for a proper subset: A is a subset of B, but A and B are different. See the textbook's [relationships between sets](https://discrete.openmathbooks.org/dmoi3/sec_intro-sets.html#sec_intro-sets-4).

If `A = {1, 2}` and `B = {1, 2, 3}`, then A is a proper subset of B. Also, `B ⊆ B`. The empty set is a subset of every set: it has no element that could violate the condition.

Membership and inclusion ask different questions. `2 ∈ B` checks one element; `{2} ⊆ B` checks all elements of a set. `{2} ∈ B` is false here because B contains numbers, not the set `{2}`.

**Checkpoint.** Is `{1, 4} ⊆ B` true?

Answer: no, because `4 ∉ B`.

## Describing a set with a rule

Instead of listing elements, we can state a membership condition. This is [set-builder notation](https://discrete.openmathbooks.org/dmoi3/sec_intro-sets.html#subsec_notation).

```math
A = \{x \in U \mid x < 4\}
```

Read this as "A contains the values x in U such that x is less than 4." With `U = {1, 2, 3, 4, 5}`, it describes `{1, 2, 3}`. The vertical bar means "such that" here. It is mathematical notation, not regex syntax.

A rule also lets us describe an infinite set without writing every element. For example, among all integers, the rule "x is positive" describes `{1, 2, 3, ...}`.

**Checkpoint.** In our finite U, which values satisfy "x is greater than 3"?

Answer: `{4, 5}`.

Next: [set operations](set-operations.html).
