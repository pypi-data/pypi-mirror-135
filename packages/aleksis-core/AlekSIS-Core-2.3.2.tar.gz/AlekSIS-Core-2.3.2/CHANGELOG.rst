Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog`_,
and this project adheres to `Semantic Versioning`_.

`2.3.2`_ – 2021-12-20
---------------------

Added
~~~~~

* Allow configuration of database options

Fixed
~~~~~

* Correctly update theme colours on change again
* Use correct favicon as default AlekSIS favicon
* Show all years in a 200 year range around the current year in date pickers

Removed
~~~~~~~

* Remove old generated AlekSIS icons
* Imprint is now called "Imprint" and not "Impress".
* Logo files weren't uploaded to public namespace.

`2.3.1`_ – 2021-12-17
---------------------

Fixed
~~~~~

* Small files could fail to upload to S3 storage due to MemoryFileUploadHandler
* Corrected typos in previous changelog

`2.3`_ – 2021-12-15
-------------------

Added
~~~~~

* [OAuth] Allow apps to fill in their own claim data matching their scopes

Fixed
~~~~~

* View for assigning permissions didn't work with some global permissions.
* PDFs generated in background didn't contain logo or site title.
* Admins were redirected to their user preferences
  while they wanted to edit the preferences of another user.
* Some CharFields were using NULL values in database when field is empty
* Optional dependecy `sentry-sdk` was not optional

Changed
~~~~~~~

* Docker base image ships PostgreSQL 14 client binaries for maximum compatibility
* Docker base image contains Sentry client by default (disabled in config by default)

Removed
~~~~~~~

* Remove impersonation page. Use the impersonation button on the person
  detail view instead.

`2.2.1`_ – 2021-12-02
--------------------

Fixed
~~~~~

* [Docker] Stop initialisation if migrations fail
* [OAuth] Register `groups` scope and fix claim
* [OAuth] Fix OAuth claims for follow-up requests (e.g. UserInfo)
* [OAuth] Fix grant types checking failing on wrong types under some circumstances
* [OAuth] Re-introduce missing algorithm field in application form
* Remove errornous backup folder check for S3

`2.2`_ - 2021-11-29
-------------------

Added
~~~~~

* Support config files in sub-directories
* Provide views for assigning/managing permissions in frontend
* Support (icon) tabs in the top navbar.

Changed
~~~~~~~

* Update German translations.

Fixed
~~~~~

* Use new MaterializeCSS fork because the old version is no longer maintained.
* Sender wasn't displayed for notifications on dashboard.
* Notifications and activities on dashboard weren't sorted from old to new.

`2.1.1`_ - 2021-11-14
---------------------

Added
~~~~~

* Provide ``SITE_PREFERENCES`` template variable for easier and request-independent access on all site preferences.

Fixed
~~~~~

* Make style.css and favicons cachable.
* Import model extensions from other apps before form extensions.
* Recreate backwards compatiblity for OAuth URLs by using ``oauth/`` again.
* Show correct logo and school title in print template if created in the background.

Removed
~~~~~~~

* Remove fallback code from optional Celery as it's now non-optional.

`2.1`_ - 2021-11-05
-------------------

Added
~~~~~

* Provide an ``ExtensiblePolymorphicModel`` to support the features of extensible models for polymorphic models and vice-versa.
* Implement optional Sentry integration for error and performance tracing.
* Option to limit allowed scopes per application, including mixin to enforce that limit on OAuth resource views
* Support trusted OAuth applications that leave out the authorisation screen.
* Add birthplace to Person model.

Changed
~~~~~~~

* Replace dev.sh helper script with tox environments.
* OAuth Grant Flows are now configured system-wide instead of per app.
* Refactor OAuth2 application management views.

Fixed
~~~~~

* Fix default admin contacts

Credits
~~~~~~~

* We welcome new contributor 🐧 Jonathan Krüger!
* We welcome new contributor 🐭 Lukas Weichelt!

`2.0`_ - 2021-10-29
-------------------

Changed
~~~~~~~

* Refactor views/forms for creating/editing persons.

Fixed
~~~~~

* Fix order of submit buttons in login form and restructure login template
  to make 2FA work correctly.
* Fix page title bug on the impersonate page.
* Users were able to edit the linked user if self-editing was activated.
* Users weren't able to edit the allowed fields although they were configured correctly.
* Provide `style.css` and icon files without any authentication to avoid caching issues.


Removed
~~~~~~~

* Remove mass linking of persons to accounts, bevcause the view had performance issues,
  but was practically unused.

`2.0rc7`_ - 2021-10-18
----------------------

Fixed
~~~~~

* Configuration mechanisms for OpenID Connect were broken.
* Set a fixed version for django-sass-processor to avoid a bug with searching ``style.css`` in the wrong storage.
* Correct the z-index of the navbar to display the main title again on mobile devices.

Removed
~~~~~~~

* Leftovers from a functionality already dropped in the development process
  (custom authentication backends and alternative login views).

`2.0rc6`_ - 2021-10-11
----------------------

Added
~~~~~

* OpenID Connect scope and accompanying claim ``groups``
* Support config files in JSON format
* Allow apps to dynamically generate OAuth scopes

Changed
~~~~~~~

* Do not log or e-mail ALLOWED_HOSTS violations
* Update translations.
* Use initial superuser settings as default contact and from addresses

Fixed
~~~~~

* Show link to imprint in footer
* Fix API for adding OAuth scopes in AppConfigs
* Deleting persons is possible again.
* Removed wrong changelog section

Removed
~~~~~~~

* Dropped data anonymization (django-hattori) support for now
* ``OAUTH2_SCOPES`` setting in apps is not supported anymore. Use ``get_all_scopes`` method
  on ``AppConfig`` class instead.

`2.0rc5`_ - 2021-08-25
----------------------

Fixed
~~~~~

* The view for getting the progress of celery tasks didn't respect that there can be anonymous users.
* Updated django to latest 3.2.x


`2.0rc4`_ - 2021-08-01
----------------------

Added
~~~~~

* Allow to configure port for prometheus metrics endpoint.

Fixed
~~~~~

* Correctly deliver server errors to user
* Use text HTTP response for serviceworker.js insteas of binary stream
* Use Django permission instead of rule to prevent performance issues.

`2.0rc3`_ - 2021-07-26
----------------------

Added
~~~~~

* Support PDF generation without available request object (started completely from background).
* Display a loading animation while fetching search results in the sidebar.

Fixed
~~~~~

* Make search suggestions selectable using the arrow keys.

Fixed
~~~~~

* Use correct HTML 5 elements for the search frontend and fix CSS accordingly.

`2.0rc2`_ - 2021-06-24
---------------------

Added
~~~~~

* Allow to install system and build dependencies in docker build


`2.0rc1`_ - 2021-06-23
----------------------

Added
~~~~~

* Add option to disable dashboard auto updating as a user and sitewide.

Changed
~~~~~~~

* Use semantically correct html elements for headings and alerts.

Fixed
~~~~~

* Add missing dependency python-gnupg
* Add missing AWS options to ignore invalid ssl certificates

`2.0b2`_ - 2021-06-15
--------------------

Added
~~~~~~~

* Add option to disable dashboard auto updating as a user and sitewide.

Changed
~~~~~~~

* Add verbose names for all preference sections.
* Add verbose names for all openid connect scopes and show them in grant
  view.
* Include public dashboard in navigation
* Update German translations.

Fixed
~~~~~

* Fix broken backup health check
* Make error recovery in about page work

Removed
~~~~~~~

* Drop all leftovers of DataTables.

`2.0b1`_ - 2021-06-01
---------------------

Changed
~~~~~~~

* Rename every occurance of "social account" by "third-party account".
* Use own templates and views for PWA meta and manifest.
* Use term "application" for all authorized OAuth2 applications/tokens.
* Use importlib instead of pkg_resources (no functional changes)

Fixed
~~~~~

* Fix installation documentation (nginx, uWSGI).
* Use a set for data checks registry to prevent double entries.
* Progress page tried to redirect even if the URL is empty.

Removed
~~~~~~~

* Drop django-pwa completely.

`2.0b0`_ - 2021-05-21
---------------------

Added
~~~~~

* Allow defining several search configs for LDAP users and groups
* Use setuptools entrypoints to find apps
* Add django-cachalot as query cache
* Add ``syncable_fields`` property to ``ExtensibleModel`` to discover fields
  sync backends can write to
* Add ``aleksis-admin`` script to wrap django-admin with pre-configured settings
* Auto-create persons for users if matching attributes are found
* Add ``django-allauth`` to allow authentication using OAuth, user registration,
  password changes and password reset
* Add OAuth2 and OpenID Connect provider support
* Add ``django-uwsgi`` to use uWSGI and Celery in development
* Add loading page for displaying Celery task progress
* Implement generic PDF generation using Chromium
* Support Amazon S3 storage for /media files
* Enable Django REST framework for apps to use at own discretion
* Add method to inject permissions to ExtensibleModels dynamically
* Add helper function which filters queryset by permission and user
* Add generic support for Select 2 with materialize theme
* Add simple message that is shown whenever a page is served from the PWA cache
* Add possibility to upload files using ckeditor
* Show guardians and children on person full page
* Manage object-level permissions in frontend
* Add a generic deletion confirmation view
* Serve Prometheus metrics from app
* Provide system health check endpoint and checks for some components
* Add impersonate button to person view
* Implement a data check system for sanity checks and guided resolution of inconsistencies
* Make the dashboard configurable for users and as default dashboard by admins
* Support dynamic badges in menu items
* Auto-delete old /media files when related model instance is deleted
* Add SortableJS
* Add a widget for links/buttons to other websites

Changed
~~~~~~~

* Make Redis non-optional (see documentation)
* Use Redis as caching and session store to allow horizontal scaling
* Enable PostgreSQL connection pooling
* Use uWSGI to serve /static under development
* Use a token-secured storage as default /media storage
* Rewrite Docker image to serve as generic base image for AlekSIS distributions
* Make Docker image run completely read-only
* Ensure Docker image is compatible with K8s
* Remove legacy file upload functoin; all code is required to use the storage API
* Default search index backend is now Whoosh with Redis storage
* Re-style search result page
* Move notifications to separate page with indicator in menu
* Move to ``BigAutoField`` for all AlekSIS apps
* Require Django 3.2 and Python 3.9
* Person and group lists can now be filtered
* Allow displaying the default widget to anonymous users

Fixed
~~~~~

* Correct behavious of celery-beat in development
* Fix precaching of offline fallback page
* Use correct styling for language selector
* Rewrite notification e-mail template for AlekSIS
* Global search now obeys permissions correctly
* Improve performance of favicon generation
* Dashboard widgets now handle exceptions gracefully
* Roboto font was not available for serving locally

Removed
~~~~~~~

* Dropped support for other search backends than Whoosh
* Drop django-middleware-global-request completely

`2.0a2`_ - 2020-05-04
---------------------

Added
~~~~~

* Frontend-ased announcement management.
* Auto-create Person on User creation.
* Select primary group by pattern if unset.
* Shortcut to personal information page.
* Support for defining group types.
* Add description to Person.
* age_at method and age property to Person.
* Synchronise AlekSIS groups with Django groups.
* Add celery worker, celery-beat worker and celery broker to docker-compose setup.
* Global search.
* License information page.
* Roles and permissions.
* User preferences.
* Additional fields for people per group.
* Support global permission flags by LDAP group.
* Persistent announcements.
* Custom menu entries (e.g. in footer).
* New logo for AlekSIS.
* Two factor authentication with Yubikey, OTP or SMS.
* Devs: Add ExtensibleModel to allow apps to add fields, properties.
* Devs: Support multiple recipient object for one announcement.

Changes
~~~~~~~

* Make short_name for group optional.
* Generalised live loading of widgets for dashboard.
* Devs: Add some CSS helper classes for colours.
* Devs: Mandate use of AlekSIS base model.
* Devs: Drop import_ref field(s); apps shold now define their own reference fields.

Fixed
~~~~~

* DateTimeField Announcement.valid_from received a naive datetime.
* Enable SASS processor in production.
* Fix too short fields.
* Load select2 locally.

`2.0a1`_ - 2020-02-01
---------------------

Added
~~~~~

* Migrate to MaterializeCSS.
* Dashboard.
* Notifications via SMS (Twilio), Email or on the dashboard.
* Admin interface.
* Turn into installable, progressive web app.
* Devs: Background Tasks with Celery.

Changed
~~~~~~~

* Customisable save_button template.
* Redesign error pages.

Fixed
~~~~~

* setup_data no longer forces database connection.

`1.0a4`_ - 2019-11-25
---------------------

Added
~~~~~

* Two-factor authentication with TOTP (Google Authenticator), Yubikey, SMS
  and phone call.
* Devs: CRUDMixin provides a crud_event relation that returns all CRUD
  events for an object.

`1.0a2`_ - 2019-11-11
---------------------

Added
~~~~~

* Devs: Add ExtensibleModel to allow injection of methods and properties into models.


`1.0a1`_ - 2019-09-17
---------------------

Added
~~~~~

* Devs: Add API to get an audit trail for any school-related object.
* Devs: Provide template snippet to display an audit trail.
* Devs: Provide base template for views that allow browsing back/forth.
* Add management command and Cron job for full backups.
* Add system status overview page.
* Allow enabling and disabling maintenance mode from frontend.
* Allow editing the dates of the current school term.
* Add logo to school information.
* Allow editing school information.
* Ensure all actions are reverted if something fails (atomic requests).

Fixed
~~~~~

* Only show active persons in group and persons views.
* Silence KeyError in get_dict template tag.
* Use bootstrap buttons everywhere.

.. _Keep a Changelog: https://keepachangelog.com/en/1.0.0/
.. _Semantic Versioning: https://semver.org/spec/v2.0.0.html

.. _1.0a1: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/1.0a1
.. _1.0a2: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/1.0a2
.. _1.0a4: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/1.0a4
.. _2.0a1: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/2.0a1
.. _2.0a2: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/2.0a2
.. _2.0b0: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/2.0b0
.. _2.0b1: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/2.0b1
.. _2.0b2: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/2.0b2
.. _2.0rc1: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/2.0rc1
.. _2.0rc2: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/2.0rc2
.. _2.0rc3: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/2.0rc3
.. _2.0rc4: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/2.0rc4
.. _2.0rc5: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/2.0rc5
.. _2.0rc6: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/2.0rc6
.. _2.0rc7: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/2.0rc7
.. _2.0: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/2.0
.. _2.1: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/2.1
.. _2.1.1: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/2.1.1
.. _2.2: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/2.2
.. _2.2.1: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/2.2.1
.. _2.3: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/2.3
.. _2.3.1: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/2.3.1
.. _2.3.2: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/2.3.2
