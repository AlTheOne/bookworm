from django.contrib import admin
from catalogApp.models import *
from django.db.models import Q


class BooksAdmin(admin.ModelAdmin):
	class Meta:
		model = Books
	
	GLOBAL_ID = None

	fields = ('title', 'preview', 'description', ('genre', 'tags'), ('author', 'phouse'), 'attributes', 'date', ('price', 'discount', 'price_discount'), 'counter', 'user', 'is_active')
	readonly_fields = ('price_discount',)
	save_on_top = True

	list_display = ('id', 'title', 'is_active', 'updated', 'created')
	list_display_links = ('title',)
	list_editable = ('is_active',)
	list_filter = ('is_active', 'updated', 'created')
	search_fields = ('title', 'description')

	def get_form(self, request, obj=None, **kwargs):
		if obj is not None:
			self.GLOBAL_ID = obj.id
		return super(BooksAdmin, self).get_form(request, obj, **kwargs)

	def formfield_for_manytomany(self, db_field, request, **kwargs):
		if db_field.name == "attributes":
			kwargs["queryset"] = AttributesBooks.objects.filter(Q(rel_attrib=self.GLOBAL_ID)|Q(rel_attrib=None))
		return super(BooksAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

admin.site.register(Books, BooksAdmin)


class AttributesBooksAdmin(admin.ModelAdmin):
	class Meta:
		model = AttributesBooks

	list_display = ('id', 'name', 'value')
	list_display_links = ('name',)
	search_fields = ('name', 'value')

admin.site.register(AttributesBooks, AttributesBooksAdmin)


class CurrencyAdmin(admin.ModelAdmin):
	class Meta:
		model = Currency

	list_display = ('id', 'title', 'quota', 'is_active')
	list_display_links = ('title', )
	search_fields = ('title', 'slug')
	list_editable = ('is_active',)

	fields = (('title', 'slug'), 'rune', 'quota', 'is_active')

admin.site.register(Currency, CurrencyAdmin)


class PublicHouseAdmin(admin.ModelAdmin):
	class Meta:
		model = PublicHouse

	list_display = ('id', 'title', 'is_active')
	list_display_links = ('title',)
	list_editable = ('is_active',)
	search_fields = ('title',)

admin.site.register(PublicHouse, PublicHouseAdmin)


class GenreBooksAdmin(admin.ModelAdmin):
	class Meta:
		model = GenreBooks

	list_display = ('id', 'title', 'user', 'is_active', 'updated', 'created')
	list_display_links = ('title',)
	list_editable = ('is_active',)
	search_fields = ('title', 'slug')
	list_filter = ('is_active', 'updated', 'created')

admin.site.register(GenreBooks, GenreBooksAdmin)


class AuthorBooksAdmin(admin.ModelAdmin):
	class Meta:
		model = AuthorBooks

	list_display = ('id', 'last_name', 'first_name', 'is_active', 'updated', 'created')
	list_display_links = ('last_name',)
	search_fields = ('last_name', 'first_name', 'secondary_name')
	list_filter = ('is_active', 'updated', 'created')

admin.site.register(AuthorBooks, AuthorBooksAdmin)


class TagsBooksAdmin(admin.ModelAdmin):
	class Meta:
		model = TagsBooks

	list_display = ('id', 'title', 'user', 'is_active', 'updated', 'created')
	list_display_links = ('title',)
	list_editable = ('is_active',)
	search_fields = ('title', 'slug')
	list_filter = ('is_active', 'updated', 'created')

admin.site.register(TagsBooks, TagsBooksAdmin)


class CommentsBookAdmin(admin.ModelAdmin):
	class Meta:
		model = CommentsBook

	list_display = ('id', 'short_message', 'rate', 'user', 'is_active', 'created')
	list_display_links = ('short_message',)
	search_fields = ('message',)
	list_editable = ('is_active',)
	list_filter = ('is_active', 'updated', 'created')

admin.site.register(CommentsBook, CommentsBookAdmin)