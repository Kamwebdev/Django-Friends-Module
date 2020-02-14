from accounts.models import UserProfile, User
import django_filters


class UsersFilter(django_filters.FilterSet):

    class Meta:
        model = UserProfile
        fields = {'user__first_name':['iexact'], 'user__last_name':['iexact'], 'city':['iexact']}
        #exclude = ['',]