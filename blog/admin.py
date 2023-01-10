from django.contrib import admin
from .models import Article, Category
from jalali_date import datetime2jalali, date2jalali

admin.site.site_header = 'وبلاگ نمونه'


def make_publish(modeladmin, request, queryset):
    row_updated = queryset.update(status='p')
    if row_updated == 1:
        bit_message = "منتشر شد"
    else:
        bit_message = "منتشر شد"
    modeladmin.message_user(request, "{} مقاله {}".format(row_updated, bit_message))
make_publish.short_description = "انتشار مقالات انتخاب شده"


def make_draft(modeladmin, request, queryset):
    row_updated = queryset.update(status='d')
    if row_updated == 1:
        bit_message = "پیش‌نویس شد"
    else:
        bit_message = "پیش‌نویس شد"
    modeladmin.message_user(request, "{} مقاله {}".format(row_updated, bit_message))
make_draft.short_description = 'پیس‌نویس شدن مقالات انتخاب شده'


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('position', 'title', 'slug', 'status', 'parent')
    list_editable = ('status', 'parent')
    search_fields = ('title', 'slug',)
    list_filter = ('status', 'parent')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)


class ArticleAdmin(admin.ModelAdmin):
    def jalali(self, obj):
        return datetime2jalali(obj.publish).strftime('%y/%m/%d _ %H:%M:%S')
    jalali.short_description = 'تاریخ'

    list_display = ('title', 'thumbnail_tag', 'author', 'slug', 'jalali', 'status', 'categories')
    search_fields = ('title', 'description')
    list_filter = ('status', 'publish')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-status', '-publish']


    actions = [make_publish, make_draft]


admin.site.register(Article, ArticleAdmin)
