import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk

class PopularityRecommender:
    def __init__(self):
        self.t_data = None                                  
        self.user_names = None                             
        self.song_names = None                               
        self.pop_recommendations = None                

    def create_p(self, t_data, user_names, song_names):  
        self.t_data = t_data  
        self.user_names = user_names  
        self.song_names = song_names  

        t_data_grouped = t_data.groupby([self.user_names, self.song_names]).agg(play_count=('play_count', 'sum')).reset_index()  
        t_data_sort = t_data_grouped.sort_values(['play_count', self.song_names], ascending=[0, 1])  
        t_data_sort['Song_preference'] = t_data_sort.groupby(self.user_names)['play_count'].rank(ascending=0, method='first').astype(int)

        self.pop_recommendations = t_data_sort

    def recommend_p(self, user_name):      
        user_recommendations = self.pop_recommendations[self.pop_recommendations[self.user_names] == user_name].copy()
        user_recommendations['user_name'] = user_name  
        cols = user_recommendations.columns.tolist()  
        cols = cols[-1:] + cols[:-1]  
        user_recommendations = user_recommendations[cols]  
          
        return user_recommendations

# Sample data with 5 songs per user
data = pd.DataFrame({
    'user_name': ['Alice', 'Alice', 'Alice', 'Alice', 'Alice',
                  'Bob', 'Bob', 'Bob', 'Bob', 'Bob',
                  'Charlie', 'Charlie', 'Charlie', 'Charlie', 'Charlie',
                  'David', 'David', 'David', 'David', 'David',
                  'Eve', 'Eve', 'Eve', 'Eve', 'Eve'],
    'song_name': ['Song1', 'Song2', 'Song3', 'Song4', 'Song5',
                  'Song1', 'Song2', 'Song3', 'Song4', 'Song5',
                  'Song1', 'Song2', 'Song3', 'Song4', 'Song5',
                  'Song1', 'Song2', 'Song3', 'Song4', 'Song5',
                  'Song1', 'Song2', 'Song3', 'Song4', 'Song5'],
    'play_count': [5, 3, 2, 4, 1,
                   6, 2, 4, 1, 5,
                   7, 4, 1, 5, 3,
                   1, 5, 8, 2, 7,
                   8, 2, 3, 4, 1]
})

# Initialize the recommender system
pr = PopularityRecommender()
pr.create_p(data, 'user_name', 'song_name')

# GUI
class RecommenderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Music recommandation system")

        # Configure ttk style for a light blue theme
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Choose a light-colored theme, like 'clam'
        self.style.configure('.', background='#e0f7fa')  # Set light blue background color for all widgets
        self.style.configure('Green.TButton', background='#4caf50', foreground='white')  # Light green button style

        self.label = ttk.Label(root, text="Enter User Name:")
        self.label.pack(pady=10)

        self.user_entry = ttk.Entry(root, width=30)
        self.user_entry.pack(pady=10)
        self.user_entry.config(style='EntryStyle.TEntry')

        self.button = ttk.Button(root, text="Get Recommendations", command=self.show_recommendations, style='Green.TButton')
        self.button.pack(pady=10)

        self.username_label = ttk.Label(root, text="")
        self.username_label.pack(pady=10)

        self.tree = ttk.Treeview(root, columns=('song_name', 'play_count', 'Song_preference'), show='headings')
        self.tree.heading('song_name', text='Song Name')
        self.tree.heading('play_count', text='Play Count')
        self.tree.heading('Song_preference', text='Song Preference')
        self.tree.pack(pady=20)
        self.tree.config(style='TreeviewStyle.Treeview')

    def show_recommendations(self):
        user_name = self.user_entry.get()
        self.username_label.config(text=f"Recommendations for: {user_name}")
        recommendations = pr.recommend_p(user_name)

        for row in self.tree.get_children():
            self.tree.delete(row)

        for index, row in recommendations.iterrows():
            self.tree.insert('', 'end', values=row[['song_name', 'play_count', 'Song_preference']].tolist())

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('600x400')  # Set initial window size
    gui = RecommenderGUI(root)
    root.mainloop()