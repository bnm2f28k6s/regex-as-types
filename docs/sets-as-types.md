# Sets as types

Why have we spent so much time describing sets? Our pattern language is a **type-level language**: a language for describing which values a program may use, rather than instructions for computing those values. A pattern describes a type's allowed values, and membership tells us whether a particular value satisfies it.

Read [building patterns from sets](regex-building-blocks.html) and [cardinality and mappings](cardinality-and-mappings.html) first. This lesson connects those foundations to type checking. The approved model uses string values, identifies pattern types by their allowed sets, and defines subtyping by inclusion. Unknown membership requires an explicit check before constrained use; static or dynamic enforcement and failure reporting are left to implementations or host integration. Detailed program typing rules remain open; there is no implemented checker or complete type system here.

At the language level, all values are strings. Numbers, for example, are described by constrained string sets, not a separate non-string value kind. Implementations may use other internal representations as optimizations, provided they preserve the language-level meaning. We retain finite Unicode scalar-value strings as the teaching universe U, but the final character model and encoding remain [open questions](open-design-questions.html#what-values-do-constraints-describe). The examples use ASCII, whole-string acceptance, and unchanged, immutable values, without implicit trimming or normalization.

## A type expression describes allowed values

A pattern, when used as a type expression, denotes its accepted string set `L(p)`. This is our approved **set-theoretic interpretation of types**: the meaning of a type is a set of values. CDuce's [introduction to types and patterns](https://www.cduce.org/manual_types_patterns.html#intro) provides an existing example of this approach, including singleton types. It supplies precedent, not our grammar.

Keep three things separate:

| Thing | Example | Role |
| --- | --- | --- |
| Value | `"cat"` | A particular string a program could use |
| Type expression | <code>&#96;cat&#96; &#124; &#96;dog&#96;</code> | A description written in our proposed language |
| Denoted set | `{"cat", "dog"}` | The values that description permits |

Here, **denotes** means "has this set as its meaning." The set contains string values, not other types. We are not asking whether a string is a valid type declaration; we are asking whether it is a permitted value of the described type.

This lets us reuse the pattern vocabulary instead of inventing a second set notation for types. The same whole-string meaning applies in either role. How a surrounding program marks a type position is still open; this lesson does not introduce declarations, named fragments, or a membership-test operator.

**Checkpoint.** Is `"cat"` itself the two-member set described by <code>&#96;cat&#96; &#124; &#96;dog&#96;</code>?

Answer: no. It is one value in that set. The type expression describes the set.

## Equal sets mean equal pattern types

Different pattern expressions can describe exactly the same set. The approved rule is that they then describe the same type, regardless of spelling. For example:

```text
`a` | `b` | `c`
```

```text
[`a`-`c`]
```

Both describe `{"a", "b", "c"}` by our [alternatives and range rules](regex-building-blocks.html#character-ranges-abbreviate-consecutive-choices). Neither accepts `"ab"` or `"d"`. Their type equality follows from equal membership, not equal source text or merely equal cardinality.

This separates the pattern's written representation from its meaning. It is also separate from an implementation's storage representation. As an optional Rust comparison, [a type alias gives an existing type another name, whereas a newtype introduces a distinct type](https://doc.rust-lang.org/book/ch20-03-advanced-types.html#type-synonyms-and-type-aliases). Equal underlying storage alone does not make Rust newtypes interchangeable. Our approved rule concerns equal denoted string sets; it does not introduce Rust-style wrappers or naming syntax.

**Checkpoint.** Do two patterns become different types merely because one uses a range and the other lists the same alternatives?

Answer: no. If their accepted sets are equal, their pattern types are equal. How a future checker establishes that equality remains an algorithm-design question.

## Membership checks one value

For a concrete string v and a pattern p used as a type expression, satisfaction is simply membership:

```text
v satisfies p  exactly when  v ∈ L(p)
```

This is mathematical explanation, not executable syntax. It applies the earlier [definition of L(p)](regex-introduction.html#a-pattern-as-a-description-of-a-set); no separate search mode or engine behavior is involved.

| Type expression | Value | Satisfies it? |
| --- | --- | --- |
| <code>&#96;cat&#96;</code> | `"cat"` | Yes |
| <code>&#96;cat&#96;</code> | `"cats"` | No |
| <code>&#96;cat&#96; &#124; &#96;dog&#96;</code> | `"dog"` | Yes |
| <code>&#96;cat&#96; &#124; &#96;dog&#96;</code> | `"catdog"` | No |
| <code>&#96;&#96;</code> | `""` | Yes |
| <code>&#96;&#96;</code> | `" "` | No |

A **singleton type** permits exactly one value, as in the CDuce [singleton-type explanation](https://www.cduce.org/manual_types_patterns.html#intro). Under our interpretation, <code>&#96;cat&#96;</code> is a singleton string type. So is <code>&#96;&#96;</code>: it permits the empty string, not zero values. The approved spelling `[]` denotes ∅ and therefore the **empty type**, with no permitted values at all. It rejects even `""`. See [empty brackets](regex-building-blocks.html#empty-brackets-describe-the-empty-set) for the distinction and its repetition boundary cases.

**Checkpoint.** Does satisfying <code>&#96;cat&#96;</code> change `"cats"` into `"cat"`?

Answer: no. Checking membership accepts or rejects the unchanged value. It does not extract, trim, or convert it.

## A string constraint can be a refinement

A **refinement type** restricts a base type using a predicate, a condition that is true or false for each value. The [LiquidHaskell introduction to refinement types](https://ucsd-progsys.github.io/liquidhaskell-tutorial/Tutorial_01_Introduction.html#refinement-types) describes this combination of types and predicates. Its checker and predicate logic are not requirements for our language.

In our string-only model, the base is U and the condition is whole-string acceptance. A pattern-constrained string can therefore be understood as a refinement of the base string type:

```text
{s ∈ U | s is accepted by p} = L(p)
```

For example, the [label pattern](regex-building-blocks.html#a-complete-example) refines strings to labels with lowercase ASCII letters, a hyphen, and two ASCII digits:

```text
[`a`-`z`]+ `-` [`0`-`9`]{2}
```

It permits `"cat-42"` and `"a-00"`. It rejects `"Cat-42"`, `"cat-4"`, and `"cat-042"`. The value stays a string. A numeric type in our language would likewise describe strings with numeric structure, not introduce a separate non-string value kind. An implementation may use a numeric representation internally without changing the allowed language-level strings.

"Pattern-constrained string type" is a useful plain-language name for our first examples. "Refinement type" explains their relationship to a base string type; "set-theoretic interpretation" explains what the type expressions mean. These terms describe different aspects of the proposal, not competing choices of syntax.

**Checkpoint.** Does restricting strings to labels mean that our language already supports arbitrary refinement predicates?

Answer: no. The analogy explains the restriction. It does not add arithmetic predicates, a solver, or other type features to our pattern vocabulary.

## Numeric structure and canonical strings

The string model is a language-design choice, not a claim that every implementation must store text literally. An integer-like type can specify a digit alphabet and rules for arranging those digits. A canonical form then selects a preferred spelling rather than automatically rewriting every accepted input.

For this illustration only, consider unsigned decimal strings using ASCII digits. The permissive pattern allows leading zeroes:

```text
[`0`-`9`]+
```

A proposed canonical form allows exactly `"0"`, or a nonzero first digit followed by any number of digits:

```text
`0` | [`1`-`9`] [`0`-`9`]*
```

These examples are deductions from our [pattern-building rules](regex-building-blocks.html), not a settled definition of signed integers or arithmetic.

| String value | Permissive decimal form? | Proposed canonical form? |
| --- | --- | --- |
| `"0"` | Yes | Yes |
| `"7"` | Yes | Yes |
| `"007"` | Yes | No |
| `"00"` | Yes | No |
| `"-7"` | No | No |
| `""` | No | No |
| `"٧"` | No | No |

The canonical set is a subset of the permissive set, so its type is a subtype. The two types are not equal: `"007"` belongs only to the permissive set. Checking the canonical constraint rejects that value; it does not turn it into `"7"`. Such a rewrite would be a separate normalization operation whose rules are still open.

An optimized representation must preserve whatever distinctions the language exposes. If both `"007"` and `"7"` are allowed as distinct strings, storing only their common numeric interpretation would lose the leading-zero distinction. The implementation would need to retain that information or limit that optimization to an appropriate canonical set. It must also preserve the allowed set rather than silently restrict it to a machine integer's range. No storage format or optimization is implemented here.

**Checkpoint.** Does the all-strings model forbid an implementation from using numeric storage?

Answer: no. Storage may differ, but it must preserve the language-level values and behavior. Signs, zero spellings, arithmetic, and normalization still need their own design rules.

## Checking without choosing static or dynamic enforcement

Checking a known value asks whether that one value belongs to a set. **Static type checking** instead reasons about program expressions using typing rules and known information, without requiring their runtime results. For a concrete example of that distinction, [Software Foundations' typechecker chapter](https://softwarefoundations.cis.upenn.edu/plf-current/Typechecking.html) separates the typing relation from an algorithm that checks terms in a context.

Our semantic requirement is that a value used under a constraint belongs to its allowed set. A prior guarantee can establish this through inclusion. Otherwise, unknown membership requires an explicit check before constrained use. "Unknown" describes missing information, not a new string value or a third membership outcome. The theoretical language does not require a static, dynamic, or mixed enforcement strategy.

Suppose a use requires the set `{"cat", "dog"}`:

| Information available | What follows in our proposed model? |
| --- | --- |
| The expression is the known value `"cat"` | Membership establishes that this value is allowed |
| Its possible results are known to lie in `{"cat", "dog"}` | Every possible result is allowed |
| Its results are only known to be strings | That information is insufficient; `"cow"` is a counterexample |
| An external string has passed the whole-string check | The checked value belongs to the required set; how a host carries that guarantee is integration machinery |

Insufficient information does not mean the value is invalid. It means the required membership has not been established. The approved boundary rule requires an explicit check in that case, without prescribing whether an implementation establishes the result before execution or checks an actual input during execution. A failed check does not authorize using the value under the constraint.

For a concrete example, suppose an operation requires the canonical decimal form above, but its input comes from a file. Before reading the file, we cannot assume which string it contains:

| Situation | What is known? |
| --- | --- |
| The source guarantees canonical decimal strings | Inclusion already justifies using its result; this requirement needs no additional value check |
| The source guarantees only an arbitrary string | Validity is unknown; it could be `"7"`, `"007"`, or `"cat"` |
| A later membership check accepts the actual string `"7"` | This value satisfies the canonical constraint |
| A later membership check rejects `"007"` or `"cat"` | That value cannot be used unchanged where canonical form is required |

The input may be valid even when the initial information is too broad. A runtime check is one way an implementation could establish membership. A host with static checking could also track that only a successful path supplies the constrained value. TypeScript's [explanation of type guards and narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html) provides a supplemental analogy for this combination; neither mechanism is required by our core model.

The need to check unknown membership is settled. The machinery is deferred: file input, check execution, carrying a successful guarantee, and surfacing failure belong to a future implementation or host integration. The theoretical set language does not need to choose an exception, diagnostic, optional value, or result representation now. This explanation introduces no input, branching, or error-handling syntax.

Optional or result-like representations may be considered in that future integration work, but none is selected here. Do not confuse an optional value with the existing pattern quantifier `?`, which permits zero or one copy and can therefore admit the empty string. The empty string is a value, not an already-defined absence or failure marker.

A Boolean membership answer alone does not specify a surrounding program's typing or control-flow rules. Those can be designed separately if needed, without making a runtime or native integration part of the theoretical set language. No such implementation is added by this lesson.

**Checkpoint.** If an arbitrary input string might equal `"cat"`, may a static checker assume it satisfies the singleton type <code>&#96;cat&#96;</code>?

Answer: no. Possibility is not a guarantee. It needs stronger static information or a successful check whose result the type rules can use.

## Inclusion defines subtyping

**Subtyping** allows a value of one type to be used where another type is expected. See [Software Foundations' safe substitution principle](https://softwarefoundations.cis.upenn.edu/plf-current/Sub.html). For our pattern-defined types, the approved rule is inclusion of the denoted sets:

```text
S <: T  exactly when  S ⊆ T
```

Here S and T name allowed-value sets in the mathematics. `<:` reads "is a subtype of"; it is explanatory notation, not a chosen operator in our language. Defining subtyping through set inclusion is called **semantic subtyping**. CDuce's [subtyping explanation](https://www.cduce.org/manual_types_patterns.html#tvar) states this set-containment interpretation, and its [semantic-subtyping research](https://www.cduce.org/papers.html) develops the wider approach.

Let S be `{"cat"}` and T be `{"cat", "dog"}`. Every S value is a T value, so S is a subtype of T. A use that permits either animal can receive a value guaranteed to be `"cat"`, without conversion or an additional membership check for that requirement. The reverse is not justified: `"dog"` belongs to T but not S.

| Source guarantee | Required set | Inclusion holds? |
| --- | --- | --- |
| `{"cat"}` | `{"cat", "dog"}` | Yes |
| `{"cat", "dog"}` | `{"cat"}` | No; `"dog"` is excluded |
| `{"cat"}` | `{"dog"}` | No; `"cat"` is excluded |
| `{"cat"}` | `{"cat"}` | Yes |

This explains why a more restrictive allowed-value set gives a subtype: it makes a stronger guarantee. We can forget that extra precision when passing to a broader requirement. This is the idea of [subsumption](https://softwarefoundations.cis.upenn.edu/plf-current/Sub.html), not a conversion of the value.

The [cardinality lesson](cardinality-and-mappings.html#equal-cardinality-means-a-bijection-exists) showed why equal size is different. `{"cat"}` and `{"dog"}` have equal cardinality, but neither includes the other. A bijection does not authorize passing `"cat"` unchanged where only `"dog"` is allowed.

This rule establishes compatibility of the denoted value sets. It does not by itself supply rules for function expressions, mutable storage, or nontermination. Those still need definitions consistent with the string-value model. Variables and named fragments remain deferred; this lesson adds no separate nominal type-identity mechanism.

Since the [empty set is a subset of every set](sets.html#subsets-and-proper-subsets), the empty type `[]` is a subtype of every pattern type in this model. That does not supply a value to pass: no string satisfies `[]`. The empty-string type is different because it has the member `""`.

**Checkpoint.** Can a value known only to satisfy <code>&#96;cat&#96; &#124; &#96;dog&#96;</code> be used wherever <code>&#96;cat&#96;</code> is required?

Answer: not on that guarantee alone. It could be `"dog"`. Inclusion works in the other direction.

## Set operations explain type combinations

Once a type denotes allowed values, the earlier [set operations](set-operations.html) explain possible type combinations. These are deductions under our approved interpretation, consistent with CDuce's [set-theoretic type connectives](https://www.cduce.org/manual_types_patterns.html#bool). They do not import CDuce's operator spellings.

| Set construction | Interpretation for string constraints |
| --- | --- |
| `S ∪ T` | Values permitted by either constraint |
| `S ∩ T` | Values permitted by both constraints |
| `S ∖ T` | Values permitted by S but excluded by T |
| `U ∖ S` | String values outside S, relative to U |
| `∅`, written `[]` | No permitted string values, not even `""` |
| `U` | Every string value in the teaching universe |

For S = `{"cat", "dog"}` and T = `{"dog", "cow"}`, the union is `{"cat", "dog", "cow"}`, the intersection is `{"dog"}`, and `S ∖ T` is `{"cat"}`. An intersection requires the same value to satisfy both constraints; it is not a pair of values or string concatenation.

Alternatives already express union, and `[]` spells the empty set and empty type. Intersection, difference, complement, and an explicit universal type spelling remain [open notation questions](open-design-questions.html#what-notation-expresses-the-operations). U is the string-value universe; its final character model is not yet settled. Optimized internal storage does not introduce a second language-level universe.

**Checkpoint.** Is the intersection of `{"cat"}` and `{"dog"}` the type of the empty string?

Answer: no. Their intersection is ∅, written `[]`, with no members. The type of the empty string denotes `{""}`, with one member.

## What remains to design

We now have a reason for the set lessons: patterns describe string-value sets at the type level, equal denoted sets give equal pattern types, membership checks concrete values, and inclusion justifies passing values between constraints. These are approved foundations, not a finished static type system.

The core design can continue with type-position notation, set operations, and numeric string forms. If we later connect it to executable programs, implementations or hosts will need checking machinery and ways to preserve guarantees. Static versus dynamic enforcement, native integration, and failure representations are deferred rather than prerequisites for this theoretical lesson. Defining a set's mathematical meaning does not itself supply a checking algorithm, as the [Software Foundations typechecker introduction](https://softwarefoundations.cis.upenn.edu/plf-current/Typechecking.html) illustrates for its own typing relation.

**Checkpoint.** Have we committed to a compiler, runtime, external regex engine, or solver?

Answer: no. We have fixed the string-value interpretation, type equality, inclusion-based compatibility, and explicit checking of unknown membership. Enforcement timing, failure reporting, and native machinery remain implementation or integration work outside the present core.

Next: [open design questions](open-design-questions.html#how-do-type-expressions-support-checking).
