import redis
import logging

from django.utils.encoding import force_str
from django.conf import settings

from redis_sessions.session import RedisServer

from dnoticias_auth.exceptions import InvalidSessionParameters

logger = logging.getLogger(__name__)


class KeycloakSessionStorage:
    REDIS_PREFIX = settings.DJANGO_KEYCLOAK_ASSOC_REDIS

    def __init__(self, keycloak_session_id: str, django_session_id: str):
        self.server = RedisServer(None).get()
        self.keycloak_session_id = keycloak_session_id
        self.django_session_id = django_session_id

        if not any([self.keycloak_session_id, self.django_session_id]):
            raise InvalidSessionParameters()

    def load(self):
        try:
            session_data = self.server.get(self.get_real_stored_key())
            return force_str(session_data)
        except:
            return {}

    def exists(self):
        return self.server.exists(self.get_real_stored_key())

    def create_or_update(self):
        if self.exists():
            data = self.load()
            if self.django_session_id in data:
                logger.debug(
                    "Session %s already exists for keycloak sid: %s, skipping",
                    self.django_session_id,
                    self.keycloak_session_id,
                )
                return
            self.django_session_id = f"{data},{self.django_session_id}"
            self.delete()

        self.save()

    def save(self):
        logger.debug("Saving key: %s", self.keycloak_session_id)
        if redis.VERSION[0] >= 2:
            self.server.setex(
                self.get_real_stored_key(),
                self.get_expiry_age(),
                self.django_session_id
            )
        else:
            self.server.set(self.get_real_stored_key(), self.django_session_id)
            self.server.expire(self.get_real_stored_key(), self.get_expiry_age())

    def delete(self):
        logger.debug("Deleting key: %s", self.keycloak_session_id)

        try:
            self.server.delete(self.get_real_stored_key())
        except:
            pass

    def get_real_stored_key(self) -> str:
        return f"{self.REDIS_PREFIX}:{self.keycloak_session_id}"

    def get_expiry_age(self, **kwargs):
        return 3600 * 24 * 365


class GenericSessionStorage:

    def __init__(self, key: str):
        self.server = RedisServer(None).get()
        self.key = key

    def load(self):
        try:
            session_data = self.server.get(self.key)
            return force_str(session_data)
        except:
            return {}

    def delete(self):
        logger.debug("Deleting key: %s", self.key)

        try:
            self.server.delete(self.key)
        except:
            pass
