# custom email backend para que ferozo no tire error de ssl por cert auto-firmado
import ssl
import smtplib

from django.core.mail.backends.smtp import EmailBackend


class FerozoEmailBackend(EmailBackend):
    # smtp con ssl desactivado para ferozo


    def _get_ssl_context(self):
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return context

    def open(self):
        if self.connection:
            return False
        try:
            if self.use_ssl:
                self.connection = smtplib.SMTP_SSL(
                    self.host,
                    self.port,
                    context=self._get_ssl_context(),
                    timeout=self.timeout,
                )
            else:
                self.connection = smtplib.SMTP(
                    self.host,
                    self.port,
                    timeout=self.timeout,
                )
            if self.use_tls:
                self.connection.ehlo()
                self.connection.starttls(context=self._get_ssl_context())
                self.connection.ehlo()
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except Exception:
            if not self.fail_silently:
                raise
