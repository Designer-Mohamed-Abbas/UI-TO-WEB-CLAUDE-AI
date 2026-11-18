# UI/UX audit method

Audit is **separate** from implementation. Do not change the code because of audit findings unless the user approves.

## Areas to evaluate
Alignment - spacing consistency - typography hierarchy - color contrast - visual balance - component consistency - navigation clarity - accessibility - touch-target size - information hierarchy - responsive weaknesses - user-flow problems - interaction clarity.

## Per issue
1. Issue name  2. Location (screen/component)  3. Explanation  4. Severity  5. Why it matters  6. Recommended correction

## Severity
- **Critical**: blocks a task or excludes users (unreadable contrast on key text, unreachable action, dead-end flow, target far below minimum).
- **Moderate**: hurts clarity or consistency but a user can still succeed.
- **Minor**: polish (small misalignment, inconsistent radius).

## Method
1. Measure what you can (contrast ratio from sampled colors, target sizes in the reference).
2. Mark each finding measured / inferred / estimated.
3. Cite the screen and region. No vague findings.
4. Finish with a count per severity and "No changes were applied; awaiting approval."
