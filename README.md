# django_error_assist

This package helps in searching answers in stackoverflow or google(based on your preference) for errors that occur in Django by providing a 
a link just below the Exception/Error.

## Installation 

As always `pip` is the recommended way to install this package.
```
pip install django_error_assist
```

## Settings to be done

In your `settings.py` file set the source as Google/StackOverFlow
```
DJANGO_ERROR_ASSIST_FROM = 'google'
```
OR
```
DJANGO_ERROR_ASSIST_FROM = 'stackoverflow'
```
and now we should add the Middleware in `settings.py` as shown below:
(tested and proved to work from django version >= 1.10)
```
 MIDDLEWARE += ['django_error_assist.middleware.DjangoErrorAssistMiddleware']
```
and you are done!

**NOTE 1: By default 'stackoverflow' is the chosen one for you**
**NOTE 2 : This works only when DEBUG is set to True**

After this step whenever you encounter an error you should see a link under the error. 
By clicking on the link it'll will take you the result page of google/stackoverflow (based on your preference) about the error in the new tab.
Happy Djangoing!
