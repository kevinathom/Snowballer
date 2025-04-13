# Snowballer algorithm and development

## Reference documentation
- [OpenAlex works filters](https://docs.openalex.org/api-entities/works/filter-works)
- [Paging](https://docs.openalex.org/how-to-use-the-api/get-lists-of-entities/paging)
- [Search works](https://docs.openalex.org/api-entities/works/search-works)
- [Turning a Python script into a website](https://blog.pythonanywhere.com/169/)
- [Convert Python Script to .exe File](https://www.geeksforgeeks.org/convert-python-script-to-exe-file/)

## Algorithm
1. Get work entity ID(s)
   1. Search using the [OpenAlex web interface](https://openalex.org/)
   1. Export results to CSV or save to CSV manually -- need to provide user instructions
   1. Load identifiers from CSV file
1. Set the degrees of separation from seed articles to results
	1. Input the maximum desired degrees for cites and cited_by (independently)
	1. Encode for processing
1. For each entity ID
   1. Get works (cites or cited_by)
      1. Short query to get the number of works (see `meta` > `count` field)
      1. Loop to get all works
   1. Repeat for cites and/or cited_by as specified by degrees of separation step
1. Deduplicate works
   1. Load results
   1. Merge results
   1. Keep unique entries (where entire row is not duplicated)

## Sample calls
- Seed article: `https://openalex.org/W3125944002`
- Title search: `https://api.openalex.org/works?filter=title.search:Does-the-stock-market-fully-value-intangibles`
- Cited by: `https://api.openalex.org/works?filter=cited_by:W3125944002`
- Cites: `https://api.openalex.org/works?filter=cites:W3125944002`

## Aspirations
- Make executable
- Improve error-handling
