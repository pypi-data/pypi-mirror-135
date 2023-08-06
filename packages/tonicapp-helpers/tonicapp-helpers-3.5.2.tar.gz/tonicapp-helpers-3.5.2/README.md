# Helpers

## Requirements
* Python
* Django>=3.2.2,<4.0
* Django Rest Framework


## Installation

```
$ pip install tonicapp-helpers
```

Add the application to your project's `INSTALLED_APPS` in `settings.py`.

```
INSTALLED_APPS = [
    ...
    'helpers',
]
```


## Source

```
https://pypi.org/project/tonicapp-helpers/
```


## Update Library

```
python3 setup.py sdist
```

```
python3 -m twine upload dist/*
Enter your username: ******
Enter your password: ******
```


# Version updates
From v1.0 to v2.0 the support to drf_spectacular library was removed (the file schema_parameters was removed).


## V2.2.0
Support for views with two different routes. (This should be depecrated in the future)
Support for personalized serializers in requests.

## V2.2.1
Bugfix in permissions when user_id or id not exist

## V2.3.1
Change logger.info to logger.debug in middleware locale.

## V2.4.1
Add CUSTOM_WEB_TOKEN to authentication and IsCustomUserPermission to permissions.

## V2.4.2
Bugfix the prefix match

## V2.4.4
Bugfix the authentication

## V2.5.4
Support to duplications in locale and software type middleware

## V2.6.4
Create new permission: IsAuthenticated

## V2.6.5
In authentication create alternative to run tests

## V2.7.5
Improve the documentation.

## V2.7.6
Bugfix in documentation

## V2.8.6
Add personalized query params to documentation

## V2.9.6
Update information about custom_schemas

## V2.9.7
Fix on permissions (IsCustomUserPermission)

## V2.9.8
Fix on authentication (Allow firebase in tests if it exists)

## V2.9.9
Fix on authentication (Allow to show description and serializer in responses)

## V2.10.9
Add middleware for specialty id

## V2.10.10
Fix middleware for specialty id if specialty_id does not exist

## V2.10.11
Fix on permissions for None users in request (IsCustomUserPermission)

## V2.11.11
Add user agent middleware. We are using user-agents==2.2.0 library to get the most of the user agent: https://pypi.org/project/user-agents/#:~:text=user_agents%20is%20a%20Python%20library,tablet%20or%20PC%20based%20device. This middleware it will take 0.0024 seconds to run.

## V2.12.0
Add logs in some requests.

## V2.13.0
Add language middleware.

## V2.13.1
Add support for multiple features to language middleware.

## V2.13.2
Add support for multiple features in the same translation to language middleware.

## V2.13.3
Fix replace on language middleware.

## V2.13.4
Refactor on language middleware.

## V2.13.5
Fix null values on language middleware.

## V2.13.6
Temporary hotfix of accept language in middleware locale.
We need to wait for the fix of mobile team (Android and iOS) and check if datadog has warnings related with this problem in the last month.
If we add another country with this logic activated we need to add to the list.

## V3.0.0
Do not use the version 3.0.0 if you have a django version lower than 3.2.0.
If you need to upgrade for version 3.2.0 check this document: https://docs.djangoproject.com/en/3.2/releases/3.2/

Change way of import JSONField in models to give support to django 3.2.2.
Add documentation for json fields.

## V3.1.0
Add middleware for user uid.

## V3.2.0
Fix for multi language locales

## V3.3.0
Create new base model FavoriteBase

## V3.3.1
Update FavoriteBase model

## V3.4.0
Create views and checks for monitoration

## V3.4.1
Update view and checks for monitoration

## V3.4.2
Create new checks for monitoration

## V3.4.3
Update locale middleware to allow monitoring requests without language

## V3.4.4
Add logs to locale middleware

## V3.4.5
Improvements on locale middleware

## V3.4.8
Create base viewset monitoring

## V3.4.9
Fix list_shards call to Kinesis on monitoring

## V3.4.10
Fix search call to Algolia on monitoring

## V3.5.0
Locale middleware now uses a list from django settings to exclude some paths from validation
On update we should create the variable EXCLUDE_PATHS in the settings.py.

## V3.5.1
Fix for uid range generation.

## V3.5.2
Improve uid to id conversion.