# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: access_restriction.spec.js >> Authenticated User Access >> User can access risk page
- Location: frontend\web\tests\access_restriction.spec.js:51:3

# Error details

```
Test timeout of 60000ms exceeded while running "beforeEach" hook.
```

```
Error: apiRequestContext._wrapApiCall: ENOENT: no such file or directory, copyfile 'C:\Users\rebec\OneDrive\Documents\GitHub\cmps-357-sp26-final-project-cmps357-team-3\test-results\.playwright-artifacts-5\traces\2e8507777980310a0acc-9750056ba35eaab6c09d.network' -> 'C:\Users\rebec\OneDrive\Documents\GitHub\cmps-357-sp26-final-project-cmps357-team-3\test-results\.playwright-artifacts-5\traces\2e8507777980310a0acc-9750056ba35eaab6c09d-pwnetcopy-1.network'
```

# Page snapshot

```yaml
- main [ref=e2]:
  - generic [ref=e3]:
    - generic [ref=e4]: "404"
    - paragraph [ref=e5]: The requested path could not be found
```