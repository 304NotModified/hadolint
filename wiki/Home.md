# Hadolint Rules Wiki

Welcome to the Hadolint rules documentation. This wiki provides detailed information about each linting rule.

## About Hadolint

Hadolint is a Dockerfile linter that helps you build best practice Docker images. It parses the Dockerfile into an AST and performs rules on top of the AST.

## Quick Links

- [Main Repository](https://github.com/hadolint/hadolint)
- [Installation Guide](https://github.com/hadolint/hadolint#install)
- [Configuration Options](https://github.com/hadolint/hadolint#configure)
- [Integration Guide](https://github.com/hadolint/hadolint/blob/master/docs/INTEGRATION.md)

## Rules by Category

### DL1xxx - Ignore Rules

These rules relate to the use of ignore pragmas.

- **[DL1001](DL1001)** (Ignore): Please refrain from using inline ignore pragmas `# hadolint ignore=DLxxxx`.

### DL3xxx - Dockerfile Rules

These rules help enforce best practices when writing Dockerfiles.

- **[DL3000](DL3000)** (Error): Use absolute WORKDIR
- **[DL3001](DL3001)** (Info): For some bash commands it makes no sense running them in a Docker container like `ssh`, `vim`, `shutdown`, `service`, `ps`, `free`, `top`, `kill`, `mount`, `ifconfig`
- **[DL3002](DL3002)** (Warning): Last USER should not be root
- **[DL3003](DL3003)** (Warning): Use WORKDIR to switch to a directory
- **[DL3004](DL3004)** (Error): Do not use sudo as it leads to unpredictable behavior. Use a tool like gosu to enforce root
- **[DL3006](DL3006)** (Warning): Always tag the version of an image explicitly
- **[DL3007](DL3007)** (Warning): Using latest is prone to errors if the image will ever update. Pin the version explicitly to a release tag
- **[DL3008](DL3008)** (Warning): Pin versions in apt get install. Instead of `apt-get install <package>` use `apt-get install <package>=<version>`
- **[DL3009](DL3009)** (Info): Delete the apt lists (/var/lib/apt/lists) after installing something
- **[DL3010](DL3010)** (Info): Use `ADD` for extracting archives into an image
- **[DL3011](DL3011)** (Error): Valid UNIX ports range from 0 to 65535
- **[DL3012](DL3012)** (Error): Multiple `HEALTHCHECK` instructions
- **[DL3013](DL3013)** (Warning): Pin versions in pip. Instead of `pip install <package>` use `pip install <package>==<version>` or `pip install --requirement <requirements file>`
- **[DL3014](DL3014)** (Warning): Use the `-y` switch to avoid manual input `apt-get -y install <package>`
- **[DL3015](DL3015)** (Info): Avoid additional packages by specifying `--no-install-recommends`
- **[DL3016](DL3016)** (Warning): Pin versions in npm. Instead of `npm install <package>` use `npm install <package>@<version>`
- **[DL3018](DL3018)** (Warning): Pin versions in apk add. Instead of `apk add <package>` use `apk add <package>=<version>`
- **[DL3019](DL3019)** (Info): Use the `--no-cache` switch to avoid the need to use `--update` and remove `/var/cache/apk/*` when done installing packages
- **[DL3020](DL3020)** (Error): Use COPY instead of ADD for files and folders
- **[DL3021](DL3021)** (Error): COPY with more than 2 arguments requires the last argument to end with /
- **[DL3022](DL3022)** (Warning): `COPY --from` should reference a previously defined `FROM` alias
- **[DL3023](DL3023)** (Error): `COPY --from` cannot reference its own `FROM` alias
- **[DL3024](DL3024)** (Error): FROM aliases (stage names) must be unique
- **[DL3025](DL3025)** (Warning): Use arguments JSON notation for CMD and ENTRYPOINT arguments
- **[DL3026](DL3026)** (Error): Use only an allowed registry in the FROM image
- **[DL3027](DL3027)** (Warning): Do not use apt as it is meant to be an end-user tool, use apt-get or apt-cache instead
- **[DL3028](DL3028)** (Warning): Pin versions in gem install. Instead of `gem install <gem>` use `gem install <gem>:<version>`
- **[DL3029](DL3029)** (Warning): Do not use --platform flag with FROM
- **[DL3030](DL3030)** (Warning): Use the -y switch to avoid manual input `yum install -y <package>`
- **[DL3032](DL3032)** (Warning): `yum clean all` missing after yum command.
- **[DL3033](DL3033)** (Warning): Specify version with `yum install -y <package>-<version>`.
- **[DL3034](DL3034)** (Warning): Non-interactive switch missing from `zypper` command: `zypper install -y`
- **[DL3035](DL3035)** (Warning): Do not use `zypper dist-upgrade`.
- **[DL3036](DL3036)** (Warning): `zypper clean` missing after zypper use.
- **[DL3037](DL3037)** (Warning): Specify version with `zypper install -y <package>=<version>`.
- **[DL3038](DL3038)** (Warning): Use the -y switch to avoid manual input `dnf install -y <package>`
- **[DL3040](DL3040)** (Warning): `dnf clean all` missing after dnf command.
- **[DL3041](DL3041)** (Warning): Specify version with `dnf install -y <package>-<version>`.
- **[DL3042](DL3042)** (Warning): Avoid use of cache directory with pip. Use `pip install --no-cache-dir <package>`
- **[DL3043](DL3043)** (Error): `ONBUILD`, `FROM` or `MAINTAINER` triggered from within `ONBUILD` instruction.
- **[DL3044](DL3044)** (Error): Do not refer to an environment variable within the same `ENV` statement where it is defined.
- **[DL3045](DL3045)** (Warning): `COPY` to a relative destination without `WORKDIR` set.
- **[DL3046](DL3046)** (Warning): `useradd` without flag `-l` and high UID will result in excessively large Image.
- **[DL3047](DL3047)** (Info): Avoid use of wget without progress bar. Use `wget --progress=dot:giga <url>`. Or consider using `-q` or `-nv` (shorthands for `--quiet` or `--no-verbose`).
- **[DL3048](DL3048)** (Style): Invalid label key.
- **[DL3049](DL3049)** (Info): Label `
- **[DL3050](DL3050)** (Info): Superfluous label(s) present.
- **[DL3051](DL3051)** (Warning): label `
- **[DL3052](DL3052)** (Warning): Label `
- **[DL3053](DL3053)** (Warning): Label `
- **[DL3054](DL3054)** (Warning): Label `
- **[DL3055](DL3055)** (Warning): Label `
- **[DL3056](DL3056)** (Warning): Label `<label>` does not conform to semantic versioning.
- **[DL3057](DL3057)** (Ignore): `HEALTHCHECK` instruction missing.
- **[DL3058](DL3058)** (Warning): Label `
- **[DL3059](DL3059)** (Info): Multiple consecutive `RUN` instructions. Consider consolidation.
- **[DL3060](DL3060)** (Info): `yarn cache clean` missing after `yarn install` was run.
- **[DL3061](DL3061)** (Error): Invalid instruction order. Dockerfile must begin with `FROM`, `ARG` or comment.
- **[DL3062](DL3062)** (Warning): Pin versions in go. Instead of `go install <package>` use `go install <package>@<version>`

### DL4xxx - Maintainer Rules

These rules relate to MAINTAINER instructions and deprecated syntax.

- **[DL4000](DL4000)** (Error): MAINTAINER is deprecated
- **[DL4001](DL4001)** (Warning): Either use Wget or Curl but not both
- **[DL4003](DL4003)** (Warning): Multiple `CMD` instructions found. If you list more than one `CMD` then only the last `CMD` will take effect
- **[DL4004](DL4004)** (Error): Multiple `ENTRYPOINT` instructions found. If you list more than one `ENTRYPOINT` then only the last `ENTRYPOINT` will take effect
- **[DL4005](DL4005)** (Warning): Use SHELL to change the default shell
- **[DL4006](DL4006)** (Warning): Set the SHELL option -o pipefail before RUN with a pipe in it. If you are using /bin/sh in an alpine image or if your shell is symlinked to busybox then consider explicitly setting your SHELL to /bin/ash, or disable this check

## Severity Levels

- **Error**: Critical issues that should always be fixed
- **Warning**: Important issues that should typically be addressed
- **Info**: Informational suggestions for improvement
- **Style**: Code style recommendations

## Configuration

See the [configuration documentation](https://github.com/hadolint/hadolint#configure) for information on how to:
- Ignore specific rules globally or inline
- Override rule severities
- Set failure thresholds
- Configure trusted registries

## Contributing

If you find issues or want to improve these documentation pages, please contribute to the [Hadolint project](https://github.com/hadolint/hadolint).

## License

Hadolint is licensed under GPL-3.0. See the [LICENSE](https://github.com/hadolint/hadolint/blob/master/LICENSE) file for details.
