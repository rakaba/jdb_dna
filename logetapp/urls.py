from django.urls import path
from . import views
from .views import listview, styledetailview, stylemypageview, stylemytestview, storedetailview, dnaapplicationview, itemorderview, dnaapplication_doneview, itemorder_doneview, stylepaperview, stylerepoview, styleadview, stylewebview, storedetailbodyview, skindetailview, skinmypageview, skinmytestview, skinpaperview, skinrepoview, skinadview, skinwebview, storedetailskinview, muscledetailview, musclemypageview, musclemytestview, musclepaperview, musclerepoview, muscleadview, musclewebview, storedetailmuscleview, headdetailview, headmypageview, headmytestview, headpaperview, headrepoview, headadview, headwebview, storedetailheadview, otherdetailview, othermypageview, othermytestview, otherrepoview, otheradview, otherwebview, storedetailotherview, floraexpertdetailview, floraexpertmypageview, floraexpertmytestview, floraexpertrepoview, floraexpertwebview, storedetailfloraexpertview, floralightdetailview, floralightmypageview, floralightmytestview, floralightwebview, storedetailfloralightview, foodproteindetailview, foodproteinmypageview, foodproteinmytestview, foodproteinwebview, storedetailfoodproteinview, skinmyteststoreview, stylemyteststoreview, musclemyteststoreview, headmyteststoreview, floralightmyteststoreview, floraexpertmyteststoreview, foodproteinmyteststoreview, othermyteststoreview, storestylerepoview, storestyleadview, storeskinrepoview, storeskinadview, storemusclerepoview, storemuscleadview, storeheadrepoview, storeheadadview, storefloraexpertrepoview, storeotherrepoview






app_name = 'logetapp'

urlpatterns = [
    path('', views.Login.as_view(), name='index'),
    path('top/', views.Top.as_view(), name='top'),
    path('sample/', views.Sample.as_view(), name='sample'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('user_create/', views.UserCreate.as_view(), name='user_create'),
    path('user_create/done/', views.UserCreateDone.as_view(), name='user_create_done'),
    path('user_create/complete/<token>/', views.UserCreateComplete.as_view(), name='user_create_complete'),
    path('user_detail/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('user_update/<int:pk>/', views.UserUpdate.as_view(), name='user_update'),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
    path('email/change/', views.EmailChange.as_view(), name='email_change'),
    path('email/change/done/', views.EmailChangeDone.as_view(), name='email_change_done'),
    path('email/change/complete/<str:token>/', views.EmailChangeComplete.as_view(), name='email_change_complete'),
    path('list/', listview, name="list"),
    path('styledetail/<int:pk>/', styledetailview, name="styledetail"),
    path('skindetail/<int:pk>/', skindetailview, name="skindetail"),
    path('stylemypage/<int:pk>/', stylemypageview, name="stylemypage"),
    path('skinmypage/<int:pk>/', skinmypageview, name="skinmypage"),
    path('stylemytest/<int:pk>/', stylemytestview, name="stylemytest"),
    path('skinmytest/<int:pk>/', skinmytestview, name="skinmytest"),
    path('skinmyteststore/<int:pk>/', skinmyteststoreview, name="skinmyteststore"),
    path('storedetail/<int:pk>/', storedetailview, name="storedetail"),
    path('dnaapplication/<int:pk>/', dnaapplicationview, name="dnaapplication"),
    path('dnaapplication_done/', dnaapplication_doneview, name="dnaapplication_done"),
    path('itemorder/<int:pk>/', itemorderview, name="itemorder"),
    path('itemorder_done/', itemorder_doneview, name="itemorder_done"),
    path('stylepaper/<int:pk>/', stylepaperview, name="stylepaper"),
    path('stylerepo/<int:pk>/', stylerepoview, name="stylerepo"),
    path('stylead/<int:pk>/', styleadview, name="stylead"),
    path('styleweb/<int:pk>/', stylewebview, name="styleweb"),
    path('storedetail_body/<int:pk>/', storedetailbodyview, name="storedetailbody"),
    path('skindetail/<int:pk>/', skindetailview, name="skindetail"),
    path('skinmypage/<int:pk>/', skinmypageview, name="skinmypage"),
    path('skinpaper/<int:pk>/', skinpaperview, name="skinpaper"),
    path('skinrepo/<int:pk>/', skinrepoview, name="skinrepo"),
    path('skinad/<int:pk>/', skinadview, name="skinad"),
    path('skinweb/<int:pk>/', skinwebview, name="skinweb"),
    path('storedetail_skin/<int:pk>/', storedetailskinview, name="storedetailskin"),
    path('muscledetail/<int:pk>/', muscledetailview, name="muscledetail"),
    path('musclemypage/<int:pk>/', musclemypageview, name="musclemypage"),
    path('musclepaper/<int:pk>/', musclepaperview, name="musclepaper"),
    path('musclerepo/<int:pk>/', musclerepoview, name="musclerepo"),
    path('musclead/<int:pk>/', muscleadview, name="musclead"),
    path('muscleweb/<int:pk>/', musclewebview, name="muscleweb"),
    path('musclemytest/<int:pk>/', musclemytestview, name="musclemytest"),
    path('storedetail_muscle/<int:pk>/', storedetailmuscleview, name="storedetailmuscle"),
    path('headdetail/<int:pk>/', headdetailview, name="headdetail"),
    path('headmypage/<int:pk>/', headmypageview, name="headmypage"),
    path('headpaper/<int:pk>/', headpaperview, name="headpaper"),
    path('headrepo/<int:pk>/', headrepoview, name="headrepo"),
    path('headad/<int:pk>/', headadview, name="headad"),
    path('headweb/<int:pk>/', headwebview, name="headweb"),
    path('headmytest/<int:pk>/', headmytestview, name="headmytest"),
    path('storedetail_head/<int:pk>/', storedetailheadview, name="storedetailhead"),
    path('floralightdetail/<int:pk>/', floralightdetailview, name="floralightdetail"),
    path('floralightmypage/<int:pk>/', floralightmypageview, name="floralightmypage"),
    path('floralightweb/<int:pk>/', floralightwebview, name="floralightweb"),
    path('floralightmytest/<int:pk>/', floralightmytestview, name="floralightmytest"),
    path('storedetail_floralight/<int:pk>/', storedetailfloralightview, name="storedetailfloralight"),
    path('floraexpertdetail/<int:pk>/', floraexpertdetailview, name="floraexpertdetail"),
    path('floraexpertmypage/<int:pk>/', floraexpertmypageview, name="floraexpertmypage"),
    path('floraexpertrepo/<int:pk>/', floraexpertrepoview, name="floraexpertrepo"),
    path('floraexpertweb/<int:pk>/', floraexpertwebview, name="floraexpertweb"),
    path('floraexpertmytest/<int:pk>/', floraexpertmytestview, name="floraexpertmytest"),
    path('storedetail_floraexpert/<int:pk>/', storedetailfloraexpertview, name="storedetailfloraexpert"),
    path('foodproteindetail/<int:pk>/', foodproteindetailview, name="foodproteindetail"),
    path('foodproteinmypage/<int:pk>/', foodproteinmypageview, name="foodproteinmypage"),
    path('foodproteinweb/<int:pk>/', foodproteinwebview, name="foodproteinweb"),
    path('foodproteinmytest/<int:pk>/', foodproteinmytestview, name="foodproteinmytest"),
    path('storedetail_foodprotein/<int:pk>/', storedetailfoodproteinview, name="storedetailfoodprotein"),
    path('otherdetail/<int:pk>/', otherdetailview, name="otherdetail"),
    path('othermypage/<int:pk>/', othermypageview, name="othermypage"),
    path('otherrepo/<int:pk>/', otherrepoview, name="otherrepo"),
    path('otherad/<int:pk>/', otheradview, name="otherad"),
    path('otherweb/<int:pk>/', otherwebview, name="otherweb"),
    path('othermytest/<int:pk>/', othermytestview, name="othermytest"),
    path('storedetail_other/<int:pk>/', storedetailotherview, name="storedetailother"),
    path('stylemyteststore/<int:pk>/', stylemyteststoreview, name="stylemyteststore"),
    path('musclemyteststore/<int:pk>/', musclemyteststoreview, name="musclemyteststore"),
    path('headmyteststore/<int:pk>/', headmyteststoreview, name="headmyteststore"),
    path('floralightmyteststore/<int:pk>/', floralightmyteststoreview, name="floralightmyteststore"),
    path('floraexpertmyteststore/<int:pk>/', floraexpertmyteststoreview, name="floraexpertmyteststore"),
    path('foodproteinmyteststore/<int:pk>/', foodproteinmyteststoreview, name="foodproteinmyteststore"),
    path('othermyteststore/<int:pk>/', othermyteststoreview, name="othermyteststore"),
    path('storestylerepo/<int:pk>/', storestylerepoview, name="storestylerepo"),
    path('storestylead/<int:pk>/', storestyleadview, name="storestylead"),
    path('storeskinrepo/<int:pk>/', storeskinrepoview, name="storeskinrepo"),
    path('storeskinad/<int:pk>/', storeskinadview, name="storeskinad"),
    path('storemusclerepo/<int:pk>/', storemusclerepoview, name="storemusclerepo"),
    path('storemusclead/<int:pk>/', storemuscleadview, name="storemusclead"),
    path('storeheadrepo/<int:pk>/', storeheadrepoview, name="storeheadrepo"),
    path('storeheadad/<int:pk>/', storeheadadview, name="storeheadad"),
    path('storefloraexpertrepo/<int:pk>/', storefloraexpertrepoview, name="storefloraexpert"),
    path('storeotherrepo/<int:pk>/', storeotherrepoview, name="storeotherrepo"),
]
