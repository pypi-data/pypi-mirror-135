# SDKMS Plugin Registry Builder

This tool builds a SDKMS plugin registry manifest file out of a git repository.
It iterates through each commit and signs it. At each step of the iteration
the tool keeps building the manifest which is a JSON structure with the
following schema:

```json
[
    {
        "name": "<Plugin Name>",
        "versions": {
            "<version>": {
                "path": <path/to/plugin/file>,
                "description": <plugin description>,
                "short_description": <short description used by SDKMS for display in tiles>,
                "release_notes": [
                    <str>,
                    ...
                ],
                "commit": <hexsha>
            },
            ...
        }
    },
    ...
]
```

## Fortanix Plugin Registry

SDKMS Plugin Registries are GIT repositories that contains SDKMS plugins
(custom Lua programs) that can be executed inside SDKMS to achieve certain
business specific logic, or a functionality that is not part of the
core capabilities offered by SDKMS.
The repository should follow the following conventions:

1. Each plugin should have a unique name.
2. There should be just one plugin in each subdirectory.
3. In each subdirectory the following files are required (case-sensitive):
    - `plugin.lua`: Contains the plugin code.
    - `README.md`: Contains a description of the plugin.
    - `metadata.json`: Contains metadata of the plugin. The schema of the JSON should be:

```json
{
    "name": <Plugin name>,
    "version": <Plugin version>,
    "short_description": <Short description of what the plugin does. This text will be displayed in the plugin tile in the UI>,
    "release_notes": [
        <Array of release notes>
    ]
}
```

NOTE: older plugins have a single `plugin.lua` file with metadata stored in the first few lines of the file as comments.
If a plugin follows that convention correctly then the `README.md` and `metadata.json` files are ignored and not required.
In such cases the plugin metadata is extracted from the lua file. Here is an example of this convention:

```lua
-- Name: Test Plugin
-- Version: 1.0
-- Description: Hello, world!
--
-- This is a test.
-- End of description.

function run(input)
   return "Hello, world!"
end
```

## Instructions

Before running this tool it is necessary that the git repository to be built is
setup with the configuration so that its commits can be signed. Once the
repository is setup run:

`sdkms-plugin-registry-builder --repo-dir <Path/to/git/repository>`
