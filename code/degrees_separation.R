# Encode degrees of separation
## Initialize objects
cite_degrees <- list()
deg <- 1
## Create vectors for get_works
while(cited_by > 0 || cites > 0){
  # Check for 0 or more degrees
  cited_by_deg <- min(cited_by, 1)
  cites_deg <- min(cites, 1)
  # Create a vector for the current degree of separation
  cite_degrees[[deg]] <- c(rep('cited_by', cited_by_deg),
                         rep('cites', cites_deg))
  # Increment/Decrement counts
  deg <- deg + 1
  cited_by <- cited_by - cited_by_deg
  cites <- cites - cites_deg
}

# Clean up temporary objects
rm('cited_by', 'cited_by_i', 'cites', 'cites_i', 'deg')
gc()
