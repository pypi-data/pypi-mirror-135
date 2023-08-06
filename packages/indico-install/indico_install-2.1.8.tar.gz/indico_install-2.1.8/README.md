# Indico Platform Management
[![Codeship Status for IndicoDataSolutions/indico-install](https://app.codeship.com/projects/52ec5580-2390-0138-f313-5e60cb46bbdf/status?branch=development)](https://app.codeship.com/projects/383042)

This repository contains tools to create and manage Indico K8S clusters. It is used by anyone who works with an Indico K8S Cluster.
Split off from indico-deployment, the docker container and CLI in this repository are kept consistent with original expectations

- [Introduction and Setup](https://github.com/IndicoDataSolutions/indico-deployment/wiki/Introduction-and-Setup)
- [Wiki](https://github.com/IndicoDataSolutions/indico-deployment/wiki)
- [Contributing](#contributing)


## Contributing
When making any changes to the CLI or tools, please appropriately document them in the wiki and include the updated pages as part of your PR.

## Version Updates
Update the version number in setup.py as part of PR, after testing thoroughly
Add any changes to the CHANGELOG

## Dependency Management
The indico-install tool has logical dependencies (minimally pinned), while the indico-deployment container has concrete dependencies (pinned versions of dependencies and sub-dependencies). Concrete dependencies are required for the indico-deployment container because we need stable and reproducable environments for managing clusters. Logical dependencies for the indico-install library are stored in `setup.py` and concrete dependencies for the indico-deployment tool are stored in the `requirements.txt`

And added benefit of maintaining logical and concrete dependencies is much faster builds. Due to the large amount of dependencies in the project and [backtracking](https://pip.pypa.io/en/latest/topics/dependency-resolution/#backtracking) in pip, dependency resolution can take an unreasonable amount of time (see [here](https://github.com/pypa/pip/issues/9517) for more details). By using [pip-tools](https://github.com/jazzband/pip-tools), we can easily specify the exact version dependencies and sub-dependencies.

### Updating dependencies
Updating dependencies can be done by adding the logical requirement to setup.py and running:
```
python3 -m pip install pip-tools==6.2.0
pip-compile setup.py --extra=aks --extra=eks --extra=indico --extra=saml
```

This command consumes the logical dependencies in setup.py and produces a resolved requirements.txt with pinned dependencies. This new requirements.txt file should then be added in a PR.

For more information, read the pip-tools README: https://github.com/jazzband/pip-tools
