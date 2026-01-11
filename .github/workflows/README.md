# One-Click Deployment Resources

This directory contains GitHub Actions workflows for validating deployment configurations.

## Workflows

### validate-deployment.yml
Automatically validates deployment configuration files when code is pushed:
- ✅ Validates JSON files (app.json)
- ✅ Validates YAML files (service.yaml, button.yaml)
- ✅ Checks Python syntax
- ✅ Verifies required files exist
- ✅ Validates Dockerfile syntax

This ensures the one-click deployment button always works correctly.

## Contributing

If you're contributing to this project, the validation workflow will automatically run on your pull requests to ensure deployment configurations remain valid.
