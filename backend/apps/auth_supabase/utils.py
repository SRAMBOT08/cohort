import ssl
from django.core.mail.backends.smtp import EmailBackend

class UnverifiedEmailBackend(EmailBackend):
    """
    Custom EmailBackend to bypass SSL certificate verification.
    USE ONLY FOR DEVELOPMENT/DEBUGGING when local certs are broken.
    """
    def _get_ssl_context(self):
        # Create an unverified SSL context
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx
