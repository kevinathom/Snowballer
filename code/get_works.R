# Load dependencies
library(httr)
library(jsonlite)

# Set data directory
setwd('~\Documents\GitHub\Snowballer\data') # hard-coded example

# Get work entity ID(s)
seed_ids <- c('W3125944002') # hard-coded example

# Get works cited/citing
oal_domain <- 'https://api.openalex.org/'
fields_to_return <- c('id,doi,title,publication_year,language,type,is_retracted') # hard-coded example
## Initialize results storage
result <- as.data.frame(matrix(nrow = 0,
                               ncol = length(strsplit(fields_to_return, ",")[[1]]),
                               dimnames = list(NULL, strsplit(fields_to_return, ",")[[1]])))
## For each work entity ID
for(sid in seed_ids){
  ## Get cited_by works then cites works
  for(cit in c('cited_by', 'cites')){
    ## Get result count
    pgraw <- GET(paste0(oal_domain, 'works?per-page=1&page=1&select=id&filter=', cit, ':', sid))
    pgdat <- fromJSON(rawToChar(pgraw$content))
    cit_count <- pgdat$meta$count
    ## If there are citations
    if(cit_count > 0){
      ## Get all results
      pg <- 0
      ppg <- 200
      ## While there are results remaining
      while((pg * ppg) < cit_count){
        ## Stay at or below 200 results per page
        pg <- pg + 1
        ## Get one page of results
        pgraw <- GET(paste0(oal_domain, 'works?per-page=', ppg, '&page=', pg, '&select=', fields_to_return, '&filter=', cit, ':', sid))
        pgdat <- fromJSON(rawToChar(pgraw$content))$results
        ## Add latest page of results to the full results
        result <- rbind(result, pgdat)
      }
    }
  }
  ## Write results to file (to conserve memory)
  write.table(result, 
              file = paste0(sid, '.txt'),
              sep = '|',
              row.names = FALSE)
  ## Reset results storage
  result <- result[0, ]
}
