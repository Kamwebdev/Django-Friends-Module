from django_filters.views import FilterView
from accounts.models import UserProfile
from django.views.generic.edit import DeleteView
from django.views import View
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .filters import UsersFilter
from .forms import UsersManageForm
from .models import Friend


class AllUsersListView(LoginRequiredMixin, FilterView):
    model = UserProfile
    template_name = 'friends/allusers.html'
    filterset_class = UsersFilter
    paginate_by = 3

    def get_queryset(self):
        q1 = Friend.objects.filter(owner=self.request.user)
        queryset = super(AllUsersListView, self).get_queryset().exclude(Q(user__in=[
            o.liked for o in q1])).exclude(user=self.request.user).filter(user__is_active=True)
        return queryset


class FriendsListView(LoginRequiredMixin, FilterView):
    model = Friend
    template_name = 'friends/friends.html'
    filterset_class = UsersFilter
    paginate_by = 3

    def get_queryset(self):
        q1 = Friend.objects.filter(owner=self.request.user)
        queryset = super(FriendsListView, self).get_queryset().filter(
            Q(owner=self.request.user)).filter(liked__is_active=True)
        return queryset


# todo check if exist
class AddFriendView(LoginRequiredMixin, View):
    def post(self, request):
        if self.request.user:
            obj = Friend(owner_id=self.request.user.id,
                         liked_id=self.request.POST.get("id"))
            obj.save()
            return HttpResponse(status=204)
        return HttpResponse(status=403)


class FriendDeleteView(LoginRequiredMixin, DeleteView):
    model = Friend
    template_name = 'friends/deletefriend.html'
    success_url = reverse_lazy('friends')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != self.request.user:
            raise PermissionDenied()
        return super(FriendDeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        Friend.objects.filter(owner = obj.liked, liked = obj.owner).delete()
        return super(FriendDeleteView, self).delete(request, *args, **kwargs)


class AcceptFriendListView(LoginRequiredMixin, FilterView):
    model = Friend
    template_name = 'friends/accept.html'
    paginate_by = 3

    def get_queryset(self):
        queryset = super(AcceptFriendListView, self).get_queryset().filter(
            liked=self.request.user, accepted=False).filter(liked__is_active=True)
        return queryset

@login_required
def AcceptAddListView(request, pk):
    obj = Friend.objects.filter(id=pk).get()
    if obj.liked != request.user:
        raise PermissionDenied()
    else:
        obj.accepted=True
        obj.save()
        obj1 = Friend(owner_id=request.user.id,liked_id=obj.owner.id, accepted=True)
        obj1.save()
    return redirect('acceptlistfriend')


class AcceptDeleteListView(LoginRequiredMixin, DeleteView):
    model = Friend
    template_name = 'friends/deletefriend.html'
    success_url = reverse_lazy('friends')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.liked != self.request.user:
            raise PermissionDenied()
        return super(AcceptDeleteListView, self).dispatch(request, *args, **kwargs)