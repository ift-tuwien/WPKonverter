# Development

While not strictly required we assume that you installed:

- [`gh`](https://cli.github.com),
- [`just`](https://github.com/casey/just) and
- [`uv`](https://docs.astral.sh/uv)

in the description below.

## Release

**Note:** Please replace `<VERSION>` with the version number e.g. `0.0.1` in the text below

To release a new version of WPKonverter, please use the following steps:

1. Switch to the `main` branch

   ```sh
   git switch main
   ```

2. Check that the [**CI jobs** for the `main` branch finish successfully][GitHub Actions]

   [GitHub Actions]: https://github.com/ift-tuwien/WPKonverter/actions

3. Change the version number and commit your changes:

   ```sh
   just release <VERSION>
   ```

   **Note:** [GitHub Actions][] will publish a package based on the tagged commit and upload it to [PyPi](https://pypi.org/project/wpkonverter/).

4. Publish your release on GitHub:

   ```sh
   gh release create
   ```

   1. Choose the tag for the latest release
   2. As title use “Version `<VERSION>`”, e.g. “Version 0.0.1”
   3. Choose “Write my own”
   4. Paste the release notes for the latest version into the text editor window
   5. Save and close the text file
   6. Answer “N” to the question “Is this a prerelease?”
