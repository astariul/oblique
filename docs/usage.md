# Usage

## Create your repository

The very first step is to create your own repository from this template repository. To do this, just click the button "Use this template" :

<p align="center">
  <a href="https://github.com/astariul/oblique/generate"><img src="https://img.shields.io/badge/%20-Use%20this%20template-green?style=for-the-badge&color=347d39" alt="Use template" /></a>
</p>

It will prompt you to create a new Github repository.

## Add your content

Once your repository is created, you can just clone it and replace the dummy content with ***your*** content.

To be sure you don't forget to replace anything, here is an exhaustive list of steps to follow :

### Change `setup.py`

In `setup.py`, replace the `name` of the package, the `version`, the `author` and the `author_email`, the package `description`, and the package `url`.

### Replace `README.md`

You can keep the same README outline, but you must update the core content.

Make sure to search for any occurence of the string `astariul/oblique` and replace it with your own `<user>/<repo>`.

Make sure to search for any occurence of the string `astariul` and replace it with your own username.

Make sure to search for any occurence of the string `oblique` and replace it with the name of your package.

!!! important
    Don't forget to carefully read your README and edit each section with a content that fit your package !

### Update the documentation

In the file `mkdocs.yml`, replace the `site_name`, `repo_url`, `repo_name`.

Of course you also need to update the content of the documentation. You can do this by updating the `md` files in the `docs/` folder.

For the code reference (in `docs/code_ref.md`), make sure to change the name from `oblique` to the name of your package.

!!! info
    The documentation will be published in Github page ***after*** you create a Github release.

### Change the package name and content

Make sure to replace the name of the folder `oblique/`, which contains the source code of the package, to the name of ***your*** package.

Of course change the routes, components, and core logic to put your actual application !

### Update the configuration file

In the configuration file `pyproject.toml`, you should replace the name `oblique` with the name of your package.

### Replace the tests

If you removed the existing template code, the tests will not pass anymore ! Make sure to write new tests to validate your application logic.

### Update names and links in `.github/` folder

A few links to update in `.github/` folder :

* In `.github/ISSUE_TEMPLATE/bug.yaml`, replace `oblique` by the name of your package.
* In `.github/ISSUE_TEMPLATE/config.yml`, replace `astariul/oblique` by your `<user>/<repo>`.
* In `.github/workflows/mike_dev.yaml`, replace `oblique` by your package name.
* In `.github/workflows/mike_stable.yaml`, replace `oblique` by your package name.

### Optionally

Optionally, if there is some features you don't want (like the Github action that automatically publish the documentation), you can remove it !

Head over to the [Features](features.md) page to see which file to remove.

## Enable Dependabot

From the Github website, on your repository page, you can enable [Dependabot](https://docs.github.com/en/code-security/supply-chain-security/managing-vulnerabilities-in-your-projects-dependencies/configuring-dependabot-security-updates#enabling-or-disabling-dependabot-security-updates-for-an-individual-repository) by going to the `Settings` tab of your repository, then in the `Security & analysis` section you can enable `Dependabot alerts` and `Dependabot security updates`.
