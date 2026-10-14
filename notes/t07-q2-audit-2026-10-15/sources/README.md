# sources/ — local cache, not in Git

`scan1015/` holds the raw arXiv/OpenAlex query scripts and returned records from the 14–15/10 broad scan (search metadata, not paper text). Per AUDIT.md the cache stays local; `CACHE-MANIFEST.json` and `VERIFICATION.json` in the parent folder record file names, record counts, unique arXiv IDs and SHA256 hashes so the copy can be checked.

Counts are returned search records, not papers read. The "about 45 new sources" figure in the 15/10 direction map is an analyst selection that was not reconstructed (see REPORT.md §1).
