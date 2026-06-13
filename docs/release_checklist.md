# EconKit Release Checklist

Use this checklist before publishing a new EconKit release.

---

## 1. Code Quality

- [ ] Core functions run without syntax errors
- [ ] CLI runs without syntax errors
- [ ] Public functions have clear names
- [ ] Error messages are understandable
- [ ] No private data is included
- [ ] No secrets or API keys are included

---

## 2. Tests

Run:

```bash
pytest
```

Check:

- [ ] all tests pass locally
- [ ] GitHub Actions pass
- [ ] CLI smoke tests pass
- [ ] sample dataset validation passes

---

## 3. Documentation

Check:

- [ ] README is up to date
- [ ] API documentation is up to date
- [ ] CLI documentation is up to date
- [ ] examples guide is up to date
- [ ] methodology document is up to date
- [ ] changelog has a new entry

---

## 4. Examples

Run:

```bash
python examples/analyze_macro_data.py
python examples/analyze_macro_risk.py
python examples/generate_report.py
python examples/run_macro_scenarios.py
python examples/run_forecasting.py
python examples/run_regression.py
```

Check:

- [ ] all examples run
- [ ] outputs are generated
- [ ] generated reports are readable
- [ ] charts are created correctly

---

## 5. Package Metadata

Check:

- [ ] version number is updated
- [ ] license is correct
- [ ] dependencies are correct
- [ ] citation file is updated
- [ ] package description is accurate

---

## 6. Release Notes

Before release, write:

- [ ] summary of changes
- [ ] new features
- [ ] bug fixes
- [ ] breaking changes, if any
- [ ] known limitations

---

## 7. Final GitHub Check

Before announcing a release:

- [ ] repository homepage looks professional
- [ ] Actions badge is passing
- [ ] README examples are accurate
- [ ] links work
- [ ] no generated output clutter is committed accidentally
