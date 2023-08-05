# RobotnikMQ

Utilities for safe, efficient, and scalable infrastructure using RabbitMQ

## Usage

TODO

## Installation & Setup

To install robotnikmq with [`pip`](https://pip.pypa.io/en/stable/) execute the following:

```bash
pip install /path/to/repo/robotnikmq
```

If you don't want to re-install every time there is an update, and prefer to just pull from the git repository, then use the `-e` flag.

### Configuration

RobotnikMQ can be configured globally, on a per-user, or on a per-application basis. When certain functions of the RobotnikMQ library are called without a provided configuration, it will attempt to find a configuration first for the application in the current working directory `./robotnikmq.yaml`, then for the user in `~/.config/robotnikmq/robotnikmq.yaml` and then for the system in `/etc/robotnikmq/robotnikmq.yaml`. An error will be raised if a configuration is not provided and neither of those files exist.

The RobotnikMQ configuration is primarily a list of servers organized into tiers. If a given system or user can be expected to connect to the same cluster the vast majority of the time, then you can/should use a per-user or global configuration. Otherwise, simply have your application configure its own RobotnikMQ configuration (see **Usage** section).

The configuration file itself should look something like this:

```yaml
tiers:
- - ca_cert: /home/eugene/Development/robotnikmq/tests/integration/vagrant/pki/robotnik-ca.crt
    cert: /home/eugene/Development/robotnikmq/tests/integration/vagrant/pki/issued/rabbitmq-vm/rabbitmq-vm.crt
    host: 127.0.0.1
    key: /home/eugene/Development/robotnikmq/tests/integration/vagrant/pki/issued/rabbitmq-vm/rabbitmq-vm.key
    password: ''
    port: 1
    user: ''
    vhost: ''
  - ca_cert: /home/eugene/Development/robotnikmq/tests/integration/vagrant/pki/robotnik-ca.crt
    cert: /home/eugene/Development/robotnikmq/tests/integration/vagrant/pki/issued/rabbitmq-vm/rabbitmq-vm.crt
    host: '1'
    key: /home/eugene/Development/robotnikmq/tests/integration/vagrant/pki/issued/rabbitmq-vm/rabbitmq-vm.key
    password: '1'
    port: 1
    user: '1'
    vhost: '1'
- - ca_cert: /home/eugene/Development/robotnikmq/tests/integration/vagrant/pki/robotnik-ca.crt
    cert: /home/eugene/Development/robotnikmq/tests/integration/vagrant/pki/issued/rabbitmq-vm/rabbitmq-vm.crt
    host: 127.0.0.1
    key: /home/eugene/Development/robotnikmq/tests/integration/vagrant/pki/issued/rabbitmq-vm/rabbitmq-vm.key
    password: hackme
    port: 5671
    user: robotnik
    vhost: /robotnik
```

In the example above, you should be able to see two tiers of servers, the first has two server configurations that are intentionally broken for testing purposes, while the second has a valid configuration (this is the configuration that is used for unit-testing).

The idea is that RobotnikMQ will first attempt to connect to all servers in the first tier in a random order, then if all of them fail, it will attempt to connect to all the servers in the second tier, and so on. This is intended to allow both load-balancing on different servers and for redundancy in case some of those servers fail. You can also configure only one tier with one server, or just a list of tiers, each of which have one server in them. This way, the secondary and tertiary servers would only be used if there is something wrong with the primary.

## Development

### Standards

- Be excellent to each other
- Code coverage must be at 100% for all new code, or a good reason must be provided for why a given bit of code is not covered.
  - Example of an acceptable reason: "There is a bug in the code coverage tool and it says its missing this, but its not".
  - Example of unacceptable reason: "This is just exception handling, its too annoying to cover it".
- The code must pass the following analytics tools. Similar exceptions are allowable as in rule 2.
  - `pylint --disable=C0111,W1203,R0903 --max-line-length=100 ...`
  - `flake8 --max-line-length=100 ...`
  - `mypy --ignore-missing-imports --follow-imports=skip --strict-optional ...`
- All incoming information from users, clients, and configurations should be validated.
- All internal arguments passing should be typechecked whenever possible with `typeguard.typechecked`

### Development Setup

Using [poetry](https://python-poetry.org/) install from inside the repo directory:

```bash
poetry install
```

This will set up a virtualenv which you can always activate with either `poetry shell` or run specific commands with `poetry run`. All instructions below that are meant to be run in the virtualenv will be prefaced with `(robotnikmq)$ `

#### IDE Setup

**Sublime Text 3**

```bash
curl -sSL https://gitlab.com/-/snippets/2066312/raw/master/poetry.sublime-project.py | poetry run python
```

## Testing

All testing should be done with `pytest` which is installed with the `dev` requirements.

To run all the unit tests, execute the following from the repo directory:

```bash
(robotnikmq)$ pytest
```

This should produce a coverage report in `/path/to/dewey-api/htmlcov/`

While developing, you can use [`watchexec`](https://github.com/watchexec/watchexec) to monitor the file system for changes and re-run the tests:

```bash
(robotnikmq)$ watchexec -r -e py,yaml pytest
```

To run a specific test file:

```bash
pytest tests/unit/test_core.py
```

To run a specific test:

```bash
pytest tests/unit/test_core.py::test_hello
```

For more information on testing, see the `pytest.ini` file as well as the [documentation](https://docs.pytest.org/en/stable/).

### Vagrant Testing

When you run `pytest` you may notice that some tests are being skipped with the message "rabbitmq-vm needs to be running", this is because those tests require other services to connect to. RobotnikMQ works primarily with RabbitMQ, as a result, a lot of the tests require a server hosting it. RobotnikMQ comes with a [vagrant testing setup](https://www.vagrantup.com/docs/cli) which can be initialized from the repo directory and executing `vagrant up --provision`. The VM comes with some basic essentials for working with RobotnikMQ. Coincidentally, the virtualized setup happens to serve as a model for how mentat can be configured.

- You can log in with `vagrant ssh`
- The VM hosts a RabbitMQ server with port-forwarding configured
  - You can access the managment UI at: https://localhost:15671/ (username: `vagrant`, password: `Uy7ht9qbbakp5h3p2KiyyEjIX8O7VkuQ`)