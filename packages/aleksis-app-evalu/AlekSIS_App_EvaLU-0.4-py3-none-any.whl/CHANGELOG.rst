Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog`_,
and this project adheres to `Semantic Versioning`_.

`0.4`_
------

Added
~~~~~

* Add option to finish evaluation before phase end to view results then.

Fixed
~~~~~

* Rule names used wrong semantic.

`0.3.2`_
--------

Fixed
~~~~~

* Fix raising of integrity errors when finishing evaluation.

`0.3.1`_
--------

Fixed
~~~~~

* When registration and registration had overlapping time periods, evaluation was not possible.

`0.3`_
------

Added
~~~~~

* [Dev] Add some automatic tests.

Fixed
~~~~~

* [BREAKING CHANGE] Use hybrid encryption for evaluation results to make it possible to properly encrypt longer results.

**Warning:** This change is not compatible with evaluation results from older versions of this app.
If you have evaluation results from older versions of this app, you will need to delete them.

`0.2`_
-------

Changed
~~~~~~~

* Allow overlapping of registration and evaluation period.

`0.1.5`_
--------

Fixed
~~~~~

* Results page failed with zero division error when no results were found.

`0.1.4`_
--------

Fixed
~~~~~

* Use only groups in matching school term for evaluation.

`0.1.3`_
--------

Fixed
~~~~~

* Migrations depended on too new migrations from Core.

`0.1.2`_
--------


Fixed
~~~~~

* Migrations didn't work due to a race condition.


`0.1.1`_
--------

Fixed
~~~~~

* Migrations didn't work due to a race condition.

`0.1`_
------

Added
~~~~~

* Initial release.


.. _Keep a Changelog: https://keepachangelog.com/en/1.0.0/
.. _Semantic Versioning: https://semver.org/spec/v2.0.0.html


.. _0.1: https://edugit.org/katharineum/AlekSIS-App-EvaLU/-/tags/0.1
.. _0.1.1: https://edugit.org/katharineum/AlekSIS-App-EvaLU/-/tags/0.1.1
.. _0.1.2: https://edugit.org/katharineum/AlekSIS-App-EvaLU/-/tags/0.1.2
.. _0.1.3: https://edugit.org/katharineum/AlekSIS-App-EvaLU/-/tags/0.1.3
.. _0.1.4: https://edugit.org/katharineum/AlekSIS-App-EvaLU/-/tags/0.1.4
.. _0.1.5: https://edugit.org/katharineum/AlekSIS-App-EvaLU/-/tags/0.1.5
.. _0.2: https://edugit.org/katharineum/AlekSIS-App-EvaLU/-/tags/0.2
.. _0.3: https://edugit.org/katharineum/AlekSIS-App-EvaLU/-/tags/0.3
.. _0.3.1: https://edugit.org/katharineum/AlekSIS-App-EvaLU/-/tags/0.3.1
.. _0.3.2: https://edugit.org/katharineum/AlekSIS-App-EvaLU/-/tags/0.3.2
.. _0.4: https://edugit.org/katharineum/AlekSIS-App-EvaLU/-/tags/0.4
