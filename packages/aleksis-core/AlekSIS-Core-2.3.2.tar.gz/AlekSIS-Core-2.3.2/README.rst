AlekSIS (School Information System) — Core (Core functionality and app framework)
=================================================================================

This is the core of the AlekSIS framework and the official distribution
(see below). It bundles functionality for all apps, and utilities for
developers and administrators.

If you are looking for the AlekSIS standard distribution, i.e. the complete
software product ready for installation and usage, please visit the `AlekSIS`_
website or the distribution repository on `EduGit`_.

Features
--------

The AlekSIS core currently provides the following features:

* For users:

 * Authentication via OAuth applications
 * Configurable dashboard
 * Custom menu entries (e.g. in footer)
 * Global preferences
 * Global search
 * Group types
 * Manage announcements
 * Manage groups
 * Manage persons
 * Notifications via SMS email or dashboard
 * PWA with offline caching
 * Rules and permissions for users, objects and pages
 * Two factor authentication via Yubikey, OTP or SMS
 * User preferences
 * User registration, password changes and password reset

* For admins

 * Asynchronous tasks with celery
 * Authentication via LDAP
 * Automatic backup of database, static and media files
 * Generic PDF generation with chromium
 * OAuth2 and OpenID Connect provider support
 * Serve prometheus metrics
 * System health and data checks

* For developers

 * `aleksis-admin` script to wrap django-admin with pre-configured settings
 * Caching with Redis
 * Django REST framework for apps to use at own discretion
 * Injection of fields, methods, permissions and properties via custom `ExtensibleModel`
 * K8s compatible, read-only Docker image
 * Object-level permissions and rules with `django-guardian` and `django-rules`
 * Query caching with `django-cachalot`
 * Search with `django-haystack` and `Whoosh` backend
 * uWSGI and Celery via `django-uwsgi` in development

Licence
-------

::

  Copyright © 2017, 2018, 2019, 2020, 2021 Jonathan Weth <dev@jonathanweth.de>
  Copyright © 2017, 2018, 2019, 2020 Frank Poetzsch-Heffter <p-h@katharineum.de>
  Copyright © 2018, 2019, 2020, 2021 Julian Leucker <leuckeju@katharineum.de>
  Copyright © 2018, 2019, 2020, 2021 Hangzhi Yu <yuha@katharineum.de>
  Copyright © 2019, 2020, 2021 Dominik George <dominik.george@teckids.org>
  Copyright © 2019, 2020, 2021 Tom Teichler <tom.teichler@teckids.org>
  Copyright © 2019 mirabilos <thorsten.glaser@teckids.org>
  Copyright © 2021 Lloyd Meins <meinsll@katharineum.de>
  Copyright © 2021 magicfelix <felix@felix-zauberer.de>

  Licenced under the EUPL, version 1.2 or later, by Teckids e.V. (Bonn, Germany).

Please see the LICENCE.rst file accompanying this distribution for the
full licence text or on the `European Union Public Licence`_ website
https://joinup.ec.europa.eu/collection/eupl/guidelines-users-and-developers
(including all other official language versions).

Trademark
---------

AlekSIS® is a registered trademark of the AlekSIS open source project, represented
by Teckids e.V. Please refer to the `trademark policy`_ for hints on using the trademark
AlekSIS®.

.. _AlekSIS: https://aleksis.org
.. _European Union Public Licence: https://eupl.eu/
.. _EduGit: https://edugit.org/AlekSIS/official/AlekSIS
.. _trademark policy: https://aleksis.org/pages/about
