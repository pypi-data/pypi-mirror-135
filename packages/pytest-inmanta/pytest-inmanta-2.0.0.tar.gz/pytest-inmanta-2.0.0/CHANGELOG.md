# v 2.0.0 (2022-01-24)
Changes in this release:
- Added support for testing v2 modules.
- Extended to be compatible with `inmanta-core>=6`
- Added support for custom `inmanta_reset_state` method to clean up stateful modules between compiles
- Ensure that projects are compiled using a separate venv.
- Fixed typing issue for `filter_args` in different method of the Project class.

## Breaking changes
- pytest-inmanta now keeps `inmanta_plugins` submodules alive across compiles. As a result, stateful modules must implement
    custom state cleanup logic as described in the README.

# v 1.6.2 (2021-08-17)
Changes in this release:
- Fixed issue with project fixture related to cleanup assumptions causing failures for `inmanta-core>=5.1.2.dev`

# v 1.6.1 (2021-06-29)
Changes in this release:
- Fixed an invalid import from inmanta-core (inmanta/inmanta-core#3074)

# v 1.6.0 (2021-06-18)
Changes in this release:
- Added the ability to assert the expected 'change' of a deploy
- Compiled models are logged (debug level), with line numbers (#199)
- Export mypy types

# v 1.5.0 (2021-03-26)
Changes in this release:
- Remove dependency on the inmanta package

# V 1.4.0 (20-10-12)
Changes in this release:
- Added meaningful error message when --venv points to a non-existing directory (#62)
- Ensure that cache is closed completely (#57)
- Fix incompatibility with pytest 6.0.0
- Fixed plugin loading compatibility with compiler's import mechanism (#46, #49)
- Added `inmanta_plugins` fixture to make abstraction of required module reloading when the compiler project is reset (related to #49)
- Added deprecation warning for `project_no_plugins` fixture in favor of `INMANTA_TEST_NO_LOAD_PLUGINS` environment variable (#66)
- Added resource unittest::IgnoreResource.
- Improve documentation of options (#67)

# V 1.3.0
Changes in this release:
- Added INMANTA_TEST_NO_LOAD_PLUGINS environment variable as workaround for inmanta/pytest-inmanta#49

# V 1.2.0
Changes in this release:
- Fixed status field on dryrun_resource (#53)
- Fixed error when running tests for module that imports other modules from its plugins
- Added project_no_plugins fixture as workaround for plugins being loaded multiple times (inmanta/pytest-inmanta#49)

# V 1.1.0
Changes in this release:
- Added --use-module-in-place option (#30)
- Added support to test regular functions and classes (#37)
- Close handler caches on cleanup (#42)

# V 1.0.0
Changes in this release:
- Added support to get logs from handler (#35)
- Added support to specify multiple --repo-path options (#38)
- Added --install_mode option

# V 0.10.0
Changes in this release:

# V 0.9.0
Changes in this release:

## Added
- Added support to retrieve scopes in project fixture.
- Test the serialization/deserialization of resources.

## Fixed
- Ensure that the project fixture doesn't leak any data across test cases.

# V 0.8.0
Changes in this release:
- Add suport for skip and fail through data global

# V 0.7.2
Changes in this release:
- Prevent IOError when using remote IO

# V 0.7.1
Changes in this release:
- Fix packaging bug

# V 0.7.0
Changes in this release:
- Various bugfixes
- Use yaml.safe_load() instead of yaml.load()
- Documentation on how to test plugins
- Add unittest handlers

# V 0.6.0
Changes in this release:
- added log serialization to deploy, to better mimic agent behavior
- added dryrun
