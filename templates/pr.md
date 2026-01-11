# PR Template

## Title Format
`[TYPE] Brief description (max 72 chars)`

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`

Example: `feat(notifications): add WebSocket real-time delivery`

---

## Description

### What does this PR do?
Brief summary of the changes (2-3 sentences).

### Why are we doing this?
Link to feature document, issue, or task:
- **Feature:** [Feature Name](link)
- **Task:** [Task ID](link)
- **Issue:** Closes #123

### How does it work?
High-level explanation of the approach taken.

---

## Type of Change

- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)
- [ ] Performance improvement
- [ ] Configuration change

---

## Changes Made

### Added
- New feature X
- New endpoint Y
- New component Z

### Changed
- Modified behavior of A
- Updated logic in B

### Removed
- Deprecated function C
- Unused code D

### Fixed
- Bug in E
- Edge case in F

---

## Testing

### Tests Added/Updated
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] E2E tests added/updated
- [ ] Manual testing completed

### Test Coverage
- **Before:** XX%
- **After:** XX%
- **Target:** ≥90% for new code

### How to Test
1. Step-by-step instructions to verify changes
2. Expected behavior
3. Edge cases to check

---

## Screenshots / Demos

<!-- If UI changes, include before/after screenshots -->
<!-- If API changes, include request/response examples -->

**Before:**
[Screenshot or description]

**After:**
[Screenshot or description]

---

## Performance Impact

- [ ] No performance impact
- [ ] Performance improved (provide metrics)
- [ ] Potential performance impact (document and justify)

**Metrics:**
- Response time: before vs after
- Memory usage: before vs after
- Database queries: count and duration

---

## Security Considerations

- [ ] No security impact
- [ ] Security review required
- [ ] Involves user data (PII)
- [ ] Authentication/authorization changes
- [ ] Input validation added/updated
- [ ] No secrets in code or commits

**Security checklist:**
- [ ] Input validation on all user inputs
- [ ] Output encoding to prevent XSS
- [ ] No SQL injection vulnerabilities
- [ ] Proper error handling (no info leakage)
- [ ] Secrets stored securely (not in code)

---

## Database Changes

- [ ] No database changes
- [ ] Migration included (backward compatible)
- [ ] Migration tested with production-size data
- [ ] Rollback migration included
- [ ] Indexes added for new queries

**Migration details:**
- Schema changes: [describe]
- Data backfill needed: Yes/No
- Estimated duration: X minutes

---

## Breaking Changes

- [ ] No breaking changes
- [ ] Breaking changes (list below)

**If breaking changes:**
- What breaks: [describe]
- Migration path: [how users/systems adapt]
- Deprecation notice: [when and how communicated]

---

## Rollback Plan

**How to rollback if this causes issues:**
1. Step 1
2. Step 2
3. Step 3

**Data rollback (if applicable):**
- How to restore data if needed

**Monitoring:**
- Metrics to watch post-deploy
- Alert thresholds

---

## Dependencies

### Requires
- [ ] Dependency A deployed first
- [ ] Configuration change B
- [ ] Infrastructure change C

### Enables
- [ ] Feature D can now be implemented
- [ ] Task E unblocked

---

## Deployment Notes

### Pre-deployment
- [ ] Database migration ready
- [ ] Configuration updated in environments
- [ ] Feature flags configured
- [ ] Monitoring dashboard ready

### Deployment Order
1. Database migration (if applicable)
2. Backend deployment
3. Frontend deployment
4. Verification steps

### Post-deployment
- [ ] Smoke tests passed
- [ ] Metrics look normal
- [ ] No errors in logs
- [ ] Feature flag enabled (if applicable)

---

## Documentation

- [ ] Code comments added for complex logic
- [ ] API documentation updated
- [ ] README updated
- [ ] User guide updated
- [ ] Runbook updated (if operational impact)
- [ ] ADR created (if architectural decision)

**Documentation links:**
- API docs: [link]
- User guide: [link]
- Runbook: [link]

---

## Review Checklist

### Code Quality (for author)
- [ ] Code follows project style guide
- [ ] No console.log or debug code
- [ ] No commented-out code
- [ ] No TODOs without issue references
- [ ] Functions are small and focused
- [ ] Variables have meaningful names
- [ ] Complex logic has comments

### Testing (for author)
- [ ] All tests pass locally
- [ ] New tests cover edge cases
- [ ] Manual testing completed
- [ ] Performance tested (if applicable)

### Documentation (for author)
- [ ] PR description is clear and complete
- [ ] Commit messages follow conventions
- [ ] Code is self-documenting or commented
- [ ] Related docs updated

### For Reviewers
Review against:
- [ ] **Correctness:** Does it work as intended?
- [ ] **Design:** Is this the right approach?
- [ ] **Readability:** Is code easy to understand?
- [ ] **Tests:** Are tests adequate?
- [ ] **Performance:** Any concerns?
- [ ] **Security:** Any vulnerabilities?
- [ ] **Edge cases:** Are they handled?

---

## Review Notes

<!-- Reviewers: Add your comments, questions, and feedback here -->

---

## Checklist Before Merge

- [ ] All CI checks passing
- [ ] Required approvals obtained (minimum 1, or 2 for breaking changes)
- [ ] All review comments addressed or discussed
- [ ] Documentation updated
- [ ] Tests passing (unit, integration, E2E)
- [ ] No merge conflicts
- [ ] Commits squashed (if needed)
- [ ] Deployment plan confirmed

---

**Author:** @username  
**Reviewers:** @reviewer1, @reviewer2  
**Created:** YYYY-MM-DD  
**Target merge:** YYYY-MM-DD  
**Related PRs:** #123, #456
