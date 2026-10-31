# devsecops-pipeline-templates

[![example](https://github.com/mest0006/devsecops-pipeline-templates/actions/workflows/example.yml/badge.svg)](https://github.com/mest0006/devsecops-pipeline-templates/actions/workflows/example.yml)

Reusable GitHub Actions workflows that give any repository a secure delivery pipeline in one short file: secret scanning, static analysis, IaC scanning, container scanning, an SBOM, and keyless image signing with verification. The idea is a golden path: teams get security gates by default instead of rebuilding them per repo.

## Templates

| Workflow | What it does | Fails the build when |
|---|---|---|
| `secret-scan.yml` | gitleaks over the full git history | a secret is found |
| `sast.yml` | CodeQL static analysis; results land in the Security tab | CodeQL reports an error-level alert (configurable in repo settings) |
| `iac-scan.yml` | `terraform fmt` check plus Checkov | formatting is off, or Checkov finds a misconfiguration (unless `soft-fail: true`) |
| `container.yml` | build, Trivy scan, SPDX SBOM; on the default branch push to GHCR, sign with cosign (GitHub OIDC, no stored keys) and attach the SBOM as an attestation; outputs the image digest | a fixable HIGH or CRITICAL vulnerability is found |

## Use it from another repo

```yaml
jobs:
  secrets:
    uses: mest0006/devsecops-pipeline-templates/.github/workflows/secret-scan.yml@main

  image:
    needs: secrets
    uses: mest0006/devsecops-pipeline-templates/.github/workflows/container.yml@main
    permissions:
      contents: read
      packages: write
      id-token: write
    with:
      context: .
      image-name: my-service

  deploy:
    needs: image
    runs-on: ubuntu-latest
    steps:
      - run: echo "deploy ghcr.io/${{ github.repository_owner }}/my-service@${{ needs.image.outputs.digest }}"
```

Pin `@main` to a release tag or commit SHA in production so template changes roll out deliberately.

## Example

`.github/workflows/example.yml` runs every template against the small app in `example-app/`, then verifies the image signature with `cosign verify`, checking that it was signed by this repository's workflow through GitHub's OIDC issuer. That last step is what an admission controller (for example a Kyverno `verifyImages` rule) would do before letting the image run.

## Design notes

- **Least privilege.** Each template defaults to `contents: read`; jobs request `packages: write` or `id-token: write` only where they push or sign, and callers must grant them explicitly.
- **Keyless signing.** cosign uses the workflow's short-lived OIDC identity, so there is no signing key to store, rotate or leak.
- **Digest out, digest in.** The container template outputs the digest, so deploy jobs pin exactly the image that was scanned and signed.
- **Scans fail on fixable issues.** `ignore-unfixed` keeps the gate actionable: a red build always has a fix available.

## License

MIT
