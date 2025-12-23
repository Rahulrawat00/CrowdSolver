from django.contrib import admin
from .views import Member,Secretary
from .models import Categoryname,Solutions,Vote

class Memberdata(admin.ModelAdmin):
    list_display = ('memberName', 'memberMail', 'memberContact','memberPassword','memberAddress','memberImage','memberType')


admin.site.register(Member, Memberdata)
class Category_Name(admin.ModelAdmin):
    list_display=('category',)


admin.site.register(Categoryname, Category_Name)


@admin.register(Secretary)
class SecretaryAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('email',)

    def save_model(self, request, obj, form, change):
        # Hash password only when creating or changing it
        if not change:
            obj.set_password(obj.password)
        else:
            original = Secretary.objects.get(pk=obj.pk)
            if original.password != obj.password:
                obj.set_password(obj.password)

        super().save_model(request, obj, form, change)

class Solutions_data(admin.ModelAdmin):
    list_display = ('title','Description')

admin.site.register(Solutions,Solutions_data)

class vote_data(admin.ModelAdmin):
    list_display=('solution', 'member', 'is_approved','voted_at')
admin.site.register(Vote,vote_data)



