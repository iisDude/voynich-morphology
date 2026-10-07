# Native candidate partition verification

The initial `run.py` checked every v11 native assigned mask and every realized bridge-cut partition across 204 views. Exact pixels, normalized shapes, group containment and union conservation must agree. Source candidates are read only.

These results are part of the v11 freeze. After that freeze, reproduce into a new result version rather than overwrite this directory. Passing verifies coordinate and pixel bookkeeping; it does not validate writing recall, drawing exclusion, pen lifts, graphemes or physical panel independence.
