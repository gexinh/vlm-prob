# Search SAE model cards

Search by backbone, SAE method, activation hook or dictionary width. Open a card
to view its source configuration, input conventions and checkpoint downloads.

## On the project page

Open **SAE checkpoints** in the project page navigation. Select **Open model
card** beside a search result to view its details. The URL fragment identifies
the selected dictionary, so you can copy the URL to share that card directly.

## From a local checkout

Run this command in the repository root:

```bash
python -m http.server 8000
```

Open <http://localhost:8000/docs/methods/sae/models/web/>. Keep the server running
while searching and opening cards; the catalog loads its data over HTTP.

## On GitHub

Use the [model directory](../published/README.md) to browse checkpoints grouped
by backbone and open their Markdown cards.
