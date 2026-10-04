# Schemas

Machine-readable companions to the guidelines (JSON Schema, draft 2020-12). All schemas are deliberately permissive: known keys are type-checked, unknown keys are allowed and should be preserved by tools that rewrite the data.

| Schema | Validates | Defined in |
|---|---|---|
| `page-frontmatter.schema.json` | The YAML frontmatter of a page, once parsed to JSON | [09 · Metadata and Frontmatter](../guidelines/09-Metadata_and_Frontmatter.md), [Appendix C](../guidelines/appendices/C-Portable_Page_Metadata_Reference.md) |
| `bundle-manifest.schema.json` | `wiki-bundle.yaml` | [10 · Interchange and Portability](../guidelines/10-Interchange_and_Portability.md) (XFER-1, XFER-2) |
| `history-record.schema.json` | Each line of `history/<page-id>.jsonl` | XFER-7 |
| `discussion-record.schema.json` | Each line of `discussions/<page-id>.jsonl` | XFER-10 |
| `attachment-meta.schema.json` | `<file>.meta.yaml` sidecars or `attachments.yaml` entries | XFER-4 |
| `site-description.schema.json` | The site description document | [11 · APIs and Discovery](../guidelines/11-APIs_and_Discovery.md) (API-1) |
| `self-assessment.schema.json` | `wiki-commons.yaml` | [16 · Conformance Profiles](../guidelines/16-Conformance_Profiles_and_Self_Assessment.md) |

## Validating

Any draft 2020-12 validator works. With Python:

```sh
pip install jsonschema pyyaml
python3 - <<'PY'
import json, yaml, jsonschema, pathlib
schema = json.load(open("schemas/bundle-manifest.schema.json"))
data = yaml.safe_load(open("examples/portable-wiki-bundle/wiki-bundle.yaml"))
jsonschema.Draft202012Validator(schema).validate(data)
print("manifest valid")
PY
```

With Node:

```sh
npm install ajv ajv-formats js-yaml
node -e '
const Ajv = require("ajv/dist/2020"); const addFormats = require("ajv-formats");
const yaml = require("js-yaml"); const fs = require("fs");
const ajv = addFormats(new Ajv({strict: false}));
const validate = ajv.compile(JSON.parse(fs.readFileSync("schemas/bundle-manifest.schema.json")));
const data = yaml.load(fs.readFileSync("examples/portable-wiki-bundle/wiki-bundle.yaml", "utf8"));
console.log(validate(data) ? "manifest valid" : validate.errors);'
```

Frontmatter is the YAML between the opening and closing `---` lines of a page file; extract it, parse it, and validate the result. Format assertions (`date-time`, `uri`) are advisory in JSON Schema unless the validator is configured to enforce them.

The `discussion-record` schema references `history-record.schema.json#/$defs/author` by relative URL; validators that resolve `$ref` against the `$id` will fetch it from this repository, and those that do not should be given both schemas.
