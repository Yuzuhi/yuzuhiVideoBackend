import pandas as pd
import os
import math

# 　load datasets
base_path = r"C:\Users\86173\Desktop\movies"
tags = pd.read_csv(os.path.join(base_path, "tags.csv"))
movies = pd.read_csv(os.path.join(base_path, "movies.csv"))
ratings = pd.read_csv(os.path.join(base_path, "ratings.csv"))
links = pd.read_csv(os.path.join(base_path, "links.csv"))

movies = [int(movie) for movie in movies["movieId"].tolist()]

# initialize user rating dict
rating_dict = {}
for _, row in ratings.iterrows():
    rating_dict.setdefault(row["userId"], {})
    rating_dict[row["userId"]].update({row["movieId"]: row["rating"]})

# get all user
users = set(ratings["userId"])

# calculate user similarity
similarity_dict = {}
for u in users:
    similarity_dict.setdefault(u, {})
    for v in users:
        if u == v:
            continue
        u_set = {movies for movies in rating_dict[u].keys() if rating_dict[u][movies] > 0}
        v_set = {movies for movies in rating_dict[v].keys() if rating_dict[v][movies] > 0}
        similarity_dict[u][v] = float(len(u_set & v_set)) / math.sqrt(len(u_set) * len(v_set))

# ItemCF 物品的协同过滤

# 创建电影和用户的映射字典
movie_user_mapping = dict()

for _, row in ratings.iterrows():
    movie_user_mapping[int(row["movieId"])] = int(row["userId"])


def predict_rating(user, movie):
    rating = 0.0
    for simi_user in similarity_dict[user].keys():
        if rating_dict[simi_user].__contains__(movie):
            rating += similarity_dict[user][simi_user] * rating_dict[simi_user][movie]
    return rating


def recommend(user):
    recommend_list = []
    for movie in movies:
        if not rating_dict[user].__contains__(movie):
            rating = predict_rating(user, movie)
            recommend_list.append((movie, rating))
    recommend_list.sort(key=lambda x: x[1], reverse=True)
    return recommend_list


if __name__ == '__main__':
    res = recommend(2)[:10]
    print(res)
