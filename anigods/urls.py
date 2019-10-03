from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views
from project import views as project_view
from anime import views as anime_view
from api import views as api_views

urlpatterns = [
    url(r'^robots\.txt$', TemplateView.as_view(template_name='home/robots.txt',content_type='text/plain')),
    url(r'^django-admin/', admin.site.urls),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    # User management
    url(r'^accounts/', include('allauth.urls')),
    url(r'^users/', include('users.urls')),

    url(r'^search/',  include('search.urls')),
    url(r'^du-an/', include('project.urls')),
    url(r'^anime/', include('anime.urls')),
    url(r'^api/',  include('api.urls')),
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r'', include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r'^pages/', include(wagtail_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
