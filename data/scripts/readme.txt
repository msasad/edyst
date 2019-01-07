The given files generate_scores.py and generate_stats.py can be used to generate random data in CSV format, which can then be loaded into the database with the provided 'loaddata' flask CLI


Data can be generated and loaded as follows:

1. Create random scores data

    python generate_scores.py > scores.csv


2. Create user data (total score, streak) based on the generated scores

    python generate_stats.py

   The above command will generate a file named users.csv


3. Load the generated data into database using flask cli (within the app environment)

    flask loaddata /path/to/users.csv /path/to/scores.csv
