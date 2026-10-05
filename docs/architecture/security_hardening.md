# Platform security and deployment hardening guide

## TLS and access policy

- Enable TLS on MQTT broker endpoints in production
- Use mTLS or client certificates for device authentication where possible
- Limit public network surface to the required ports only
- Place Postgres behind a private network or internal service mesh

## Authentication and session policy

- Use a strong secret key in production and rotate it periodically
- Keep session cookies `HttpOnly`, `Secure`, and `SameSite=Lax`
- Require MFA for admin access to Grafana and cloud dashboards

## Data protection and compliance

- Log all ingestion, forecast, and route assignment events for review
- Retain telemetry using a clearly documented retention policy
- Separate production config from code and source control
- Restrict access to raw sensors and operational data to approved roles
