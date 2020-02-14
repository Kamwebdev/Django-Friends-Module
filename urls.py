from django.conf.urls import include
from django.urls import path


from . import views

urlpatterns = [
    path('allusers', views.AllUsersListView.as_view(), name='allusers'),
    path('friends', views.FriendsListView.as_view(), name='friends'),
    path('friends/add/', views.AddFriendView.as_view(), name='addfriend'),
    path('friends/delete/<int:pk>', views.FriendDeleteView.as_view(), name='frienddelete'),
    path('accept/list', views.AcceptFriendListView.as_view(), name='acceptlistfriend'),
    path('accept/<int:pk>', views.AcceptAddListView, name='addaccept'),
    path('accept/delete/<int:pk>', views.AcceptDeleteListView.as_view(), name='acceptdelete'),
] 