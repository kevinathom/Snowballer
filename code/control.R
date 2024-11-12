# Set user email
my_email <- 'kevinat@wharton.upenn.edu'

# Set directories
## Data
data_dir <- '~/Documents/GitHub/Snowballer/data/'
## Code
code_dir <- '~/Documents/GitHub/Snowballer/code/'

# Set degrees of separation
## Cited by
cited_by <- 3
## Cites
cites <- 1

# Set seed work entity ID(s)
seed_ids <- c('W3125944002', 'W2582743722') # hard-coded example

########################

# Encode degrees of separation
source(paste0(code_dir, 'degrees_separation.R'))

# Get works
source(paste0(code_dir, 'get_works.R'))

# De-duplicate results
source(paste0(code_dir, 'dedup_works.R'))
