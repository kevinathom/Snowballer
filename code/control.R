### Set initial information ###

# Set user email
my_email <- 'kevinat@wharton.upenn.edu'

# Set directories
## Data
data_dir <- '~/Documents/GitHub/Snowballer/data/'
## Code
code_dir <- '~/Documents/GitHub/Snowballer/code/'

# Set degrees of separation
cited_by <- 1
cites <- 2

# Set seed work entity ID(s)
seed_ids <- c('W3125944002', 'W2762606399') # hard-coded example

# Set fields to request for works
fields_to_return <- c('id,doi,title,publication_year,language,type,is_retracted')


### Run Process ###

# Encode degrees of separation
source(paste0(code_dir, 'degrees_separation.R'))

# Get works for each degree of separation
## Initialize API domain
oal_domain <- 'https://api.openalex.org/'
## Configure work entity IDs for first degree of separation
seed_ids <- data.frame(cit = rep('seed'),
                       id = seed_ids)
## For each degree of separation
for(deg in 1:length(cite_degrees)){
  source(paste0(code_dir, 'get_works.R'))
}
## Clean up temporary objects
rm('deg', 'fields_to_return', 'my_email', 'oal_domain', 'seed_ids')

# De-duplicate results
source(paste0(code_dir, 'dedup_works.R'))
