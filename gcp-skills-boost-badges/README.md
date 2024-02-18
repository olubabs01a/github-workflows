# Import Badges from Google Cloud Skills Boost ☁️🏆
## Introduction
Keep your profile README updated with your latest achievements in Google Cloud Skills Boost!

## Prerequisites
#### Make your Google Cloud Skills Boost profile public 🌐
It's time to show off those awesome skills you've been working on! 💪🏾

Your skills profile needs to be public. Not sure how to do this? Follow these [instructions](https://support.google.com/qwiklabs/answer/9222527?hl=en).

## Calling this workflow
```
jobs:
  <job-id>:
    uses: olubabs01a/github-workflows/.github/workflows/update-readme.yaml@<source-branch>
    with:
      skills-boost-url: <public Skills Boost URL>
      target-file: <target file to update>
      badge-count: <max badges displayed>
      repo-name: olubabs01a/github-workflows
      repo-ref: <source-branch>
      clone-path: gcp-skills-boost-badges
    secrets: inherit
```

### Arguments
| Argument Name | Type | Required | Description |
| - | - | - | - |
| `skills-boost-url` | _string_ | True | URL for public Skills Boost profile |
| `target-file` | _string_ | True | Target file to update with badges, e.g. `README.md` |
| `badge-count` | _number_ | True | Maximum number of badges to display in target file |
| `repo-name` | _string_ | True | The repository where the workflow is contained, i.e. `olubabs01a/github-workflows` |
| `repo-ref` | _string_ | True | Branch or tag name. |
| `clone-path` | _string_ | True | Folder containing Skills badges workflow, i.e. `gcp-skills-boost-badges` |

### Required placeholder pattern in target file, e.g. `README.md`
```
<!-- start latest badges -->
<!-- end latest badges -->
```

### Required permissions
This workflow will commit and push changes made from checking latest imports.
```
permissions:
  contents: write
```
