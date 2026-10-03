# The Bayeux Tapestry, Unrolled · พรมผนังบาเยอ คลี่ทั้งผืน

https://nanobotco.github.io/bayeux-tapestry/ (Thai: /th/)

The whole Bayeux Tapestry end to end, all 58 scenes with their Latin; the stitches; Halley's Comet of 1066; everywhere it has been, from Canterbury to the British Museum; and who came to see it.

- `tools/fetch_strip.py` pulls the 2017 Caen/CNRS scene photographs (public domain) from Wikimedia Commons into `docs/img/strip/`; `tools/align_strip.py` finds where each overlaps the next so they lie end to end.
- `tools/map_data.py` cuts the Channel coast from Natural Earth 1:50m (`tools/land-50m.json`) into `docs/land.js`.
- `tools/build.py` holds all copy in English and Thai and writes both pages, llms.txt, sitemap and robots.
- `docs/app.js` draws the strip, the map, the comet orbit and the stitch toy.

Text CC BY 4.0, code MIT; pictures keep their own licences, listed on the page.
