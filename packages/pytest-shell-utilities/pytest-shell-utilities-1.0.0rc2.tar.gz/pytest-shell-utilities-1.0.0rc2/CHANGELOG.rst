.. _changelog:

=========
Changelog
=========

Versions follow `Semantic Versioning <https://semver.org>`_ (`<major>.<minor>.<patch>`).

Backward incompatible (breaking) changes will only be introduced in major versions with advance notice in the
**Deprecations** section of releases.

.. towncrier-draft-entries::

.. towncrier release notes start


shell-utilities 1.0.0rc2 (2022-01-21)
=====================================

* When passed a string, cast it to ``pathlib.Path`` before ``.resolve()``ing it
* Extract ``BaseFactory`` from ``Factory``. It's required on `pytest-salt-factories`_ container
  implementation.


shell-utilities 1.0.0rc1 (2022-01-21)
=====================================

Pre-release of the first working version of the pytest plugin.


.. _pytest-salt-factories: https://github.com/saltstack/pytest-salt-factories
