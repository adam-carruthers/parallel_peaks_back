from allauth.account.adapter import DefaultAccountAdapter

from rest_framework.response import Response


class CustomAccountAdapter(DefaultAccountAdapter):
    def respond_email_verification_sent(self, request, user):
        return Response({"detail": "Verification e-mail sent."})

    def get_email_confirmation_url(self, request, emailconfirmation):
        # TODO: Set this properly if going into production
        return f'http://localhost:3000/confirm-email?token={emailconfirmation.key}'
