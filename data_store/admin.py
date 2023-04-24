from django.contrib import admin, messages
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission


# Register your models here.
from api import config
from .models import dataStore, DatabasePermission, CollectionPermission
from celery import Celery


class celeryConfig:
    """
    A configuration class for the Celery app, setting up various Celery settings
    like broker URL, result backend, and other options.
    """
    
    BROKER_URL = config.BROKER_URL
    BROKER_USE_SSL = config.BROKER_USE_SSL
    CELERY_SEND_EVENTS = True
    CELERY_TASK_RESULT_EXPIRES = None
    CELERY_RESULT_BACKEND = config.CELERY_RESULT_BACKEND
    CELERY_MONGODB_BACKEND_SETTINGS = config.CELERY_MONGODB_BACKEND_SETTINGS


app = Celery()
app.config_from_object(celeryConfig)

def setpermissions(app_label,codename,name):
    """
    A function to create or update permissions for the given app_label, codename, and name.

    :param app_label: The app label to which the permission belongs
    :param codename: The codename for the permission
    :param name: The human-readable name for the permission
    """
    
    try:
        ct = ContentType.objects.get_for_model(dataStore)
        #ct=ContentType.objects.get(app_label=app_label)
        Permission.objects.get_or_create(codename=codename, name=name, content_type=ct)
    except:
         print("Unable to create {0} permission.".format(codename))

#data Store Permissions
#db = MongoClient(host=config.DATA_STORE_MONGO_URI)
db = app.backend.database.client
for database in db.list_database_names():
    if not (database in config.DATA_STORE_EXCLUDE):
        for col in db[database].list_collection_names():
            if not (col in config.DATA_STORE_EXCLUDE):
                for method in [('post','ADD'),('put','UPDATE'),('delete','DELETE'),('safe','SAFE METHODS')]:
                    codename= "{0}_{1}_{2}".format(database,col,method[0])
                    name = "Data Store {0} {1} {2}".format(database,col,method[1])
                    setpermissions('data_store',codename,name)

#create admin permissions
setpermissions('data_store','datastore_admin',"Data Store Admin")

class CollectionPermissionInline(admin.TabularInline):
    """
    A Django admin inline class for the CollectionPermission model. This class
    is used to display CollectionPermission instances related to a specific
    DatabasePermission instance on the DatabasePermission admin page.

    :param model: The Django model class to be used with this inline class
    :param extra: The number of empty forms to display for creating new related objects
    """
    
    model = CollectionPermission
    extra = 0
class DatabasePermissionAdmin(admin.ModelAdmin):
    """
    A Django admin class for the DatabasePermission model. Configures the
    display fields in the admin list view and includes CollectionPermissionInline
    to show related CollectionPermission instances.

    :ivar list_display: A tuple containing the field names to be displayed in the list view
    :ivar inlines: A list containing the inline classes to be used with this admin class
    """
    
    list_display = ('database_name','isPublic')
    inlines = [CollectionPermissionInline]
    actions = ['make_public', 'make_private']
    
    def make_public(self, request, queryset):
        queryset.update(isPublic=True)
    make_public.short_description = "Set selected databases to public"
    
    def make_private(self, request, queryset):
        queryset.update(isPublic=False)
    make_private.short_description = "Set selected databases to private"
    
    def save_formset(self, request, form, formset, change):
        """
        Overrides the save_formset method to check if a related CollectionPermission
        instance is being set to public when the parent DatabasePermission is private.
        If so, an error message is displayed and the change is not saved.

        :param request: The HttpRequest object representing the current request
        :param form: The form instance for the parent object
        :param formset: The formset instance containing the related objects
        :param change: A boolean indicating if the parent object is being changed (True) or added (False)
        """
        if formset.model == CollectionPermission:
            instances = formset.save(commit=False)
            for instance in instances:
                if not instance.pk and not instance.database.isPublic: # Check if the instance is new and the database is private
                    messages.warning(request, "Collection cannot be public if the database is private.")
                    instance.isPublic = False # Set the new collection to private
                elif instance.isPublic and not instance.database.isPublic:
                    messages.error(request, "Set the database to public first.")
                    continue
                instance.save()
            # Delete any objects that have been removed from the formset   
            for obj in formset.deleted_objects:
                obj.delete()
            formset.save_m2m()
        else:
            super().save_formset(request, form, formset, change)
class CollectionPermissionAdmin(admin.ModelAdmin):
    """
    A Django admin class for the CollectionPermission model. Configures the
    display fields in the admin list view, customizes the form for adding or
    updating instances, and handles the save action for the model.

    :ivar list_display: A tuple containing the field names to be displayed in the list view
    :ivar get_form: A method to customize the form for adding or updating instances
    :ivar formfield_for_foreignkey: A method to customize the queryset for foreign key fields
    :ivar save_model: A method to handle the save action for the model
    """
    
    def database_name(self, obj):
        return obj.database.database_name
    database_name.short_description = 'Database Name'

    list_display = ('collection_name', 'database_name', 'isPublic')
    actions = ['make_public', 'make_private']

    def make_public(self, request, queryset):
        """
        Action to set selected CollectionPermissions to public if their
        associated DatabasePermission is also public.
        """
        for cp in queryset:
            if cp.database.isPublic:
                cp.isPublic = True
                cp.save()
            else:
                messages.error(request, f"Set {cp.database} to public first.")      
    make_public.short_description = "Set selected collections to public"

    def make_private(self, request, queryset):
        queryset.update(isPublic=False)
    make_private.short_description = "Set selected collections to private"

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            # Updating permission, show only the related database
            form.base_fields['database'].queryset = DatabasePermission.objects.filter(pk=obj.database.pk)
        else:
            # Creating a new permission, show all databases
            form.base_fields['database'].queryset = DatabasePermission.objects.all()
        return form
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "database":
            kwargs["queryset"] = DatabasePermission.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        if obj.isPublic and not obj.database.isPublic:
            messages.error(request, "Set the database to public first.")
        else:
            super().save_model(request, obj, form, change)

admin.site.register(DatabasePermission, DatabasePermissionAdmin)
admin.site.register(CollectionPermission, CollectionPermissionAdmin)
