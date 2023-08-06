This is a **software design document** -- this is a living document that makes space for discussions about software design decisions as they are made in the code base.
This document is *for Developers who plan to make changes to BuildTools*.

> This document is not part of our normal development workflows -- information in this document may be outdated.

> If you are unfamiliar with BuildTools, *please review the [User Guide](../user-guide.md) before attempting to read this document.*

## Assumptions

These are our 'documented assumptions' that we can reference when making design decisions.

1. We integrate *very tightly* with `configargparse`.

## Contents

> *Note to maintainers: Try to keep this list in-sync with the project `mkdocs.yml`*

* [Development Environment](development.md) details.
* [CLI Framework documentation](cli-framework.md).
* [Ansible Results](ansible-results.md) data structure(s).
* [Refactoring](refactorings.md) to be done (or in progress).
