from django.contrib.auth import get_user_model

# from rest_framework import serializers
# from rest_framework.reverse import reverse
# from .models import *

User = get_user_model()


# class UserSerializer(serializers.ModelSerializer):

#     full_name = serializers.CharField(source="get_full_name", read_only=True)

#     class Meta:
#         model = User
#         fields = ('id', User.USERNAME_FIELD, 'full_name', 'is_active', )

#     def get_links(self, obj):
#         request = self.context['request']
#         username = obj.get_username()
#         return {
#             'self': reverse('user-detail', kwargs ={User.USERNAME_FIELD: username}, request=request),
#         }

