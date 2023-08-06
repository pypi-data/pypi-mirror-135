# `optimism`

A very small & simple unit-testing framework designed to provide all the
basic necessities to beginner programmers as simply as possible.

Designed by Peter Mawhorter.


## Dependencies

Works on Python versions 3.8 and up, with 3.9+ recommended.


## Installing

To install from PyPI, run the following command on the command-line:

```sh
python3 -m pip install optimism
```

Once it's installed, you can run the tests using:

```sh
TODO
```

## Usage

Use the `testCase` function to establish an expression as a test case.
Then use the `expectResult`, `expectOutputContains`, and/or
`expectCustom` functions to establish expectations for that test. Use
`provideInput` and/or `captureOutput` and related functions to deal with
input/output testing. Use `runFile` to create a test for an entire file.

See [the
documentation](https://cs.wellesley.edu/~pmwh/optimism/docs/optimism)
for more details on how to use it and what each function does.

## Changelog

- Version 2.0 creates a less fragile test-case API while streamlining the
  expectations API to focus on values only. `expect` now takes an
  expression and expected value together as two arguments, and `testCase`
  isn't needed. `expectType` was also added to encourage thinking about
  types. These functions are now intended to be used for debugging rather
  than testing. There are new `testFunction`, `testFile`, and `testBlock`
  functions which create `TestManager` objects that have a `case` method
  to derive `TestCase` objects. Those objects have `checkResult` and
  `checkOutputLines` methods, as well as `provideInputs`. Now that we're
  in control of running tests, the old input/output capturing/mocking
  functions are mostly removed (they were quite confusing to students).
  The new test case API does require the use of methods, but as a result
  it can avoid the following:
      1. The use of tuples to specify arguments
      2. The specification of arguments where one argument is an extra
         argument to specify the test case
      3. The use of behind-the-scenes magic to remember the current test
         case (students were confused and it encourages bad mental
         models).
      4. The use of triple-quoted strings for specifying input or output
         (too hard to get newlines right at the start and end).
