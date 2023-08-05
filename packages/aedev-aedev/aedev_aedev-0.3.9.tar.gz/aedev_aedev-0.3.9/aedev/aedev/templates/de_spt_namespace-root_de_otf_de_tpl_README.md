<!-- THIS FILE IS EXCLUSIVELY MAINTAINED by the project aedev.tpl_namespace_root V0.3.8 -->
# {portion_name} {package_version}

[![GitLab develop](https://img.shields.io/gitlab/pipeline/{repo_group}/{package_name}/develop?logo=python)](
    {repo_url})
[![LatestPyPIrelease](
    https://img.shields.io/gitlab/pipeline/{repo_group}/{package_name}/release{pypi_versions[-1]}?logo=python)](
    {repo_url}/-/tree/release{pypi_versions[-1]})
[![PyPIVersions](https://img.shields.io/pypi/v/{package_name})](
    {pypi_url}/#history)

>{project_desc}.

[![Coverage]({repo_pages}/{package_name}/coverage.svg)](
    {repo_pages}/{package_name}/coverage/index.html)
[![MyPyPrecision]({repo_pages}/{package_name}/mypy.svg)](
    {repo_pages}/{package_name}/lineprecision.txt)
[![PyLintScore]({repo_pages}/{package_name}/pylint.svg)](
    {repo_pages}/{package_name}/pylint.log)

[![PyPIImplementation](https://img.shields.io/pypi/implementation/{package_name})](
    {repo_url}/)
[![PyPIPyVersions](https://img.shields.io/pypi/pyversions/{package_name})](
    {repo_url}/)
[![PyPIWheel](https://img.shields.io/pypi/wheel/{package_name})](
    {repo_url}/)
[![PyPIFormat](https://img.shields.io/pypi/format/{package_name})](
    {pypi_url}/)
[![PyPILicense](https://img.shields.io/pypi/l/{package_name})](
    {repo_url}/-/blob/develop/LICENSE.md)
[![PyPIStatus](https://img.shields.io/pypi/status/{package_name})](
    https://libraries.io/pypi/{pip_name})
[![PyPIDownloads](https://img.shields.io/pypi/dm/{package_name})](
    {pypi_url}/#files)


## installation

{TEMPLATE_PLACEHOLDER_ID_PREFIX}{TEMPLATE_INCLUDE_FILE_PLACEHOLDER_ID}{TEMPLATE_PLACEHOLDER_ID_SUFFIX}
    de_icl_README_pre_install.md
{TEMPLATE_PLACEHOLDER_ARGS_SUFFIX}
execute the following command to install the
{import_name} {project_type}
in the currently active virtual environment:
 
```shell script
pip install {pip_name}
```

if you want to contribute to this portion then first fork
[the {package_name} repository at GitLab](
{repo_url} "{import_name} code repository").
after that pull it to your machine and finally execute the
following command in the root folder of this repository
({package_name}):

```shell script
pip install -e .[dev]
```

the last command will install this {project_type} portion, along with the tools you need
to develop and run tests or to extend the portion documentation. to contribute only to the unit tests or to the
documentation of this portion, replace the setup extras key `dev` in the above command with `tests` or `docs`
respectively.

more detailed explanations on how to contribute to this project
[are available here](
{repo_url}/-/blob/develop/CONTRIBUTING.rst)


## namespace portion documentation

information on the features and usage of this portion are available at
[ReadTheDocs](
https://{namespace_name}.readthedocs.io/en/latest/_autosummary/{import_name}.html#module-{import_name}
"{package_name} documentation").
