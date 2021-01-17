from rest_framework import serializers, exceptions
from rest_framework.authtoken.models import Token

from dj_rest_auth.serializers import LoginSerializer as DRALoginSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer as DRARegisterSerializer

from allauth.account.utils import _has_verified_for_login, send_email_confirmation

from django.contrib.auth.models import User

from matching.serializers import MatchingEntrySerializer


# TODO: Make it so that when you change your password your tokens are changed
class UserDetailsSerializer(serializers.ModelSerializer):
    matching_entry = MatchingEntrySerializer(allow_null=True)
    is_matcher = serializers.SerializerMethodField()
    def get_is_matcher(self, user):
        return user.has_perm('matching.is_matcher')
    is_moderator = serializers.SerializerMethodField()
    def get_is_moderator(self, user):
        return user.has_perm('matching.is_moderator')

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_staff', 'is_matcher', 'is_moderator', 'first_name', 'last_name',
                  'matching_entry')
        read_only_fields = ('email', 'matching_entry')


class LoginSerializer(DRALoginSerializer):
    def authenticate(self, **kwargs):
        user = super().authenticate(**kwargs)
        if not user:
            return user
        if not _has_verified_for_login(user, user.email):
            send_email_confirmation(self.context['request'], user, signup=False, email=user.email)
            raise exceptions.ValidationError("You need to verify your email before you can login. "
                                             "We have sent you another email.")
        return user



class LoginResponseSerializer(serializers.ModelSerializer):
    token = serializers.CharField(source='key')
    user = UserDetailsSerializer()

    class Meta:
        model = Token
        fields = ('token', 'user')


class RegisterSerializer(DRARegisterSerializer):
    first_name = serializers.CharField(max_length=150, allow_blank=True)
    last_name = serializers.CharField(max_length=150, allow_blank=True)

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', '')
        }


class UserDeleteSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)

    def __init__(self, *args, **kwargs):
        super(UserDeleteSerializer, self).__init__(*args, **kwargs)

        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)

    def validate_old_password(self, value):
        if not self.user.check_password(value):
            err_msg = "Your old password was entered incorrectly. Please enter it again."
            raise serializers.ValidationError(err_msg)
        return value
