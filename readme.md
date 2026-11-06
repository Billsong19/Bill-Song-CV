# Bill Song CV

Both CV variants are maintained on `master`:

- [Skills CV](skills/Bill-Song-CV.html), imported from `not-big-boy`.
- [Software engineering CV](software-eng/Bill-Song-CV.html), imported from `pipeline`.

Open either HTML file in a browser to view it or print it to PDF. Edit the HTML
and stylesheet inside the corresponding directory. Shared fonts and images live
in `assets/`.

The original branches remain available as history; future changes belong on
`master`.

## Live preview

Run from this repository (Python 3 required; no packages to install):

```sh
python3 preview.py
```

This opens both CVs in browser tabs. Saving changes to either CV, its stylesheet,
or shared assets automatically refreshes both tabs. The reload script is added
only by the preview server; the HTML files stay ready for printing or sharing.

Press Ctrl+C to stop. Use `--port 8766` to choose another port, or `--no-open`
to start without opening browser tabs.
