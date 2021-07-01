from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import PortUserCreationForm, PortUserChangeForm
from .models import PortUser,Ip,SubscriptionTypes,CargoTypes,Subscription
from django.contrib.auth.models import Group

class PortUserAdmin(UserAdmin):

    add_form = PortUserCreationForm
    form = PortUserChangeForm
    model = PortUser
    list_display = ('email','is_active','quantity_ip')

    fieldsets = (
        (None, {'fields': ('email', 'password','full_name','billing_address','user_ip')}),
        ('Дополнительные настройки', {'fields': ('is_staff', 'is_active')}),
    )
    autocomplete_fields = ['user_ip']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('full_name','email','billing_address', 'password1', 'password2', 'is_staff','is_active')}
        ),
    )

    search_fields = ('email',)
    ordering = ('email','quantity_ip')

admin.site.register(PortUser, PortUserAdmin)


@admin.register(Ip)
class IpAdmin(admin.ModelAdmin):

    def has_add_permission(self, request, obj=None):
        return False

    list_display = ['ip','quantity_user']
    autocomplete_fields = ['user']
    search_fields = ('ip',)


@admin.register(SubscriptionTypes)
class SubscriptionTypesAdmin(admin.ModelAdmin):
    list_display = ['name',]


@admin.register(CargoTypes)
class CargoTypesAdmin(admin.ModelAdmin):
    list_display = ['name',]

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user','subscription_types','date_from','date_to']

admin.site.unregister([ Group])