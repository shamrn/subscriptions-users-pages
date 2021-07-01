from django.contrib import admin
from django.utils.html import format_html

from .models import Pages,Section,Body,List,Contact
import nested_admin

class ListInlineAdmin(nested_admin.NestedStackedInline):
    model = List
    extra = 0
    min_num = 1

class BodyInlineAdmin(nested_admin.NestedStackedInline):
    model = Body
    extra = 0
    min_num = 1
    max_num = 1

class SectionInlineAdmin(nested_admin.NestedStackedInline):
    model = Section
    inlines = [BodyInlineAdmin,ListInlineAdmin]
    extra = 0

@admin.register(Pages)
class PagesAdmin(nested_admin.NestedModelAdmin):
    inlines = [SectionInlineAdmin]
    prepopulated_fields = {'slug': ('page_name',)}


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def change_button(self, obj):
        return format_html('<a href="/admin/pages/contact/{}/change/">Редактировать</a>', obj.id)

    change_button.short_description = "Редактирование"

    list_display = ('change_button','phone','whats_app','telegram','email')
    list_display_links = None