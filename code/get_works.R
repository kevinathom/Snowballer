# Load dependencies
library(httr)
library(jsonlite)

# Initialize
## Open Alex API address
oal_domain <- 'https://api.openalex.org/'
## Work entity ID storage for next degree of separation
next_ids <- data.frame(cit = c(),
                       id = c())
## Working file directory
dir.create(paste0(data_dir, 'working/'), showWarnings = FALSE)

# Get works cited/citing
## For current degree of separation's works cited_by and/or cites
for(cit in cite_degrees[[deg]]){
  ## For each work entity ID
  for(sid in seed_ids$id[seed_ids$cit == 'seed' | seed_ids$cit == cit]){
    # Initialize results storage (to file)
    write.table(as.data.frame(matrix(nrow = 0,
                                     ncol = length(strsplit(fields_to_return, ",")[[1]]),
                                     dimnames = list(NULL, strsplit(fields_to_return, ",")[[1]]))), 
                file = paste0(data_dir, 'working/', sid, '_', cit, '.txt'),
                sep = '|',
                row.names = FALSE)
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
        if(!is.null(nrow(pgdat$results))){
          write.table(pgdat$results, 
                      file = paste0(data_dir, 'working/', sid, '_', cit, '.txt'),
                      append = TRUE,
                      sep = '|',
                      row.names = FALSE,
                      col.names = FALSE)
          next_ids <- rbind(next_ids,
                            data.frame(cit = rep(cit, nrow(pgdat$results)),
                                       id = c(pgdat$results$id)))
        }
      }
    }
  }
}

# Prepare for next iteration
seed_ids <- next_ids
## Clean IDs (of full path)

# Clean up temporary objects
rm('cit', 'cit_count', 'cursor', 'fields_to_return', 'next_ids', 'oal_domain', 'pgdat', 'pgraw', 'ppg', 'sid')
gc()
