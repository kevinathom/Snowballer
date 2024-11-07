# Load dependencies
library(httr)
library(jsonlite)

# Set data directory
setwd('~/Documents/GitHub/Snowballer/data') # hard-coded example

# Get work entity ID(s)
seed_ids <- c('W3125944002') # hard-coded example
my_email <- 'kevinat@wharton.upenn.edu' # hard-coded example

# Get works cited/citing
oal_domain <- 'https://api.openalex.org/'
fields_to_return <- c('id,doi,title,publication_year,language,type,is_retracted') # hard-coded example
## For each work entity ID
for(sid in seed_ids){
  # Initialize results storage (to file)
  write.table(as.data.frame(matrix(nrow = 0,
                                   ncol = length(strsplit(fields_to_return, ",")[[1]]),
                                   dimnames = list(NULL, strsplit(fields_to_return, ",")[[1]]))), 
              file = paste0(sid, '.txt'),
              sep = '|',
              row.names = FALSE)
  # Get cited_by works then cites works
  for(cit in c('cited_by', 'cites')){
    # Get result count
    pgraw <- GET(paste0(oal_domain, 'works?mailto=', my_email, '&per-page=1&page=1&select=id&filter=', cit, ':', sid))
    Sys.sleep(.1) # Obey public API rate limit of max 10 requests per second
    pgdat <- fromJSON(rawToChar(pgraw$content))
    cit_count <- pgdat$meta$count
    # If there are citations
    if(cit_count > 0){
      # Get all results
      pg <- 0
      ppg <- 200
      # While there are results remaining
      while((pg * ppg) < cit_count){
        # Stay at or below 200 results per page
        pg <- pg + 1
        # Get one page of results
        pgraw <- GET(paste0(oal_domain, 'works?mailto=', my_email, '&per-page=', ppg, '&page=', pg, '&select=', fields_to_return, '&filter=', cit, ':', sid))
        Sys.sleep(.1) # Obey public API rate limit of max 10 requests per second
        pgdat <- fromJSON(rawToChar(pgraw$content))$results
        # Append latest page of results to the results file
        write.table(pgdat, 
                    file = paste0(sid, '.txt'),
                    append = TRUE,
                    sep = '|',
                    row.names = FALSE,
                    col.names = FALSE)
      }
    }
  }
}
## Cursor paging alternative (for larger results)
#see https://docs.openalex.org/how-to-use-the-api/get-lists-of-entities/paging
### For testing
pulls <- c()
for(sid in seed_ids){
  # Initialize results storage (to file)
  write.table(as.data.frame(matrix(nrow = 0,
                                   ncol = length(strsplit(fields_to_return, ",")[[1]]),
                                   dimnames = list(NULL, strsplit(fields_to_return, ",")[[1]]))), 
              file = paste0(sid, '.txt'),
              sep = '|',
              row.names = FALSE)
  # Get cited_by works then cites works
  for(cit in c('cited_by', 'cites')){
    # Get result count
    pgraw <- GET(paste0(oal_domain, 'works?mailto=', my_email, '&per-page=1&page=1&select=id&filter=', cit, ':', sid))
    Sys.sleep(.1) # Obey public API rate limit of max 10 requests per second
    pgdat <- fromJSON(rawToChar(pgraw$content))
    cit_count <- pgdat$meta$count
    # If there are citations
    if(cit_count > 0){
      # Get all results
      pg <- 0
      ppg <- 200
      # While there are results remaining
      while((pg * ppg) < cit_count){
        # Stay at or below 200 results per page
        pg <- pg + 1
        # Get one page of results
        pgraw <- GET(paste0(oal_domain, 'works?mailto=', my_email, '&per-page=', ppg, '&page=', pg, '&select=', fields_to_return, '&filter=', cit, ':', sid))
        Sys.sleep(.1) # Obey public API rate limit of max 10 requests per second
        pgdat <- fromJSON(rawToChar(pgraw$content))$results
        ### For testing
        pulls <- c(pulls, paste('type:', cit, 'pg:', pg, 'results', nrow(pgdat)))
        # Append latest page of results to the results file
        write.table(pgdat, 
                    file = paste0(sid, '.txt'),
                    append = TRUE,
                    sep = '|',
                    row.names = FALSE,
                    col.names = FALSE)
      }
    }
  }
}

# Clean up temporary objects
rm('cit', 'cit_count', 'fields_to_return', 'my_email', 'oal_domain', 'pg', 'pgdat', 'pgraw', 'ppg', 'seed_ids', 'sid')
