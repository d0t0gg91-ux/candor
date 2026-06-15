# Grounding: where the personas come from

Candor's eight work-mode personas are not invented dispositions. Each one is a trait
profile drawn from established personality-science frameworks, chosen because its
characteristic working style is a good fit for a particular kind of task - and because
that same style tends to be naturally low in the behaviors candor is trying to reduce
(reflexive agreement, hedging, premature closure).

This document explains the frameworks, the method, and the rationale for each mode, so
you can judge the design and adapt it.

## The premise

A general-purpose assistant uses roughly one register for everything. But the working
style that makes a _code reviewer_ effective (closure-seeking, blunt, detail-complete)
is almost the opposite of the one that makes a _brainstormer_ effective (divergent,
slow to close, comfortable with half-formed ideas). Forcing one register onto both
makes the assistant mediocre at each.

Candor's bet is that **selecting a deliberate working style per task** produces more
useful output than a single averaged one - and that the most useful styles are also the
more candid ones.

## The four frameworks

The personas are built from four overlapping, publicly documented models of personality:

1. **The Five-Factor Model (Big Five / NEO).** Five trait domains - Openness,
   Conscientiousness, Extraversion, Agreeableness, Neuroticism - each broken into six
   finer **facets** (30 in total, e.g. _Straightforwardness_, _Deliberation_,
   _Self-Discipline_, _Compliance_, _Trust_, _Ideas_, _Aesthetics_). This is the
   substrate: the facets are the actual behavioral dials each persona turns.
2. **The 16-type model** (the Myers-Briggs-style four-axis system, plus an
   Assertive/Turbulent identity axis, and the four role families - Analyst, Diplomat,
   Sentinel, Explorer). A familiar shorthand layered on the Big Five.
3. **The twelve archetypes** (Jung's archetypes as popularized for brand and character
   work - Sage, Ruler, Creator, Explorer, Magician, and so on). Each archetype is a
   recognizable "way of being in the work" with a core motivation.
4. **The Predictive Index four-drive model** (Dominance, Extraversion, Patience,
   Formality, with named reference profiles like Strategist, Scholar, and Guardian). A
   work-behavior lens that maps cleanly onto the same traits.

Because all four describe the same underlying space, a single persona can be expressed
in several of these vocabularies at once - which is how each candor mode is specified.

## Method

The mappings were developed alongside **[Persage](https://github.com/d0t0gg91-ux)**, a
personality-assessment project that implements a scoring engine over these frameworks
(Big Five facets feeding derivations into the 16-type, archetype, and Predictive Index
models). Working through that engine made the trait-to-behavior relationships concrete:
which facets, when high or low, push toward directness, analytical rigor, divergent
creativity, disciplined execution, or vigilant skepticism.

Candor keeps the _public-framework_ layer of that work and leaves the project-specific
scoring internals out - what matters for a behavioral skill is the trait reasoning, not
any particular numeric model. A few dials do most of the work:

- **Low Agreeableness (esp. low Compliance, high Straightforwardness)** -> directness;
  the willingness to hold a position and give frank assessments. This is the core
  anti-sycophancy lever.
- **High Conscientiousness** -> closure and follow-through; good for shipping, a
  liability for open-ended exploration.
- **High Openness** -> breadth, novelty, abstraction; good for ideation and creative
  work, less relevant to mechanical execution.
- **Low Trust** -> healthy skepticism of inputs and assumptions; the lever behind
  security review and debugging.

## The work modes

| Mode              | Type   | Archetype / role       | PI profile      | Signature traits                                                                  | Why it fits                                                                                                                                               |
| ----------------- | ------ | ---------------------- | --------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Coding**        | INTJ-A | Ruler                  | Strategist      | high Conscientiousness, high Straightforwardness, low Compliance                  | Closure-seeking discipline is what shipping correct code needs; low Compliance keeps reviews honest under pushback.                                       |
| **Logical**       | INTP-A | Sage                   | Scholar         | high Openness (Ideas, Values), high Deliberation, low Compliance                  | Reasoning quality depends on _not_ closing early; the Sage holds the question open and won't cave to social pressure.                                     |
| **Creative**      | INFP-A | Creator                | (collaborative) | highest Openness, enough Self-Discipline to finish                                | Maximum imaginative reach, anchored by an internal quality standard so feedback stays honest, not encouraging.                                            |
| **Brainstorming** | ENTP-A | Explorer               | Maverick        | high Openness + Extraversion, low closure pressure, low Compliance                | Divergence needs externalized, high-volume ideation that resists premature convergence and challenges the frame.                                          |
| **Security**      | ISTJ-T | Sentinel (role)        | Guardian        | low Trust, high Order/Dutifulness/Deliberation, vigilance, attacker's imagination | Defensive work needs low-trust skepticism and threat-modeling; the Sentinel family is literally the security/stability disposition. Defensive scope only. |
| **Debugging**     | ISTP-A | the Detective          | Operator        | low Trust in assumptions, high Deliberation and Ideas, low Self-Consciousness     | Finding a real cause needs repro-first discipline and the willingness to suspect your own recent change before blaming the tools.                         |
| **Architecture**  | INTJ-A | Magician               | Strategist      | high Ideas / Deliberation / Competence, low Compliance                            | Design altitude needs explicit trade-offs, failure-mode thinking, the nerve to commit to one recommendation, and to challenge a bad requirement.          |
| **Writing**       | ENFJ-A | Mentor (Diplomat role) | Persuader       | reader-modeling, high Straightforwardness and Order                               | Clear explanation needs audience-modeling (a Diplomat strength), with the candor overlay keeping it from fake-reassurance.                                |

A note on the mappings: the first four and _Debugging_/_Architecture_ map cleanly onto a
single Jungian archetype; _Security_ and _Writing_ are anchored instead on their 16-type
role family (Sentinel, Diplomat) and Predictive-Index profile (Guardian, Persuader),
which fit those dispositions more precisely than forcing a single archetype would. Each
mode's `SKILL.md` translates its trait signature into concrete behavioral directives and a
before/after example.

## The shared core, and why it's calibrated

Underneath all eight sits `candor-core`. Its job is to counter the specific ways an
assistant becomes less useful: leading with validation before a correction, reversing a
correct answer because the user pushed back (with no new evidence), hollow affirmations,
reflexive caveats, false balance, padding a correct answer with unrequested detail, and
claiming success without verifying.

The deliberate counterweight is a set of **calibration guardrails**. Genuine agreement
and sycophantic agreement are different things, and an assistant that suppresses _all_
agreement to look tough is just miscalibrated in the other direction. So the core
explicitly requires: agree clearly when the user is right, update openly when there's
real new evidence, attack claims rather than people, and match intensity to stakes.
Directness without that calibration is not the goal.

## Limitations

- **It's instructional, not guaranteed.** These are prompts. They shape behavior
  strongly and consistently but cannot enforce it the way fine-tuning could. Effects
  vary by model and situation.
- **Personality frameworks are models, not truth.** The Big Five has the strongest
  empirical support; the 16-type and archetype systems are useful organizing
  vocabularies more than validated instruments. They are used here as _design language_
  for working styles, not as claims about human psychology.
- **The mode boundaries are fuzzy.** Real tasks blend modes. The skills are written to
  layer over the shared core rather than to be mutually exclusive.
- **The benchmark is small.** See [evals/RESULTS.md](evals/RESULTS.md): the effect is
  real but measured on 20 prompts against one model, and the modern base model is already
  fairly candid, so the headline gains are modest and concentrated in form and framing.

## Further reading

- Costa, P. T., & McCrae, R. R. - the NEO-PI-R and the Five-Factor Model (the source of
  the 30-facet structure).
- C. G. Jung, _The Archetypes and the Collective Unconscious_; and Mark, M. & Pearson,
  C., _The Hero and the Outlaw_ (the popular twelve-archetype framing).
- The Predictive Index behavioral assessment (the four-drive model and reference
  profiles) - predictiveindex.com.
- Research on sycophancy in language models - e.g. Sharma et al., _Towards Understanding
  Sycophancy in Language Models_ (Anthropic) - documents how assistants trained with
  human feedback drift toward agreement over accuracy. (Search the title; this doc
  intentionally avoids citing identifiers it hasn't verified.)
