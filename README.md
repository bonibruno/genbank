# Get GEO datasets from GenBank

Python script to automate getting GEO (Gene Expression Omnibus) datasets.

The GEO datasets are robust collections of experimental data, often including gene expression, comparative genomics, and other complex data types. 
They are generally large and complicated, often requiring specific metadata tagging and classification, which makes them a reasonable choice for stress-testing advanced storage solutions and analytics engines.

Approach:

I use ftputil and os for FTP connection and file manipulation, respectively.

FTP Connection: 
  The script establishes an FTP connection to the target host defined in the HOST variable using the ftputil library.

Directory Iteration:
  The script uses nested loops to iterate through each major folder (e.g., GDS1nnn, GDS2nnn).
  For each major folder, it iterates through the individual dataset folders (e.g., GDS1001, GDS1002, etc.)

Error Handling and Retries:
  When the script encounters a dataset folder, it tries to download the relevant .gz files.
  If it fails to change to a directory, the script will retry up to 3 times before skipping to the next dataset.

File Download:
  The .gz files are downloaded only if they are not already present in the destination folder, saving bandwidth and time.

Logging:
  Errors are logged to getdata.log for analysis and debugging.
