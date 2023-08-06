Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog`_,
and this project adheres to `Semantic Versioning`_.

`2.0.1`_ - 2022-01-21
---------------------

Changed
~~~~~~~

* ``get_feeds`` task is now automatically scheduled every 10 minutes

Fixed
~~~~~

* Add admin docs.

`2.0`_ - 2021-10-30
-------------------

Changed
~~~~~~~

* German translations were updated.

`2.0rc1`_ - 2021-06-23
----------------------

Changed
~~~~~~~

* Increase cache time for events to one hour.

Fixed
~~~~~

* Don't delete cache if there was an error while receiving the events.

`2.0b0`_ - 2021-05-21
---------------------

Changed
~~~~~~~

* RSS sources now get automatically deleted if their respective widget gets deleted.

Fixed
~~~~~

* All-day events were displayed one day too long.
* Invalid iCal data broke the iCal widget.

`2.0a2`_ - 2020-05-04
---------------------

Added
~~~~~

* Allow adding iCal widgets to dashboard
* Allow adding RSS widgets to dashboard

----------


.. _Keep a Changelog: https://keepachangelog.com/en/1.0.0/
.. _Semantic Versioning: https://semver.org/spec/v2.0.0.html


.. _2.0a2: https://edugit.org/AlekSIS/Official/AlekSIS-App-DashboardFeeds/-/tags/2.0a2
.. _2.0b0: https://edugit.org/AlekSIS/Official/AlekSIS-App-DashboardFeeds/-/tags/2.0b0
.. _2.0rc1: https://edugit.org/AlekSIS/Official/AlekSIS-App-DashboardFeeds/-/tags/2.0rc1
.. _2.0: https://edugit.org/AlekSIS/Official/AlekSIS-App-DashboardFeeds/-/tags/2.0
.. _2.0.1: https://edugit.org/AlekSIS/Official/AlekSIS-App-DashboardFeeds/-/tags/2.0.1
