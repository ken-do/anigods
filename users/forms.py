from django import forms
from django.utils.translation import ugettext_lazy as _

from wagtail.users.forms import UserEditForm, UserCreationForm

from users.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
        
    # We cannot call this method clean_username since this the name of the
    # username field may be different, so clean_username would not be reliably
    # called. We therefore call _clean_username explicitly in _clean_fields.
    def _clean_username(self):
        username_field = CustomUser.USERNAME_FIELD
        # This method is called even if username if empty, contrary to clean_*
        # methods, so we have to check again here that data is defined.
        if username_field not in self.cleaned_data:
            return
        username = self.cleaned_data[username_field]

        users = CustomUser._default_manager.all()
        if self.instance.pk is not None:
            users = users.exclude(pk=self.instance.pk)
        if users.filter(**{username_field: username}).exists():
            self.add_error(CustomUser.USERNAME_FIELD, forms.ValidationError(
                self.error_messages['duplicate_username'],
                code='duplicate_username',
            ))
        return username

    class Meta(UserCreationForm.Meta):
        model = CustomUser


class CustomUserEditForm(UserEditForm):

    class Meta:
        model = CustomUser
        fields = UserEditForm.Meta.fields




class SettingsForm(forms.ModelForm):
    display_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Display Name'})
    )

    avatar = forms.ImageField(
        required = False,
        label=_('Avatar'),
        widget=forms.FileInput(attrs={'id':'imageUpload'})
    )


    class Meta(object):
        model = CustomUser
        fields = ['avatar', 'display_name']

    def __init__(self, *args, **kwargs):
        # Instance is a CustomUser object
        instance = kwargs.get('instance', None)
        if instance:
            kwargs.setdefault('initial', {}).update({'display_name': instance.display_name,
                                                     'avatar': instance.avatar})
        super().__init__(*args, **kwargs)

