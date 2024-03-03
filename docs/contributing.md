# Contributing

Contributions are welcome for bug fixes and new features. The code style is [ruff](https://docs.astral.sh/ruff/).

## Development Environment

Docker can be used to set up and manage your development environment. This approach helps maintain consistency across development setups and simplifies the process of running integration tests against different databases.

### Setting Up

You'll need Docker and Docker Compose. Once installed, you can build and start the development environment using the following commands:

```bash
docker-compose build
docker-compose up -d
```

These build the necessary Docker images and start the services defined in `docker-compose.yml` (in detached mode).

### Running Integration Tests

Docker is used for integration tests to start instances of Microsoft SQL Server, PostgreSQL, MySQL, and Oracle. This setup allows tests to be run in environments that closely mimic production.

To run the integration tests use:

```bash
docker-compose run --rm app sh ./tests/integration/setup/docker-entrypoint.sh
```

The entry point script ensures that all necessary databases are correctly configured before executing the tests.

Once finished, you can tear down your environment using:

```bash
docker-compose down
```

## Making a Contribution

To make a contribution:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes.
4. Push your branch and submit a pull request against the main project repository.
