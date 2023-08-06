This package aims to give and easy pluggable module to provide authentication and user maintennance in a Pyramid web application.
It relies the Pyramid+SQLAlchemy+Mako stack. Implementation for other template languages is on the roadmap.


# Installation and setup

## Install the package
Install the package with:
```sh
  pip install ppss_auth
```
or put ppss_auth in your app dependencies (setup.py, in the install_requires list of packages)



To activate the package, in your main *\_\_init\_\_.py* file, inside the main function, add this line: 
```python
  config.include('ppss_auth')
```

in your models include the ppss_auth's models with this line:
```python
from ppss_auth.models import *
```



## Configure the database
This can be a zero-db-conf module:
run the app with _ppss_auth.initdb_ set to True (that is the default for the params, so you can even leave it blank: see configuration, below). You are done with this, unless you need more in-depth initialization (follow reading)


### You want to do it yourself

To init the Tables manually, in the initialization script (usually in *scripts/intializedb.py*), add this row:
```python
  from ppss_auth import (models as ppssmodels)
```

and while creating the default data (in the "with transaction.manager" block of code), use something like:
```python
  ppssmodels.initdb(dbsession,createdefault=False)
```
This creates the tables and, if *createdefault* evaulates to True, it create a default admin/admin user with the admin permission. 
Please change the password to avoid secuirity issues.


You can create some data as well. Refer to [models] section, below, for more info.

## Requirements
When a user login, *essionauthpolicy* is used to store her informations (userid and user groups). 


## ini file configuration 
ppss_auth use these info from the ini file:

*default user*
- ppss_auth.adminname - the name of a sueruser. Deafult to "admin"
- ppss_auth.adminpass - the corresponding password. If not provided the admin is not allowed to log in (with the ini credentials. It may exist in database)

*predefined permissions, groups, users*

- ppss_auth.permission_list - list of permission, one on each indented row
- ppss_auth.group_list
- ppss_auth.user_list
- ppss_auth.default_password

An example is as follow: 

```python
  ppss_auth.permission_list =
    permision1
    permision2
    permision3
  ppss_auth.group_list =
    group1=permision1,permision2
    group2=permision1
    group3=permision2
  ppss_auth.user_list=
    user1=group1,group2
    iser2=group3
  ppss_auth.default_password = temp0r4ryPassword->changeme!
```


*db stuff*
- ppss_auth.initdb [True] - true/false value, tells the lib to init db automatically on first run.


*routes*
- ppss_auth.login_url [/login] - url for login.
- ppss_auth.logout_url [/logout]- url for logout.

*where to land after succesfull login/logout*
- ppss_auth.post_login_follow - try to redirect the browser back to where it came from after successful login (use true case insensitive to activate it). It's useful if combined with the forbidden pattern
- ppss_auth.post_login_route [home] - name of the route where to send the browser after user logged in. Ignored if ppss_auth.post_login_follow is set to true AND there is a referer to go to.
- ppss_auth.post_logout_route - name of the route where to send the browser after log out. Defaults to home

*templates stuff*
You can override all this values and even provide a mako-free environment. This can be a litlle tricky, but there is no hard-coded dependency to mako, just the defaults.

- ppss_auth.logintemplate - name of the login template. It defaults to the internal template: "ppss_auth:/templates/login.mako"
- ppss_auth.changepasswordtemplate - name of the change password template. Defaults to: ppss_auth:/templates/change.mako
- ppss_auth.modifyusertemplate - Defaults to: ppss_auth:/templates/modifyuser.mako
- ppss_auth.listusertemplate - Defaults to: ppss_auth:/templates/listuser.mako
- ppss_auth.logintemplateinherit - Defaults to: ppss_auth:/templates/layout.mako


*look and feel*

- ppss_auth.bootstrapversion - Should 3 or 4, accordind to the the version of bootstrap that the hosting site uses. Defaults to 4

# Things to know (devs only)

## database
Thi package provide the creation and usage of 3 main tables (and the other tables required for ER consistency):
- ppss_user - containing basic information about the users (username, hashed password and related data )
- ppss_group - user groups to allow for easier handling of user groups and permissions
- ppss_permission - a list of permissions (just an id and a name)

## models

### PPSsuser

This represents the user of your application.
She has a _username_, a _password_ and relation to her _groups_. She also has a _enabled_ property and some timestamps (creation times, and similar times).

Use the _setPassword(password)_ method on PPSsuser instances to change the password, providing the new password.

_todict(self)_ is a commodity method to get a dict of the main properties.

### PPSsgroup

This class represnts the groups of your users. It's a many-to-many relation: each user can belong to many groups, and each group can gather many users.
Other than a _name_ and the _enabled_ flag (integer with 1 for enabled), its main user is the many-to-many relation to permissions. This means that all users in the same group share (at least) all the permissions given to the group.

### PPSspermission

This class represents the permissions of the application. You can create new permissions and link them to group. You can use those permissions in the _permission_ attribute of the _view\_config_ decorator to restrict usage of some methods using ACL, or you can check it whenever needed.
