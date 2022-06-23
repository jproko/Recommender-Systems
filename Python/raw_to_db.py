import csv
import pandas as pd

# Articles of interest:
# [1]. https://realpython.com/python-csv/
# [2]. https://pythonspeed.com/articles/pandas-read-csv-fast/
# -------------------------------
# Title: Functions
def movies_to_dbMovies():
    # Title: Functionality Description
    #   This function is responsible for extracting
    #   the necessary information, from movieLens
    #   raw movies.csv file => db_movies.csv file
    # -------------------------------
    # Title: movies.csv entry format
    #   movieId,title,genres
    #   1,Toy Story (1995),Adventure|Animation|Children|Comedy|Fantasy
    # -------------------------------
    # Title: db_movies.csv entry format
    #   m_id, title, release_date
    #   1, Toy Story, 1995
    # -------------------------------
    # Title: Open read/write files
    with open('movies.csv', mode='r') as movies_csv_file, open('db_movies.csv', mode='w') as db_movies_csv_file:
        # associate readers and writers with our read and write files
        file_reader = csv.reader(movies_csv_file, delimiter=',')
        file_writer = csv.writer(db_movies_csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        # counter initialization
        row_counter = -1
        for row in file_reader:
            # keep track of rows
            row_counter = row_counter+1
            # first row is don't care beacause its title
            if(row_counter==0):
                continue
            # -------------------------------
            # Title: Perform row_operations
            #   Extract the [title, release year] list from given title
            title_data_list = extract_movie_date(row[1])
            #   Write the desired value to our csv file
            file_writer.writerow([row[0], title_data_list[0], title_data_list[1]])
# -------------------------------
def extract_movie_date(movie_title):
    # Title: Functionality Description
    #   This function is responsible for extracting
    #   release year of a movie from a given movie title, as
    #   well as discard the unnecessary ("") from titles
    # -------------------------------
    # Title: Example 1
    #   movie_title: "American President, The (1995)"
    #   return: [American President, The, 1995]
    # -------------------------------
    # Title: Example 2
    #   movie_title: Twelve Monkeys (a.k.a. 12 Monkeys) (1995)
    #   return: [Twelve Monkeys (a.k.a. 12 Monkeys), 1995]
    # -------------------------------
    # Title: Return list
    #   we associate a list of two strings
    #   [title, year]
    data_list = ["",""]
    # -------------------------------
    # Title: Extract release date
    #   We are certain that our year will be placed at the end of
    #   any title as: (YYYY)
    #   for our date therefore, we are interested in the last 6 digits
    #   of any given title.
    year = movie_title[-6:-1]+movie_title[-1]
    #   we store the necessary data to our return list
    data_list[1] = year[1:5]
    # -------------------------------
    # Title: Extract title
    #   Given that we no longer have use of the release year, as well as
    #   know exactly the 'dont-care' value of the given title, we can very
    #   well erase it from the title.
    data_list[0] = movie_title.replace(year,"")
    # -------------------------------
    # Title: Delete last empty space remaining
    data_list[0] = data_list[0][:-1]
    # -------------------------------
    return data_list
# -------------------------------
def movies_to_dbUsers():
    # Title: Functionality Description
    #   This function is responsible for extracting
    #   the necessary information, from movieLens
    #   raw ratings.csv file => db_users.csv file
    # -------------------------------
    # Title: ratings.csv entry format
    #   userId,movieId,rating,timestamp
    #   1,295,5.0,xxxxxxxxxx
    # -------------------------------
    # Title: db_users.csv entry format
    #   u_id
    #   1
    # -------------------------------
    # Title: Pandas CSV access
    df = pd.read_csv("ratings.csv")
    # -------------------------------
    # Title: Extract unique user id from data frame
    #   a = df.drop_duplicates(subset=['userId']) : drop dublicates based uppon column userId
    #       rows of a:
    #                   userId  movieId  rating   timestamp
    #       0              1      296     5.0  1147880044
    #       1              1      306     3.5  1147868817
    #       2              1      307     5.0  1147868828
    #       3              1      665     5.0  1147878820
    #   b = a["userId"] : Series keeping index and userId column
    #   c = pd.DataFrame({"u_id":b}) : Turn Series to DataFrame
    df_refined = pd.DataFrame({"u_id":df.drop_duplicates(subset=['userId'])["userId"]})
    #   Extract Dataframe to "db_users.csv" without storing index
    df_refined.to_csv("db_users.csv", index=False)
# -------------------------------
def movies_to_hasGenres():
    # Title: Functionality Description
    #   This function is responsible for extracting
    #   the necessary information, from movieLens
    #   raw movies.csv file => db_hasGenres.csv file
    # -------------------------------
    # Title: movies.csv entry format
    #   movieId,title,genres
    #   1,Toy Story (1995),Adventure|Animation|Children|Comedy|Fantasy
    # -------------------------------
    # Title: db_hasGenres.csv entry format
    #   m_id, g_id
    #   1, 3
    #   1, 4
    #   1, 5
    #   1, 6
    #   1, 10
    # -------------------------------
    # Title: Open read/write files
    with open('movies.csv', mode='r') as movies_csv_file, open('db_hasGenres.csv', mode='w') as db_hasGenres_csv_file:
        # associate readers and writers with our read and write files
        file_reader = csv.reader(movies_csv_file, delimiter=',')
        file_writer = csv.writer(db_hasGenres_csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        # counter initialization
        row_counter = -1
        switcher ={"(no genres listed)":1,"Action":2,"Adventure":3,"Animation":4,"Children":5,"Comedy":6,"Crime":7,"Documentary":8,"Drama":9,"Fantasy":10,"Film-Noir":11,"Horror":12,"Musical":13,"Mystery":14,"Romance":15,"Sci-Fi":16,"Thriller":17,"War":18,"Western":19}
        for row in file_reader:
            # keep track of rows
            row_counter = row_counter+1
            # first row is don't care beacause its title
            if(row_counter==0):
                file_writer.writerow(['m_id', 'g_id'])
                continue
            # -------------------------------
            # Title: Perform row_operations
            #   Extract all genres of a movie
            genres = row[2].split('|')
            for gen in genres:
                if(gen==""):
                    continue
                try:
                    file_writer.writerow([row[0], switcher[gen]])
                except:
                    print(row)
# -------------------------------
def movies_to_imdb_tmdb():
    # Title: Functionality Description
    #   This function is responsible for extracting
    #   the necessary information, from movieLens
    #   raw links.csv file => db_imdb_list.csv file
    #   raw links.csv file => db_tmdb_list.csv file
    #   raw links.csv file => db_m_to_imdb_list.csv file
    #   raw links.csv file => db_m_to_tmdb_list.csv file
    # -------------------------------
    # Title: links.csv file entry format
    #   movieId,imdbId,tmdbId
    #   1,0114709,862
    # -------------------------------
    # Title: db_imdb_list.csv entry format
    #   imdb_id
    #   0114709
    # -------------------------------
    # Title: db_tmdb_list.csv entry format
    #   tmdb_id
    #   862
    # -------------------------------
    # Title: db_m_to_imdb_list.csv entry format
    #   m_id, imdb_id
    #   1, 0114709
    # -------------------------------
    # Title: db_m_to_tmdb_list.csv entry format
    #    m_id, tmdb_id
    #   1, 862
    # -------------------------------

    # Title: Open read/write files
    with open('links.csv', mode='r') as links_csv_file, open('db_imdb_list.csv', mode='w') as db_imdb_list_csv_file, open('db_tmdb_list.csv', mode='w') as db_tmdb_list_csv_file, open('db_m_to_imdb_list.csv', mode='w') as db_m_to_imdb_list_csv_file, open('db_m_to_tmdb_list.csv', mode='w') as db_m_to_tmdb_list_csv_file:
        # associate readers and writers with our read and write files
        file_reader = csv.reader(links_csv_file, delimiter=',')
        file_writer_1 = csv.writer(db_imdb_list_csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        file_writer_2 = csv.writer(db_tmdb_list_csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        file_writer_3 = csv.writer(db_m_to_imdb_list_csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        file_writer_4 = csv.writer(db_m_to_tmdb_list_csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        # counter initialization
        row_counter = -1
        tmdb_list=[]
        for row in file_reader:
            # keep track of rows
            row_counter = row_counter+1
            # first row is don't care beacause its title
            if(row_counter==0):
                file_writer_1.writerow(['imdb_id', 'score', 'rated_by'])
                file_writer_2.writerow(['tmdb_id', 'score', 'rated_by'])
                file_writer_3.writerow(['m_id','imdb_id'])
                file_writer_4.writerow(['m_id','tmdb_id'])
                continue
            # -------------------------------
            # Title: Perform row_operations
            file_writer_1.writerow([row[1],'',''])
            file_writer_3.writerow([row[0], row[1]])
            if(row[2]!=""):
                if(row[2] not in tmdb_list):
                    file_writer_2.writerow([row[2],'',''])
                    file_writer_4.writerow([row[0], row[2]])
                    tmdb_list.append(row[2])

# -------------------------------
# Title: Main Script Functionality
movies_to_imdb_tmdb()
