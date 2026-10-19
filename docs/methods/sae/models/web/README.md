# Browse SAE model cards on the web

The interactive catalog renders model cards, searches the full checkpoint list,
and loads detailed metadata only when a card is selected. GitHub's source-file
viewer does not execute an HTML application; use the Markdown index or an HTTP
server to browse before the project page is deployed.

## Browse from a local checkout

Run this command in the repository root:

```bash
python -m http.server 8000
```

Open <http://localhost:8000/docs/methods/sae/models/web/>. Keep the server running
while searching and opening cards. Opening `index.html` as a `file://` URL is
not supported because browsers block the external JSON requests.

[Browse the Markdown checkpoint repository index](../published/README.md).

## Browse from the project page

After these files are merged into the deployment branch and the normal project
page workflow succeeds, the catalog is served at `sae-models/` under the project
page. Each repository's deployment generates links for its own repository.
A model card can be linked directly with `sae-models/#MODEL_ID`.
