rpmspecs-darling
^^^^^^^^^^^^^^^^

This is the RPM spec files that I have created for darling, which is a macOS translation layer for Linux.

.. contents::

Information
-----------

**Note:** I am not responsible for system damages, break-ins, or faulty code of the software that can cause the formerly listed. Always develop and test in an isolated environment at all times. **Always keep SELinux enabled.**

Frequently Asked Questions
--------------------------

There already is an RPM spec, why this one?
+++++++++++++++++++++++++++++++++++++++++++

While the RPM seems to get the build correct, it is not completely conforming to the Fedora packaging guidelines. This spec file is to bring conformity. One thing in particular their spec does incorrectly is the versioning. Because they do not have 'releases', the version must be a 0 and the release number has to be the date of their last commit and the commit sha. The BuildRequires were also changed in attempt to use pkgconfig, as recommended by Fedora.

This also will have automatic builds in copr on commit just like my other git repos.

Do you have any SRPMS available?
++++++++++++++++++++++++++++++++

They'll normally be available from my copr builds, if you are interested in making changes and using mock for yourself.

Have any documentation or guides?
+++++++++++++++++++++++++++++++++

If you're starting out rpm packaging, please consider reading the following documentation. The packaging guidelines may seem strict, but they are deemed best practices if you are considering on being a package maintainer (sponsored or not).

`FHS <http://www.pathname.com/fhs/>`_

`Fedora: Fedora Packaging Guidelines <https://fedoraproject.org/wiki/Packaging:Guidelines>`_

`Fedora: How to create an RPM package <https://fedoraproject.org/wiki/How_to_create_an_RPM_package>`_

What you should get from the above is there are specific guidelines that should be followed, for maintainability, portability, and easy review. My RPM specs will have an FAQ of the "purpose". 

Do you have any repositories?
+++++++++++++++++++++++++++++

Yes, I do.

`Copr <https://copr.fedorainfracloud.org/coprs/nalika/>`_

Do you take requests?
+++++++++++++++++++++

I normally don't. But, if what you're asking for doesn't have an RPM or project in copr, I'll consider it based on what it is, and if it fits licensing and guidelines. You can drop me an email or a line here and I will get back to you.

Do you package for other systems?
+++++++++++++++++++++++++++++++++

At this present time, I do not. I have considered packaging for OpenSUSE. However OpenSUSE, much like Arch, already have plenty of maintainers with tons upon tons of packages (up to date or not) and their own build systems similar to Fedora. So some of the packages you may see here may already exist for those distributions in base or extra repositories they provide. The COPR build system does support OpenSUSE now, so it may end up being a viable option in the future.

Presently, this does not build in copr for OpenSUSE, simply because dependencies are not in the SUSE base. I do not have a way to extend copr to the additional repositories.

.. rubric:: Footnotes

.. [#f1] https://wiki.centos.org/About/Product
