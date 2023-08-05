Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog`_,
and this project adheres to `Semantic Versioning`_.

`2.1`_ - 2022-01-17
-------------------

Added
~~~~~

* Add RegEx field type for parsing CSV fields to multiple DB fields.
* Add field type to parse a combined street and housenumber.
* Add field type to set an owner of a person's primary group by its short name.
* Add support for synchronously running the import using the management command.
* Support uploading template definitions as YAML files through the frontend.
* Add overview of all registered import templates in frontend.
* Register string functions lstrip, rstrip, strip, capitalise, lower, upper, and title
  as converters
* Allow defining one or multiple converters in templates

Changed
~~~~~~~

* Use YAML for configuration of (default) import templates.
* Extend the field type API using getters to make attributes more dynamic.
* Don't limit the import on specific models.
* Support adding domains to local parts of email addresses.
* Unclearly used ``is_active`` flag for ``Person`` model was removed
* Use phone number country code setting from AlekSIS-Core.
* Update German translations.

Fixed
~~~~~

* Management commands like ``collectstatic`` now work with no database being configured.
* Import failed when phone numbers weren't exactly valid (e. g. a missing number).
* Field type ``primary_group_by_short_name`` failed on non-existing group.
* Match field types ignored the priority settings.
* Data in match field types weren't used for the import if not used for match.
* Fixed argument parsing for management command
* First column of CSV files could not be imported
* Celery task wasn't correctly registered.
* Management command wasn't usable due to missing arguments.
* Add documentation.

Removed
~~~~~~~

* Drop TOML support for configuration of (default) import templates.

`2.0`_ - 2021-12-20
-------------------

Nothing changed.

`2.0rc2`_ - 2021-07-23
----------------------

Fixed
~~~~~

* Drop usage of no longer existing method ``get_subject_by_short_name``.

`2.0rc1`_ - 2021-06-23
----------------------

Fixed
~~~~~

* Preference section verbose names were displayed in server language and not
  user language (fixed by using gettext_lazy).
* Fix distribution name discovery for AlekSIS about page


`2.0b1`_ - 2021-06-01
---------------------

Changed
~~~~~~~

* Make Chronos optional:
  * Department group creation works without Chronos now.

`2.0b0`_ - 2021-05-21
---------------------

Added
~~~~~

* Introduce a generic, customisable CSV importer based on import templates and field types.
* Add import templates for Pedasos (students, teachers, classes, courses, parents).

Removed
~~~~~~~

* Remove integrated support for Schild-NRW import due to missing testing options.

`1.0a2`_ - 2019-11-11
---------------------

Fixed
~~~~~

* Handle PhoneNumberParseErrors gracefully.


`1.0a1`_ - 2019-09-17
---------------------

New features
~~~~~~~~~~~~

* Deactivate persons that are set to inactive in SchILD.

Changed
~~~~~~~

* Show number of created and deactivated persons after import.

Fixed
~~~~~

* Use bootstrap buttons everywhere.

.. _Keep a Changelog: https://keepachangelog.com/en/1.0.0/
.. _Semantic Versioning: https://semver.org/spec/v2.0.0.html

.. _1.0a1: https://edugit.org/Teckids/AlekSIS/AlekSIS-App-CSVImport/-/tags/1.0a1
.. _1.0a2: https://edugit.org/Teckids/AlekSIS/AlekSIS-App-CSVImport/-/tags/1.0a2
.. _2.0b0: https://edugit.org/Teckids/AlekSIS/AlekSIS-App-CSVImport/-/tags/2.0b0
.. _2.0b1: https://edugit.org/Teckids/AlekSIS/AlekSIS-App-CSVImport/-/tags/2.0b1
.. _2.0rc1: https://edugit.org/Teckids/AlekSIS/AlekSIS-App-CSVImport/-/tags/2.0rc1
.. _2.0rc2: https://edugit.org/Teckids/AlekSIS/AlekSIS-App-CSVImport/-/tags/2.0rc2
.. _2.0: https://edugit.org/Teckids/AlekSIS/AlekSIS-App-CSVImport/-/tags/2.0
.. _2.1: https://edugit.org/Teckids/AlekSIS/AlekSIS-App-CSVImport/-/tags/2.1
