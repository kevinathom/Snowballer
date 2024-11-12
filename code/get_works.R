# Load dependencies
library(httr)
library(jsonlite)

# Get works cited/citing
oal_domain <- 'https://api.openalex.org/'
## For each work entity ID
for(sid in seed_ids){
  # Initialize results storage (to file)
  write.table(as.data.frame(matrix(nrow = 0,
                                   ncol = length(strsplit(fields_to_return, ",")[[1]]),
                                   dimnames = list(NULL, strsplit(fields_to_return, ",")[[1]]))), 
              file = paste0(data_dir, sid, '.txt'),
              sep = '|',
              row.names = FALSE)
  # Get cited_by works then cites works
  for(cit in c('cited_by', 'cites')){
    # Get result count
    pgraw <- GET(paste0(oal_domain, 'works?mailto=', my_email, '&per-page=1&page=1&select=id&filter=', cit, ':', sid))
    pgdat <- fromJSON(rawToChar(pgraw$content))
    cit_count <- pgdat$meta$count
    # If there are citations
    if(cit_count > 0){
      # Get all results
      cursor <- '*' # Starts pagination
      ppg <- 200 # Results per page
      # While there are results remaining
      while(!is.null(cursor)){
        # Get one page of results
        Sys.sleep(.1) # Obey public API rate limit of max 10 requests per second
        pgraw <- GET(paste0(oal_domain, 'works?mailto=', my_email, '&per-page=', ppg, '&cursor=', cursor, '&select=', fields_to_return, '&filter=', cit, ':', sid))
        pgdat <- fromJSON(rawToChar(pgraw$content))
        cursor <- pgdat$meta$next_cursor
        # Append latest page of results to the results file
        write.table(pgdat$results, 
                    file = paste0(data_dir, sid, '.txt'),
                    append = TRUE,
                    sep = '|',
                    row.names = FALSE,
                    col.names = FALSE)
      }
    }
  }
}

# Clean up temporary objects
rm('cit', 'cit_count', 'cursor', 'fields_to_return', 'oal_domain', 'pgdat', 'pgraw', 'ppg', 'seed_ids', 'sid')
gc()
