.. Licensed under the Apache License, Version 2.0 (the "License");
.. you may not use this file except in compliance with the License.
.. You may obtain a copy of the License at
..
..    http://www.apache.org/licenses/LICENSE-2.0
..
.. Unless required by applicable law or agreed to in writing, software
.. distributed under the License is distributed on an "AS IS" BASIS,
.. WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
.. See the License for the specific language governing permissions and
.. limitations under the License.


.. _`Change log`:

Change log
==========


Version 0.9.0.dev1
------------------

This version contains all fixes up to version 0.8.x.

Released: not yet

**Incompatible changes:**

**Deprecations:**

**Bug fixes:**

**Enhancements:**

**Cleanup:**

**Known issues:**

* See `list of open issues`_.

.. _`list of open issues`: https://github.com/andy-maier/pytest-easy-server/issues


Version 0.8.0
-------------

Released: 2021-05-01

**Bug fixes:**

* Docs: Added missing description of pytest option '--es-encrypted' introduced
  in version 0.7.0. (issue #61)

* Test: Fixed the issue with installing the 'cryptography' package on Windows
  by increasing the minimum version of 'pip' to 21.0 on Python 3.6 and higher
  (issue #54)

**Enhancements:**

* Added support for validating the user-defined extensions in the easy-server
  server file and vault file by adding a new pytest option '--es-schema-file'
  that specifies a YAML file defining the JSON schemas for these extensions.
  (issue #62)


Version 0.7.0
-------------

Released: 2021-04-05

**Enhancements:**

* Increased development status to Beta. (issue #34)

* Added a pytest option '--es-encrypted' to the plugin that requires that the
  vault file (if specified) is encrypted. This is a safeguard against checking
  in decrypted vault files by mistake. (issue #44)

* Increased the minimum version of easy-server to 0.7.0. (related to issue #44)


Version 0.6.0
-------------

Released: 2021-04-03

Initial release.
