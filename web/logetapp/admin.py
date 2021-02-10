from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _
from .models import User, StyleDnaModel, SkinDnaModel, MuscleDnaModel, HeadDnaModel, FloraLightModel, FloraExpertModel, FoodProteinModel, OtherModel, StoreModel
from import_export import resources
from import_export.admin import ImportExportModelAdmin



class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'styletestid', 'styletestpass', 'stylecheckcode', 'styleansno', 'styletestername', 'skintestid', 'skintestpass', 'skincheckcode', 'skinansno', 'skintestername', 'muscletestid', 'muscletestpass', 'musclecheckcode', 'muscleansno', 'muscletestername', 'headtestid', 'headtestpass', 'headcheckcode', 'headansno', 'headtestername', 'floralighttestid', 'floralighttestpass', 'floralightcheckcode', 'floralightansno', 'floralighttestername', 'floraexperttestid', 'floraexperttestpass', 'floraexpertcheckcode', 'floraexpertansno', 'floraexperttestername', 'foodproteintestid', 'foodproteintestpass', 'foodproteincheckcode', 'foodproteinansno', 'foodproteintestername', 'othertestid', 'othertestpass', 'othercheckcode', 'otheransno', 'othertestername')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'styletestid', 'styletestpass', 'stylecheckcode', 'styleansno', 'styletestername', 'skintestid', 'skintestpass', 'skincheckcode', 'skinansno', 'skintestername', 'muscletestid', 'muscletestpass', 'musclecheckcode', 'muscleansno', 'muscletestername', 'headtestid', 'headtestpass', 'headcheckcode', 'headansno', 'headtestername', 'floralighttestid', 'floralighttestpass', 'floralightcheckcode', 'floralightansno', 'floralighttestername', 'floraexperttestid', 'floraexperttestpass', 'floraexpertcheckcode', 'floraexpertansno', 'floraexperttestername', 'foodproteintestid', 'foodproteintestpass', 'foodproteincheckcode', 'foodproteinansno', 'foodproteintestername', 'othertestid', 'othertestpass', 'othercheckcode', 'otheransno', 'othertestername')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(User, MyUserAdmin)

# Categoryモデルに統合する為にModelResourceを継承したクラスを作成
class StyleDnaModelResource(resources.ModelResource):
    class Meta:
        model = StyleDnaModel
@admin.register(StyleDnaModel)
# ImportExportModelAdminを継承したadminクラスを作成
class StyleDnaModelAdmin(ImportExportModelAdmin):
    ordering = ['styledate']
    list_display=('styletestid', 'styletestpass', 'styleansno', 'stylename')

    # resource_classにModelResourceを継承したクラスを設定
    resource_class = StyleDnaModelResource

# Categoryモデルに統合する為にModelResourceを継承したクラスを作成
class SkinDnaModelResource(resources.ModelResource):
    class Meta:
        model = SkinDnaModel
@admin.register(SkinDnaModel)
# ImportExportModelAdminを継承したadminクラスを作成
class SkinDnaModelAdmin(ImportExportModelAdmin):
    ordering = ['skindate']
    list_display=('skintestid', 'skintestpass', 'skinansno', 'skinname')

    # resource_classにModelResourceを継承したクラスを設定
    resource_class = SkinDnaModelResource

# Categoryモデルに統合する為にModelResourceを継承したクラスを作成
class MuscleDnaModelResource(resources.ModelResource):
    class Meta:
        model = MuscleDnaModel
@admin.register(MuscleDnaModel)
# ImportExportModelAdminを継承したadminクラスを作成
class MuscleDnaModelAdmin(ImportExportModelAdmin):
    ordering = ['muscledate']
    list_display=('muscletestid', 'muscletestpass', 'muscleansno', 'musclename')

    # resource_classにModelResourceを継承したクラスを設定
    resource_class = MuscleDnaModelResource

# Categoryモデルに統合する為にModelResourceを継承したクラスを作成
class HeadDnaModelResource(resources.ModelResource):
    class Meta:
        model = HeadDnaModel
@admin.register(HeadDnaModel)
# ImportExportModelAdminを継承したadminクラスを作成
class HeadDnaModelAdmin(ImportExportModelAdmin):
    ordering = ['headdate']
    list_display=('headtestid', 'headtestpass', 'headansno', 'headname')

    # resource_classにModelResourceを継承したクラスを設定
    resource_class = HeadDnaModelResource

# Categoryモデルに統合する為にModelResourceを継承したクラスを作成
class FloraLightModelResource(resources.ModelResource):
    class Meta:
        model = FloraLightModel
@admin.register(FloraLightModel)
# ImportExportModelAdminを継承したadminクラスを作成
class FloraLightModelAdmin(ImportExportModelAdmin):
    ordering = ['floralightdate']
    list_display=('floralighttestid', 'floralighttestpass', 'floralightansno', 'floralightname')

    # resource_classにModelResourceを継承したクラスを設定
    resource_class = FloraLightModelResource

# Categoryモデルに統合する為にModelResourceを継承したクラスを作成
class FloraExpertModelResource(resources.ModelResource):
    class Meta:
        model = FloraExpertModel
@admin.register(FloraExpertModel)
# ImportExportModelAdminを継承したadminクラスを作成
class FloraExpertModelAdmin(ImportExportModelAdmin):
    ordering = ['floraexpertdate']
    list_display=('floraexperttestid', 'floraexperttestpass', 'floraexpertansno', 'floraexpertname')

    # resource_classにModelResourceを継承したクラスを設定
    resource_class = FloraExpertModelResource

# Categoryモデルに統合する為にModelResourceを継承したクラスを作成
class FoodProteinModelResource(resources.ModelResource):
    class Meta:
        model = FoodProteinModel
@admin.register(FoodProteinModel)
# ImportExportModelAdminを継承したadminクラスを作成
class FoodProteinModelAdmin(ImportExportModelAdmin):
    ordering = ['foodproteindate']
    list_display=('foodproteintestid', 'foodproteintestpass', 'foodproteinansno', 'foodproteinname')

    # resource_classにModelResourceを継承したクラスを設定
    resource_class = FoodProteinModelResource

# Categoryモデルに統合する為にModelResourceを継承したクラスを作成
class OtherModelResource(resources.ModelResource):
    class Meta:
        model = OtherModel
@admin.register(OtherModel)
# ImportExportModelAdminを継承したadminクラスを作成
class OtherModelAdmin(ImportExportModelAdmin):
    ordering = ['otherdate']
    list_display=('othertestid', 'othertestpass', 'otheransno', 'othername')

    # resource_classにModelResourceを継承したクラスを設定
    resource_class = OtherModelResource



#ここから
# Categoryモデルに統合する為にModelResourceを継承したクラスを作成
class StoreModelResource(resources.ModelResource):
    class Meta:
        model = StoreModel
@admin.register(StoreModel)
# ImportExportModelAdminを継承したadminクラスを作成
class StoreModelAdmin(ImportExportModelAdmin):
    ordering = ['storeid']
    list_display=('storeid', 'storename', 'email')

    # resource_classにModelResourceを継承したクラスを設定
    resource_class = StoreModelResource
#ここまで