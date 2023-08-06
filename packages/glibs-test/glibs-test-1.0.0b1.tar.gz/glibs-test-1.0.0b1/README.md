## glibs-test

Collection of utilities for writing tests

### What's included?

- `glibs.test.TestCase`: subclass of `unittest.TestCase` that includes some utility functions and hooks.

  - `run_patch(patcher)`: a helper function so that you can run many patches in a non-repulsive way.

    Instead of doing something like this:

    ```python
    @mock.patch(a)
    @mock.patch(b)
    # ...
    @mock.patch(z)
    def test_something(a, b, ..., z):
        # ... after a gajillion variables in the function declaration
    ```

    Or even this:

    ```python
    def test_something(a, b, ..., z):
        with mock.patch(a) as am:
            with mock.patch(b) as bm:
                # ...
                    with mock.patch(z) as zm:
                        # ... in the zillionth indentation level
    ```

    You can do this:

    ```python
    def test_something():
        mock_a = self.run_patch(mock.patch(a))
        mock_b = self.run_patch(mock.patch(b))
        # ...
        mock_z = self.run_patch(mock.patch(z))
        # way nicer, isn't it?
    ```
