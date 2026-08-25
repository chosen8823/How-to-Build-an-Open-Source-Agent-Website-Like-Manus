# Dudenty Git signing

The Dudenty canon release commit and tag are signed with a dedicated Ed25519
key belonging to `chosen8823`.

- Fingerprint: `SHA256:Bu1cOkdByRRo+JylnTyUk/0J7Xkhzl+dP0BkHg4nNXM`
- Public key: `docs/signing/dudenty_git_signing_ed25519.pub`
- Allowed signers: `docs/signing/allowed_signers`

The private key is not stored in this repository.

After cloning, verify a commit or tag with:

```powershell
git -c gpg.format=ssh `
  -c gpg.ssh.allowedSignersFile=docs/signing/allowed_signers `
  verify-commit <commit>

git -c gpg.format=ssh `
  -c gpg.ssh.allowedSignersFile=docs/signing/allowed_signers `
  verify-tag dudenty-canon-v0.1.0
```

GitHub can independently display the signature as verified after the public
key is added to the originator's GitHub account as an SSH signing key.
