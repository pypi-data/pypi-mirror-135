Installing apps into development environment
============================================

Officially bundled apps
-----------------------

Officially bundled apps are available in the ``apps/official/``
sub-folder of the meta repository. If you followed the documentation, they
will already be checked out in the version required for the bundle you
are running.

Installing apps into the existing virtual environment of `AlekSIS-Core` can
be easily done after starting `poetry shell`::

  poetry install

Do not forget to run the maintenance tasks described earlier after
installing any app.

**Heads up:** This is not suitable for working on the core, because it
will install the `AlekSIS-Core` version used by the app using `pip` again.
