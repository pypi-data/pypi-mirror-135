# fastack-mail

Simple plugin for sending email.

This plugin is inspired by [fastapi-mail](https://github.com/sabuhish/fastapi-mail)

## Installation

```
pip install fastack-mail
```

## Usage

### Install plugin

```py
PLUGINS = [
    ...,
    "fastack_mail",
]
```

### Configuration

* `EMAIL_BACKEND` = "fastack_mail.backend.EmailBackend" [required]
* `EMAIL_HOSTNAME` = SMTP Server (e.g. "localhost") [required]
* `EMAIL_PORT` = SMTP Port Server (e.g. 8025) [required]
* `EMAIL_USERNAME` = SMTP username (e.g. "john@doe.com") [optional]
* `EMAIL_PASSWORD` = SMTP password (e.g. "luarbiasa") [optional]
* `EMAIL_TIMEOUT` = Connection time out (default 60) [optional]
* `EMAIL_USE_TLS` = If `True`, make the _initial_ connection to the server over TLS/SSL (default False)
* `EMAIL_START_TLS` = If `True`, make the _initial_ connection to the server over plaintext, and then upgrade the connection to TLS/SSL. Not compatible with `EMAIL_USE_TLS`. (default False)
* `EMAIL_VALIDATE_CERTS` = Determines if server certificates are validated (default True)
* `EMAIL_CLIENT_CERT` = Path to client side certificate, for TLS verification. (default None)
* `EMAIL_CLIENT_KEY` = Path to client side key, for TLS verification. (default None)
* `EMAIL_CERT_BUNDLE` = Path to certificate bundle, for TLS verification. (default None)
* `EMAIL_ASYNC_MODE` = If `True`, the `EmailBackend.send` function returns an awaitable object, if `False` it returns an immediate send result. (default False)
* `DEFAULT_FROM_EMAIL` = Default sender email for use globally (if there is no sender email) (e.g. "Local \<noreply@localhost\>")

### Example

See here https://github.com/fastack-dev/fastack-mail/tree/main/examples/mail
