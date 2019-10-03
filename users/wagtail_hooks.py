from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken
from django.contrib.sites.models import Site


class SocialAppAdmin(ModelAdmin):
    model = SocialApp
    menu_label = 'Social Apps'  # ditch this to use verbose_name_plural from model
    menu_icon = 'plus'  # change as required
    list_display = ('provider', 'name', 'client_id', 'secret')


class SocialAccountAdmin(ModelAdmin):
    model = SocialAccount
    menu_label = 'Social Accounts'  # ditch this to use verbose_name_plural from model
    menu_icon = 'user'  # change as required
    list_display = ('user', 'provider', 'uid','last_login', 'date_joined')
    list_filter = ('provider', 'last_login', 'date_joined')
    search_fields = ('user','provider','uid')


class SocialTokenAdmin(ModelAdmin):
    model = SocialToken
    menu_label = 'Social Tokens'  # ditch this to use verbose_name_plural from model
    menu_icon = 'password'  # change as required
    list_display = ('app', 'account', 'token','token_secret','expires_at')
    list_filter = ('app', 'account')
    search_fields = ('app',)

class DjangoSiteAdmin(ModelAdmin):
    model = Site
    menu_label = 'Django Sites'  # ditch this to use verbose_name_plural from model
    menu_icon = 'site'  # change as required
    list_display = ('domain', 'name')
    search_fields = ('domain','name')


class SocialLoginAdminGroup(ModelAdminGroup):
    menu_label = 'Social Logins'
    menu_icon = 'group'  # change as required
    menu_order = 300  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (SocialAccountAdmin, SocialAppAdmin, SocialTokenAdmin, DjangoSiteAdmin)


# When using a ModelAdminGroup class to group several ModelAdmin classes together,
# you only need to register the ModelAdminGroup class with Wagtail:
modeladmin_register(SocialLoginAdminGroup)

