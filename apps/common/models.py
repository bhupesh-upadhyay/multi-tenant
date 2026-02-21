from django.db import models
from django.utils import timezone

"""
A custom queryset controls how queries behave
"""
class SoftDeleteQuerySet(models.QuerySet):
    # Queryset Delete
    def delete(self): # will only update the object set is_delete False.
        return super().update(
            is_deleted=True,
            deleted_at=timezone.now()
        )
    # query set hard delete
    def hard_delete(self): # actual delete
        return super().delete()

    def active(self): # return non delete records where is_deleted=False
        return self.filter(is_deleted=False)

    def deleted(self): # return deleted records where is_delete=True
        return self.filter(is_deleted=True)

"""
Active Manger controls what default Models.objects return
means only is_delete=False i.e active data will return
Delete records will automatically hidden
"""
class ActiveManager(models.Manager): 
    def get_queryset(self): # means Model.objects.all() will give is_delete=False
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=False)

"""
Abstract base Model
Every Model that inherits this will
get these field by defaults
table will not be created only being inherited
"""
class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = ActiveManager()          # Default manager (hides deleted) syntax: model.objects.all()
    all_objects = SoftDeleteQuerySet.as_manager()  # Shows everything delete + nondeleted, syntax Model.all_objects.all()

    class Meta:
        abstract = True # Means Django will not create a table, It is just a base class.

    def delete(self, using=None, keep_parents=False): #overridding delete object model level
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])

    def hard_delete(self): # object Model level
        super().delete()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=["is_deleted", "deleted_at"])

# workflow
"""
Example How you actually use it.
class Product(SoftDeleteModel):
    name = models.CharField(max_length=100)
    
create -> Product.objects.create(name="phone")
soft Delete -> product = Product.objects.get(id=1); product.delete()
normal query -> Product.objects.all() # will not show
deleted -> Product.all_objects.delete()
Restore -> product.restore()
Permanent delete -> product.hard_delete()

CONCLUSION:
it prevent accidental data loss
"""

# Doubts.
"""
Q: why override delete in both queryset and model:
A: because Queryset and Model object are two different thing
    Model object -> Product.objects.get(id=1)
        porduct.delete() -> calls: softdeletemode.delete() (single object delete)
    queryset -> Product.objects.filter(category='Electronics')
        .delete() -> calls queryset.delete()
        
        
What is Manger:
A Django model manager is the interface through which database query operations are provided to Django models. 
default: objects = models.Manager() automatically added by default django
but here objects will call a custom mananger which have already modefied the default query of all object
here: it uses the manager that django auto-creates from your softDeleteQuerySet.
ActivManger controls visibilty
SoftDeleteQeury control behavior

so objects is a Manager, controls the default query set
Analogy here is:
Model = Table
Queryset = Sql Query
Manager = Factory that builds queries
Manager creates Queryset and queryset executes sql
"""
