# Set user email
my_email <- 'kevinat@wharton.upenn.edu'

# Set directories
## Data
data_dir <- '~/GitHub/Snowballer/data/'
## Code
code_dir <- '~/GitHub/Snowballer/code/'

# Set seed work entity ID(s)
seed_ids <- c('W3125944002') # hard-coded example

# Get works
source(paste0(code_dir, 'get_works.R'))

# De-duplicate results
source(paste0(code_dir, 'dedup_works.R'))
