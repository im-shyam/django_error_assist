from django.views import debug
from django.conf import settings


# check if the DEBUG flag is True
if settings.DEBUG:

    # URL link constants
    STACKOVERFLOW_URL = "http://stackoverflow.com/search?q=python+or+django+"
    GOOGLE_URL = "https://www.google.co.in/#q=django "

    REPLACE_STRING = '<th>Exception Type:</th>'

    HTML_STRING = """
    <h3 class="DjangoErrorAssist">
        <a href="%s" target="_blank">Get assist for this error in %s </a>
    <h3>
    """

    # Custom Exception class follows
    class Error(Exception):
        """ Base class for other exceptions """
        pass

    class ImProperTypeError(Error):
        """ Raised when value of DJANGO_ERROR_ASSIST_FROM variable is not of proper type.
        The expected type is str() """

    class ImProperValueError(Error):
        """ Raised when value of DJANGO_ERROR_ASSIST_FROM variable is not 'google' or
        'stackoverflow' """

    # Middleware class follows
    class DjangoErrorAssistMiddleware(object):
        """
        Middleware to get the help for the error that occurs in Django
        """
        def __init__(self):
            self.source_choices = dict()
            self.source_choices['stackoverflow'] = STACKOVERFLOW_URL
            self.source_choices['google'] = GOOGLE_URL

            # making 'stackoverflow' as the default source
            self.selected_source = 'stackoverflow'

            # check for user's preference of source from settings file
            if getattr(settings, 'DJANGO_ERROR_ASSIST_FROM', None):

                # check if the variable has been set to right 'type'
                if not isinstance(settings.DJANGO_ERROR_ASSIST_FROM, str):
                    raise ImProperTypeError("DJANGO_ERROR_ASSIST_FROM variable should be of type "
                                            "'str' ")

                # check if the variable is valid and expected string
                if settings.DJANGO_ERROR_ASSIST_FROM.lower() not in self.source_choices.iterkeys():
                    raise ImProperValueError("DJANGO_ERROR_ASSIST_FROM variable can take either "
                                             "'google' or 'stackoverflow' ")

                # override the selected_source with user preferred source
                self.selected_source = settings.DJANGO_ERROR_ASSIST_FROM

            # get the URL link for the selected source
            self.query_link = self.source_choices.get(self.selected_source)

            # calling the method to edit the django template
            self._alter_django_500_debug_template()

        def _alter_django_500_debug_template(self):
            # append the exception type to the query link
            self.query_link += "{{ exception_type|escape }}"

            # append the query_link to HTML_STRING
            formatted_html_string = HTML_STRING % (self.query_link, self.selected_source)

            # get the replacement string
            replacement = REPLACE_STRING + formatted_html_string

            # todo: fix the issue of appending on auto reload in dev server
            # check if this class exists in the template
            if "DjangoErrorAssist" not in debug.TECHNICAL_500_TEMPLATE:
                # patch up the built-in template with custom html string
                debug.TECHNICAL_500_TEMPLATE = debug.TECHNICAL_500_TEMPLATE.replace(REPLACE_STRING,
                                                                                    replacement)

        def __new__(cls, *args, **kwargs):
            # making sure only single instance of this class is instantiated
            if not hasattr(cls, 'instance'):
                cls.instance = super(DjangoErrorAssistMiddleware, cls).__new__(cls)
            return cls.instance
