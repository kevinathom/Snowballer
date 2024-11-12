# Encode degrees of separation
## Initialize objects
cite_degrees <- list()
i <- 1
## Create vectors for get_works
while(cited_by > 0 || cites > 0){
  # Check for 0 or more degrees
  cited_by_i <- min(cited_by, 1)
  cites_i <- min(cites, 1)
  # Create the ith vector
  cite_degrees[[i]] <- c(rep('cited_by', cited_by_i),
                         rep('cites', cites_i))
  # Increment/Decrement counts
  i <- i + 1
  cited_by <- cited_by - cited_by_i
  cites <- cites - cites_i
}

# Clean up temporary objects
rm('cited_by', 'cited_by_i', 'cites', 'cites_i', 'i')
gc()
