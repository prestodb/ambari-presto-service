Known Issues
============

* For some older versions of Presto, when attempting to ``CREATE TABLE`` or
  ``CREATE TABLE AS`` using the Hive connector, you may run into the following
  error::

    Query 20151120_203243_00003_68gdx failed: java.security.AccessControlException: Permission denied: user=hive, access=WRITE, inode="/apps/hive/warehouse/nation":hdfs:hdfs:drwxr-xr-x
        at org.apache.hadoop.hdfs.server.namenode.FSPermissionChecker.check(FSPermissionChecker.java:319)
        at org.apache.hadoop.hdfs.server.namenode.FSPermissionChecker.checkPermission(FSPermissionChecker.java:219)
        at org.apache.hadoop.hdfs.server.namenode.FSPermissionChecker.checkPermission(FSPermissionChecker.java:190)
        at org.apache.hadoop.hdfs.server.namenode.FSDirectory.checkPermission(FSDirectory.java:1771)

  To work around the issue, edit your ``jvm.config`` settings by adding the
  following property ``-DHADOOP_USER_NAME=hive``. This problem affects Presto
  ``0.115t`` but does not affect ``0.127t``. After saving your edit to
  ``jvm.config``, don't forget to restart all Presto components in order for
  the changes to take effect.

* If you decide to deploy an older version of Presto, you may have to adjust
  some setting manually. Please see [Configuring Presto](#configuring-presto)
  for an explanation of how to add custom settings. For example, the
  ``task.max-memory`` setting was deprecated in ``0.127t`` but is valid in
  ``0.115t``. Therefore, if you're installing ``0.115t`` and would like to
  change ``task.max-memory`` to something other than its default, add it as
  a custom property.

* On the Presto service home page, if you click on ``Presto workers``, you
  will get an incorrect list of workers. This is a known issue and has been
  fixed in Ambari 2.2.0.

* If the installation of Presto fails with ``Python script has been killed
  due to timeout after waiting 1800 secs``, then the ``wget`` for either the
  Presto RPM or ``presto-cli`` JAR has timed out. To increase the timeout,
  increase the ``agent.package.install.task.timeout`` setting in
  ``/etc/ambari-server/conf/ambari.properties`` on the Ambari server host.
  Make sure to restart the Ambari server for the change to take effect.
  To resume, either hit the Retry button in the installation wizard, or
  finish the wizard and then install all Presto components individually by
  navigating to the relevant host and selecting ``re-install``. The
  components can be installed manually in any order but when starting the
  components, make sure to start the Presto coordinator last. If the
  installation keeps timing out, we suggest downloading the RPM and JAR
  outside the installation process, uploading them somewhere on your network
  and editing ``package/scripts/download.ini`` with the new URLs.

* At the moment, upgrading Presto from Ambari is not possible. Even though
  Ambari provides the capability to upgrade software, we didn't get a chance
  to implement the integration. If many users request this feature
  (if you'd like to see this feature let us know by commenting on
  `this issue <https://github.com/prestodb/ambari-presto-service/issues/17>`_),
  we'll add it to the next release. To upgrade Presto without the native
  upgrade integration you have to manually uninstall Presto and then install
  the new version.