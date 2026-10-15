# Validation — 15 October 2026

Preparation environment: 3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ], Linux-6.18.44-x86_64-with-glibc2.39.

Passed 13 behavior cases, source compilation, isolated wheel build, wheel-module byte comparison, fresh virtual-environment installation using only the built wheel and no runtime dependencies, and the installed console entry point from a temporary directory outside the checkout. The installed example checks a concrete useful result. Malformed JSON, duplicate keys, unknown fields, oversized input and a meaningful domain failure were checked with their documented exit codes. See test_behavior.py and test_installed_cli.py for runnable cases.

The preparation harness initially followed the virtual-environment Python symlink and looked for the console command globally. It was corrected to retain the venv path; the installed checks now passed using the actual installed console script. No defective domain expectation was changed to match output.

Configured remote CI repeats unit, compilation, wheel, fresh install and installed console checks on Linux Python 3.10,3.12 and3.14. Remote CI results are not yet claimed at preparation time. macOS/Windows and other Python configurations are untested. These synthetic examples establish bounded behavior, not real-world completeness or adoption. No competitor benchmark or speed claim.
