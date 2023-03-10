import pprint as p
import requests

# Gather top 60 Manga from Anilist website
def fetch_media_list():
    query = '''
    query ($id: Int, $page: Int, $perPage: Int, $search: String){
  Page(page: $page, perPage: $perPage) {
    pageInfo{
      total
      perPage
      currentPage
      lastPage
      hasNextPage
    }
    media(id: $id, sort: SCORE_DESC, search: $search, type: MANGA, format: MANGA){
      id
      siteUrl
      title{
        romaji
        native
        english
      }
      popularity
      genres
      averageScore
      rankings {
        rank
        format
        type
        allTime
      }
    }
  }
}
    '''
    #Changed perpage to 60 from 20.
    variables = {"page": 1, "perPage": 50}

    url = 'https://graphql.anilist.co'

    response = requests.post(url, json={'query': query, 'variables': variables})

    data = response.json()

    return data

data = fetch_media_list()
print(data)

def cleandata_foruse(data_json):
    mangalist = data_json["data"]["Page"]["media"]
    return mangalist

# Gather the Mangas that have changed rank
def get_media_changes_list(past_list, current_list):
    media_changes_list = []
    for index, p_media in enumerate(past_list):
        '''get id and check both lists, note any changes'''
        media_id = p_media["id"]
        if current_list[index]["id"] == media_id:
            continue
        else:
            current_location_of_media = next((item for item in current_list if item["id"] == media_id), "Not Found")
            if current_location_of_media == "Not Found":
                continue
            else:
                current_rank = current_location_of_media["rankings"][0]["rank"]
                past_rank = p_media["rankings"][0]["rank"]
                ranks_moved_up = past_rank - current_rank
                current_media_index = current_list.index(current_location_of_media)
                media_below_in_rank = current_list[current_media_index + 1]
                if ranks_moved_up > 0:
                    media_changes_list.append([p_media, current_rank, ranks_moved_up, media_below_in_rank])

    return media_changes_list


# Prepares the tweets for Mangas that have moved up in rank
def prepare_tweet_text_list(media_changes):
    tweets_list = []
    for media_changed in media_changes:
        if media_changed[0]["title"]["english"] is None:
            media_title = media_changed[0]["title"]["romaji"]
        else:
            media_title = media_changed[0]["title"]["english"]
        if media_changed[3]["title"]["english"] is None:
            media_title_below = media_changed[3]["title"]["romaji"]
        else:
            media_title_below = media_changed[3]["title"]["english"]
        tweet = f"{media_title} moved up {media_changed[2]} places and is now rank {media_changed[1]} on the Anilist" \
                f"Top Rated Manga Leaderboard.\nIt is now above {media_title_below}!\n\n" \
                f"{media_changed[0]['siteUrl']}"
        tweets_list.append(tweet)
    return tweets_list




