# Verso

Verso is an application aimed to simplify and standardize automatic
versioning in a continuous delivery context.

# Philosophy

The idea with Verso is to reuse part of the functionality needed in
order to implement Continuous Delivery.

The approach to continuous delivery taken is the multi-repo approach
described well in [this
blog](https://www.thoughtworks.com/insights/blog/architecting-continuous-delivery).
That is, modularization of an application is achieved by breaking out
components that lives in their own version controlled repositories,
with their own delivery pipelines. The components are released to a
binary repository, such as Artifactory or Nexus. The dependencies to
the components may be resolved at various stages depending on the type
of component. In the case of a library the dependency typically is
resolved at build time of the dependent application, by the use of a
dependency manager, such as Maven, Pip, or Conan. In the case of a
service the components are instead resolved at deploy time.

In order to encourage modularization it is important to reduce the
friction involved in creating individual release pipelines for each
component. Likewise, it is also important to minimize the friction and
lead time involved by this multi-repo approach; multi-repo approaches
typically require multiple changes in order for a fix or feature to
end up in production. The suggested approach is to automate versioning
and releases of components, both for staging and trunk (trunk-based
development is favored). Releasing for staging means releasing
candidates for each proposed change (a proposed change is typically
subject to a review, for example pull requests or change
sets). Releasing for trunk means releasing an approved change.

Automatic versioning a component can be solved is various ways, but
the approach suggested with this project is to use a SemVer-like
approach. Depending on the ambition of the user, the approach can
potentially be everything from SemVer to SemVer-like. The reason to
use a SemVer-like approach is to let dependency management look
elegant and conventional. One thing that SemVer for example supports
is the ability to identify the generation of a component, which
simplifies understanding. It can be argued that true SemVer (including
the distinction between major, minor, and patch versions), is
sometimes over-kill for components, at least in small settings, hence
the sloppy interpretation of SemVer.

# Design

The design of this project is not carved in stone. It is not obvious
what to generalize and what to leave to the user to
specialize. Different users could have different source code
management (such as Git, Mercurial or Subversion), different binary
repositories (such as Artifactory or Nexus), and different release
formats (such as Maven, Wheel, Npm, Conan). But one thing is sure, it
is not advisable to implement the same functionality over and over
again for every project that needs to be versioned and released. In
order to maintain a SemVer-like versioning, the version must be
incremented, and valid versions must be distinguished from invalid
ones, and that kind of functionality is not trivial.

Since a SemVer-like versioning has an order, the current version must
somehow be stored; a state must be maintained. How this state is
implemented is a matter of design. One can think of a state maintained
by a binary repository or some database. In this project the source
code management is used. Following the YAGNI design principle, Git
will be used, and only Git. Supporting more version control systems
could be a future improvement of this project. Using tags of Git is
actually quite convenient since several birds are killed with one
stone; tagging revisions that releases are based on is graceful.

# Future improvements

The current design automatically maintains the patch version while the
major and minor part of the version is more or less permanent. A nice
improvement would be to combine the automatic state with a state
maintained by writing change log items in a CHANGELOG file. That way
we would both have nice release notes and automatic versioning. The
major could for example be identified by the CHANGELOG file, and the
patch version could be automatically maintained. Using this approach
would actually allow users to maintain a pure SemVer versioning by
allowing users to write change logs for major and minors, while still
use an automated versioning for patch versions.

# Etymology

The name `Verso` is the result of playing with the word `version`, the
literal meaning of the Italian word `verso` meaning `towards` in
English.

# Contributions

Contributions are welcome. All functionality must be covered by tests.

# Prerequisites

In order to test application locally Docker and Make must be
installed.

# How to test application

Testing of Verso makes use of Make as a task runner. The following
command runs all tests.

    make test

# How to release application

    VERSION=X.Y.Z make upload-test
    VERSION=X.Y.Z make upload-prod
