from django.contrib import admin
from .models import Product, UserProfile, OrderItem, Return


admin.site.register(Product)
admin.site.register(UserProfile)
admin.site.register(OrderItem)


class ReturnAdmin(admin.ModelAdmin):
    list_display = ['purchase', 'requested_at', 'status', 'admin_approved', 'confirm_link']

    def confirm_link(self, obj):
        if obj.status == 'на розгляді':
            return "/admin/returns/{obj.id}/confirm/"
        return '-'
    confirm_link.allow_tags = True
    confirm_link.short_description = "Дія"

admin.site.register(Return, ReturnAdmin)
