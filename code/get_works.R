# Load dependencies
library(httr)
library(jsonlite)

# Get work entity ID(s)
seed_ids <- c('W3125944002') # hard-coded example

# Get works cited/citing
oal_domain <- 'https://api.openalex.org/'
fields_to_return <- c('id,doi,title,publication_year,language,type,is_retracted')

##initialize object?
for(sid in seed_ids){
  for(cit in c('cited_by', 'cites')){
    # Get result count
    pgraw <- GET(paste0(oal_domain, 'works?per-page=1&page=1&select=id&filter=', cit, ':', sid))
    pgdat <- fromJSON(rawToChar(pgraw$content))
    cit_count <- pgdat$meta$count
    
    if(cit_count > 0){
      # Get all results
      pg <- 0
      ppg <- 200
      while((pg * ppg) < cit_count){
        # Stay at or below 200 results per page
        pg <- pg + 1
        pgraw <- GET(paste0(oal_domain, 'works?per-page=', ppg, '&page=', pg, '&select=', fields_to_return, '&filter=', cit, ':', sid))
        pgdat <- fromJSON(rawToChar(pgraw$content))
        ##format data to a table and store
      }
    }
  }
}
