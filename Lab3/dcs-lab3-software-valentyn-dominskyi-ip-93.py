import sqlite3
import concurrent.futures
import matplotlib.pyplot as plt
import time

from stm import atomically

class MovieDatabaseSoftware:
    def __init__(self, db_name):
        self.db_name = db_name

        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS movies
                            (id INTEGER PRIMARY KEY,
                            title TEXT NOT NULL,
                            year INTEGER NOT NULL,
                            genre TEXT NOT NULL)''')

        self.conn.commit()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def add_movie(self, title, year, genre):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self._add_movie, title, year, genre)
            future.result()

    def _add_movie(self, title, year, genre):
        with sqlite3.connect(self.db_name) as conn:
            @atomically
            def operation():
              cursor = conn.cursor()
              cursor.execute("INSERT INTO movies (title, year, genre) VALUES (?, ?, ?)", (title, year, genre))
              conn.commit()

    def delete_movie(self, movie_id):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self._delete_movie, movie_id)
            future.result()

    def _delete_movie(self, movie_id):
        with sqlite3.connect(self.db_name) as conn:
            @atomically
            def operation():
              cursor = conn.cursor()
              cursor.execute("DELETE FROM movies WHERE id=?", (movie_id,))
              conn.commit()

    def run_measurements(self):
      self.add_movie("Cool guy", 2022, "Action")
      self.add_movie("Not Cool guy", 2023, "Not Action")
      self.delete_movie(1)

runs_num = 50

xs = []
ys = []

for i in range(runs_num):

    start = time.time()

    with MovieDatabaseSoftware('moviesSoftware.db') as db:
        db.run_measurements()
    
    end = time.time()
    xs.append(end - start)
    ys.append(i)

plt.title("Runs")
plt.xlim(0, 2)
plt.plot(xs, ys)
plt.show()