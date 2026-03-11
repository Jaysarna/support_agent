This project is a Python-based tool designed to help streamline customer support workflows. It focuses on automating common support tasks and integrating easily with existing ticketing systems. It was a fun project to build to improve efficiency for support teams.

### Support Agent

making use of AI api answering support issues and guide ticket

##Demo

https://github.com/user-attachments/assets/1f4df87f-b60d-422b-8b81-4c02fc378954

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app support_agent
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/support_agent
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit




