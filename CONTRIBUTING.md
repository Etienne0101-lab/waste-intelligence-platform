# Contributing

Thank you for contributing to the Distributed IoT Mesh Waste-Intelligence Platform.

## Development workflow

1. Fork the repository.
2. Create a feature branch.
3. Keep changes scoped to a single concern whenever possible.
4. Add tests for new logic or modules.
5. Run linting and unit tests before opening a pull request.
6. Submit a pull request with a clear description of the change.

## Code standards

- Use Python for cloud and analytics services.
- Use Flask for hub APIs.
- Use ESP32 C++ for firmware.
- Add comments, docstrings, and exception handling to all production code.
- Stack environment-specific configuration in `.env` files, not source code.
- Use Docker for repeatable deployments.

## Testing requirements

- Add unit tests for new modules and utilities.
- Validate integration points between mesh, hub, and cloud layers.
- Prefer deterministic tests with mocked telemetry where possible.

## Pull request checklist

- [ ] Code is formatted and linted
- [ ] Unit tests pass
- [ ] Documentation updated
- [ ] Security-sensitive values use environment variables
- [ ] Changes align with the Hub-and-Spoke architecture
