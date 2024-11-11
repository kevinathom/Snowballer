# List TXT files in data directory
fls <- list.files(path = data_dir,
                    pattern = '*.txt',
                    ignore.case = TRUE)

# De-duplicate results
# Set file count
fl <- 1
## First file
works <- read.delim(file = paste0(data_dir, fls[fl]),
                  sep = '|')
works <- works[!duplicated(works), ]
## Remaining files
while(fl < length(fls)){
  # Increment file count
  fl <- fl + 1
  ## Append and de-duplicate next file
  works <- rbind(works,
                 read.delim(file = paste0(data_dir, fls[fl]),
                            sep = '|'))
  works <- works[!duplicated(works), ]
}

# Save results (to file)
write.table(works, 
            file = paste0(data_dir, 'all_works.txt'),
            sep = '|',
            row.names = FALSE)

# Clean up temporary objects
rm('fl', 'fls', 'works')
gc()
