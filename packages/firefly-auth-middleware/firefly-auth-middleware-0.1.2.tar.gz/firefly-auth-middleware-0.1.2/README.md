# Firefly Auth Middleware

This plugin provides an authenticator to use in conjunction with firefly-iaaa. Simply install the plugin and add a
line to your firefly.yml like so:

```yaml
contexts:
  firefly_auth_middleware: ~
```

If your IAAA service is named anything other than iaaa, you can configure that in your firefly.yml as well:

```yaml
contexts:
  firefly_auth_middleware:
    auth_service: my_identity_service  # Defaults to 'iaaa'
```