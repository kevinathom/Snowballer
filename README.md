# Snowballer
Snowballer tool automates snowball literature searches

## Reference documentation
- [OpenAlex works filters](https://docs.openalex.org/api-entities/works/filter-works)
- [Paging](https://docs.openalex.org/how-to-use-the-api/get-lists-of-entities/paging)
- [Search works](https://docs.openalex.org/api-entities/works/search-works)

## Algorithm
1. Get work entity ID(s)
   1. Hard-code in `control.py`?
   1. Load from an external file?
   1. Search?
1. Determine the desired number of degrees of separation from seed articles
   1. Create infrastructure for looping next top-level step at different degrees of separation
1. For each entity ID
   1. Get works cited by the entity (`cited_by` filter)
      1. Short query to get the number of works (see `meta` > `count` field)
      1. Loop to get all works
   1. Get works that cite the entity (`cites` filter) -- repeat steps under parallel entry above
1. Deduplicate works
   1. Load results
   1. Merge results
   1. Keep unique entries (where entire row is not duplicated)

## Sample calls
- Seed article: `https://openalex.org/W3125944002`
- Title search: `https://api.openalex.org/works?filter=title.search:Does-the-stock-market-fully-value-intangibles`
- Cited by: `https://api.openalex.org/works?filter=cited_by:W3125944002`
- Cites: `https://api.openalex.org/works?filter=cites:W3125944002`
