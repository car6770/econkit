# Code of Conduct

## Our Commitment

EconKit is a project for learning, building, and sharing economics data analysis tools.

We want this project to be a welcoming space for:

- students
- early researchers
- instructors
- analysts
- contributors learning Python
- contributors learning economics
- contributors improving documentation, examples, tests, and code

Everyone should be able to participate without being mocked, harassed, dismissed, or discouraged.

The goal is simple:

```text
Be professional.
Be respectful.
Help people learn.
Improve the project.
```

---

## Project Values

EconKit is built around the following values.

### 1. Respect

Treat others with basic respect.

People may have different levels of experience in:

- Python
- economics
- statistics
- econometrics
- GitHub
- open-source contribution
- English writing
- documentation
- testing
- command-line tools

A beginner question is not a bad question.

---

### 2. Clarity

Communicate clearly.

Good communication includes:

- explaining what changed
- explaining why it changed
- giving examples when helpful
- using readable commit messages
- writing issues with enough context
- avoiding unnecessary jargon

---

### 3. Constructive Feedback

Feedback should improve the project, not attack the person.

Good:

```text
This function might be easier to understand if the variable names were more explicit.
```

Bad:

```text
This code is stupid.
```

Good:

```text
The report output works, but the economic interpretation may overstate what the model can prove.
```

Bad:

```text
You clearly do not understand economics.
```

---

### 4. Educational Honesty

EconKit includes simplified economic tools.

Contributors should be honest about what the project can and cannot do.

It is acceptable to say:

```text
This is a simplified teaching model.
```

It is not acceptable to present simplified outputs as guaranteed forecasts, official policy recommendations, or investment advice.

---

### 5. Reproducibility

Contributions should help users reproduce results.

Good contributions:

- include clear input assumptions
- save outputs in predictable places
- update documentation
- update tests when needed
- avoid hidden state
- avoid unexplained black-box behavior

---

## Expected Behavior

Participants are expected to:

- use respectful language
- welcome beginners
- ask clarifying questions when needed
- give constructive feedback
- focus on the project and the work
- acknowledge mistakes when they happen
- document important changes
- respect different learning speeds
- avoid personal attacks
- avoid hostile or humiliating comments
- avoid intentionally derailing discussions

---

## Unacceptable Behavior

The following behaviors are not acceptable:

- harassment
- threats
- insults
- personal attacks
- discriminatory language
- sexual harassment
- repeated unwanted contact
- publishing private information
- mocking beginners for not knowing something
- intentionally misleading contributors
- sabotaging tests, code, documentation, or issues
- hostile comments about a person's background, identity, language ability, school, job, or experience level

This project should remain focused on economics, programming, learning, and reproducible analysis.

---

## Examples of Good Participation

### Good Issue Comment

```text
I tried running:

python src/econkit_cli.py policy data/sample_economic_data.csv --output-dir outputs/policy

The command worked, but the report did not explain the policy gap clearly.

Suggested improvement:
Add a short explanation of whether the actual interest rate is above or below the benchmark.
```

### Good Pull Request Summary

```text
This PR improves the inflation pressure report.

Changes:
- Adds inflation momentum to the Markdown report
- Adds a JSON output file
- Updates docs/cli.md
- Adds a test for the new output structure
```

### Good Review Comment

```text
This works, but I think the function name could be more specific.
Maybe `analyze_inflation_pressure` is clearer than `inflation_check`.
```

---

## Examples of Poor Participation

### Poor Issue Comment

```text
This project is broken. Fix it.
```

### Poor Review Comment

```text
Nobody would write code like this.
```

### Poor Economic Interpretation

```text
This model proves that the central bank must cut rates next year.
```

Better:

```text
This simplified policy-rule benchmark suggests that the current rate is above the model-implied rate under the selected assumptions.
```

---

## Handling Disagreements

Disagreements are normal in economics and software.

When disagreement happens:

1. Focus on the specific claim or code.
2. Explain the reasoning.
3. Provide examples or evidence if possible.
4. Avoid personal comments.
5. Accept that some choices are design choices.
6. Prefer transparent assumptions over hidden complexity.

Example:

```text
I prefer keeping this model simple because EconKit is designed for teaching.
A more advanced version could be added later as an optional function.
```

---

## Economic Interpretation Standards

When discussing economic results, contributors should avoid overclaiming.

Preferred language:

```text
suggests
indicates
classifies
under these assumptions
based on this simple rule
in this dataset
as an exploratory result
```

Avoid:

```text
proves
guarantees
will definitely happen
officially predicts
must happen
```

EconKit is a toolkit for analysis and learning, not a source of official forecasts.

---

## Data Privacy and Security

Do not share or commit:

- private datasets
- confidential research data
- personal information
- API keys
- passwords
- tokens
- credentials
- paid or licensed datasets that cannot be redistributed

If an example dataset is needed, use a small synthetic dataset.

---

## Reporting Problems

If you see behavior that violates this Code of Conduct, report it through the project's GitHub issue system or contact the project maintainer.

When reporting, include:

- what happened
- where it happened
- when it happened
- links or screenshots if available
- whether the behavior is ongoing
- any immediate safety or privacy concerns

Reports should be handled with care.

---

## Maintainer Responsibilities

Project maintainers are responsible for:

- encouraging respectful participation
- clarifying contribution standards
- responding to harmful behavior
- protecting project quality
- keeping discussions focused
- removing inappropriate content when necessary
- limiting participation of users who repeatedly violate this Code of Conduct

Maintainers may take actions such as:

- giving a warning
- editing or removing inappropriate comments
- closing hostile issues
- rejecting pull requests submitted in bad faith
- temporarily limiting participation
- permanently blocking participation in severe cases

---

## Scope

This Code of Conduct applies to project spaces, including:

- GitHub issues
- pull requests
- discussions
- documentation
- code review
- project-related communication

It also applies when someone represents the project in a public setting.

---

## Beginner-Friendly Standard

EconKit should remain beginner-friendly.

That means:

- no mocking basic questions
- no gatekeeping
- no unnecessary intimidation
- no treating mistakes as personal failures
- no assuming everyone knows GitHub, Python, or econometrics already

A strong open-source project helps people improve.

---

## Professional Standard

EconKit should also remain professional.

That means:

- code should be tested
- documentation should be clear
- claims should be reasonable
- economic assumptions should be transparent
- outputs should be reproducible
- contributors should treat the project seriously

Beginner-friendly does not mean low-quality.

Professional does not mean hostile.

EconKit aims to be both.

---

## Educational Disclaimer

EconKit is designed for educational and exploratory economic analysis.

It is not:

- an official forecasting model
- a central-bank policy model
- a substitute for professional econometric software
- a source of investment advice
- a source of official policy recommendations

Contributors should preserve this distinction in code, documentation, examples, and discussion.

---

## Final Note

The best way to contribute to EconKit is to help make it:

```text
clearer
more reliable
more useful
more transparent
more educational
more professional
```

Thank you for helping build a respectful and practical economics toolkit.
