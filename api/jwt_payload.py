from hashlib import md5

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        user_groups = []
        for g in user.groups.all():
            user_groups.append(g.name)
        token["name"] = user.get_full_name()
        token["email"] = user.email
        token["groups"] = user_groups
        # The following hash is not used in any security context.
        token["gravator_url"] = "https://www.gravatar.com/avatar/{0}".format(
            md5(user.email.strip(" \t\n\r").encode("utf-8")).hexdigest()  # nosec
        )
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
