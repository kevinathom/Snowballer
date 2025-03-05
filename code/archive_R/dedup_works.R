# Load dependencies
library(readr)

# List TXT files in data directory
fls <- list.files(path = paste0(data_dir, 'working/'),
                    pattern = '*.txt',
                    ignore.case = TRUE)

# De-duplicate results
## Set file count
fl <- 1
## Load and de-duplicate first file
works <- read_delim(file = paste0(data_dir, 'working/', fls[fl]),
                  delim = '|',
                  show_col_types = FALSE)
works <- works[!duplicated(works), ]
## Handle remaining files
while(fl < length(fls)){
  # Increment file count
  fl <- fl + 1
  # Append and de-duplicate next file
  works <- rbind(works,
                 read_delim(file = paste0(data_dir, 'working/', fls[fl]),
                            delim = '|',
                            show_col_types = FALSE))
  works <- works[!duplicated(works), ]
}

# Save results (to file)
write.table(works, 
            file = paste0(data_dir, 'all_works.txt'),
            sep = '|',
            row.names = FALSE)

# Clean up temporary objects
unlink(paste0(data_dir, 'working/'), recursive = TRUE)
rm('fl', 'fls', 'works')
gc()
