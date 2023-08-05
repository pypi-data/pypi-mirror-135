import logging

from django.views.decorators.clickjacking import xframe_options_exempt
from django.http.response import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.shortcuts import render
from django.conf import settings

from mozilla_django_oidc.views import OIDCLogoutView, OIDCAuthenticationCallbackView


from .utils import delete_user_sessions, get_cookie_equivalency
from .redis import KeycloakSessionStorage

logger = logging.getLogger(__name__)


class SilentCheckSSOView(View):
    @method_decorator(xframe_options_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, "authentication/silent-check-sso.html", locals())


class DnoticiasOIDCLogoutView(OIDCLogoutView):
    http_method_names = ['get', 'post']

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @property
    def redirect_url(self) -> str:
        """
        This function was created using the keycloak redirect URL as a LOGOUT_REDIRECT_URL
        /auth/realms/<realm>/protocol/openid-connect/logout?redirect_uri=<URL>

        If we provide a next value via POST, the redirect_uri will be that value.
        If we do not have a next value, the redirect_uri will be the base url.
        """
        logout_url = self.get_settings('LOGOUT_REDIRECT_URL', None)
        base_url = self.get_settings('BASE_URL', None)
        next_url = self.request.POST.get('next') or self.request.GET.get('next', '') or base_url

        if not logout_url:
            logout_url = ''
            logger.warning("No LOGOUT_REDIRECT_URL configured!")

        if not base_url:
            base_url = '/'
            logger.warning("No BASE_URL configured! Using / as default...")

        return logout_url + next_url if logout_url else base_url

    def post(self, request) -> HttpResponseRedirect:
        """
        This method extends the original oidc logout method and aditionally deletes
        the authentication cookies
        """
        keycloak_session_id = request.session.get("keycloak_session_id")

        if not keycloak_session_id:
            keycloak_session_id = request.COOKIES.get(get_cookie_equivalency("keycloak_session_id"))

        delete_user_sessions(keycloak_session_id)
        super().post(request)

        # Response is defined first because we need to delete the cookies before redirect
        response = HttpResponseRedirect(self.redirect_url)
        auth_cookies = get_cookie_equivalency(all_names=True)
        extra = {
            "domain": settings.AUTH_COOKIE_DOMAIN,
            "samesite": "Strict"
        }

        # Deletes ONLY the cookies that we need
        [response.delete_cookie(cookie, **extra) for _, cookie in auth_cookies.items()]

        return response


class DnoticiasOIDCAuthenticationCallbackView(OIDCAuthenticationCallbackView):

    def get(self, request):
        response = super().get(request)

        request.session["keycloak_session_id"] = request.GET.get("session_state")
        request.session.save()

        try:
            keycloak_session = KeycloakSessionStorage(
                request.session["keycloak_session_id"],
                request.session.session_key,
            )

            keycloak_session.create_or_update()
        except:
            logger.exception("Something wrong was happened :(")

        return response
