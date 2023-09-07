#Importing the required libraries

from pprint import pprint
from googleapiclient.discovery import build
import pandas as pd
import streamlit as st
from pymongo import MongoClient
import mysql.connector
from streamlit_option_menu import option_menu
import json
from googleapiclient.errors import HttpError


#Connecting mongodb
mongo_client = MongoClient("mongodb+srv://karthikeyanapril5:1578@cluster0.kngfgwp.mongodb.net/?retryWrites=true&w=majority")
db = mongo_client['Youtube']

# Connecting mysql
sql = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="Youtube"
)
mysql_cursor = sql.cursor()

#connecting to youtube API
api_Key = 'AIzaSyB-ZKdr-X0TeyuLdvURBEcmeEPrvlM1SRQ'
api_service_name = 'youtube'
api_version = 'v3'
youtube = build(api_service_name, api_version, developerKey = api_Key)

##CREATING FUNCTIONS TO GET YOUTUBE DETAILS###

#Getting the channel details

def get_channel_details(channel_id):
  channel_details = []
  request = youtube.channels().list(
  part="contentDetails,snippet,statistics",
  id=channel_id)
  response = request.execute()


  for item in response['items']:

    data = {'channel_id': item['id'],
            'channelName': item['snippet']['title'],
            'subscriber_count': item['statistics']['subscriberCount'],
            'Channel_views': item['statistics']['viewCount'],
            'total_videos':item['statistics']['videoCount'],
            'description': item['snippet']['description'],
            'playlist_Id': item['contentDetails']['relatedPlaylists']['uploads']}
    channel_details.append(data)
  return channel_details

channeldetails = get_channel_details('UCwr-evhuzGZgDFrq_1pLt_A')

# Getting video IDs
def get_video_ids(channel_id):
    IDs = []
    request = youtube.channels().list(
        part="snippet,contentDetails",
        id=channel_id
    )
    response = request.execute()
    playlistid = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    next_page_token = None
    while True:

        request = youtube.playlistItems().list(
            part="contentDetails",
            maxResults=50,
            playlistId=playlistid,
            pageToken = next_page_token
            )
        response = request.execute()

        for item in response['items']:
            IDs.append(item['contentDetails']['videoId'])
        next_page_token = response.get('nextPageToken')
        if next_page_token is None:
            break
    return IDs
video_id_s = get_video_ids('UCwr-evhuzGZgDFrq_1pLt_A')


#Getting video details
def getvideo_details(IDs):
    video_details = []

    for i in range(len(IDs)):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id = IDs[i]
        )
                
        response = request.execute()    

        for item in response['items']:

            data = {'channel_id': item['snippet']['channelId'],
                    'channel_name': item['snippet']['channelTitle'],
                    'video_id': item['id'],
                    'Video_name': item['snippet']['title'],
                    'video_description':item['snippet']['description'],
                    'view_count': item['statistics']['viewCount'],
                    'comment_count':item['statistics'].get('commentCount'),
                    'likecount': item['statistics']['likeCount'],
                    'thumbnail': item['snippet']['thumbnails']}

            video_details.append(data)

    return video_details

#Getting comment details
def get_video_comments(video_id):
    comments = []
    nextPageToken = None
    try:
        while True:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                pageToken=nextPageToken,
                maxResults=100
            )
            response = request.execute()

            for item in response["items"]:
                data = {'video_id': video_id,
                        'comment_id': item['snippet']['topLevelComment']['snippet']['authorChannelId']['value'],
                        'author': item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                        'text': item['snippet']['topLevelComment']['snippet']['textDisplay']}

                comments.append(data)

            nextPageToken = response.get("nextPageToken")
            if not nextPageToken:
                break
    except HttpError as e:
        if e.resp.status == 404:
            print(f"Video with ID '{video_id}' not found.")
        else:
            print(f"An error occurred: {e}")

    return comments
#Getting all the comments from the videos ids in that Youtube channel
def all_comments(IDs):
    comments = list()
    for id in IDs:
        comments += get_video_comments(id)
    return comments

    ################################# adding some data's in Mongodb ##############################################
# mycollection1 = db['Channels']
# for data_dict in channeldetails:
#     mycollection1.insert_one(data_dict)

# mycollection2 = db['Videos']
# for data_dict in videodetails:
#     mycollection2.insert_one(data_dict)

# mycollection3 = db['Comments']
# for data_dict in commentdetails:
#     mycollection3.insert_one(data_dict)

#Getting all the comments from the videos ids in that Youtube channel


#Getting all the channel names stored in the Mongodb
def all_channel_names():
    channelname = list()
    for i in db.Channels.find():
        channelname.append(i['channelName'])
    return channelname

#getting all the channel id
def all_channel_id():
    channelids = list()
    for i in db.Channels.find():
        channelids.append(i['channel_id'])
    return channelids

#### SQL #####

def insert_channels_tables_sql():
    query = "INSERT INTO channels (channel_id, channelName, subscriber_count,Channel_views, total_videos, description, playlist_Id) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    for doc in db.Channels.find({'channelName': ch_input}, {'_id': 0}):
        values = (doc['channel_id'],doc['channelName'],doc['subscriber_count'],doc['Channel_views'],doc['total_videos'],doc['description'],doc['playlist_Id'])
        mysql_cursor.execute(query,values)
        sql.commit()

def insert_videos_table_sql():
    query = "INSERT INTO videos (channel_id, channel_name, video_id,Video_name, video_description, view_count, comment_count, likecount,thumbnail) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    for doc in db.Videos.find({'channel_name': ch_input}, {'_id': 0}):
        comment_count = doc.get('comment_count', 0)
        thumbnail_json = json.dumps(doc['thumbnail'])
        values = (doc['channel_id'],doc['channel_name'],doc['video_id'],doc['Video_name'],doc['video_description'],doc['view_count'],comment_count, doc['likecount'],thumbnail_json)
        mysql_cursor.execute(query, values)
        sql.commit()

def insert_to_comments_table_sql():
    query = "INSERT INTO comments(video_id,comment_id,author,text) VALUES (%s,%s,%s,%s)"
    for vid in db.Videos.find({'channel_name': ch_input}, {'_id': 0}):
        for i in db.Comments.find({'video_id':vid['video_id']},{'_id':0}):
            values = (i['video_id'], i['comment_id'], i['author'],i['text'] )
            mysql_cursor.execute(query, values)
            sql.commit()

############################################STREAMLIT########################################################

st.set_page_config(page_title= "Youtube Data harvesting and warehousing | By: Karthikeyan.B",
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """Youtube Channel details exploration: A User-Friendly Tool Using Streamlit project Done by: Karthikeyan."""})

st.title(':red[YouTube Data Harvesting and Warehousing] ')
Selectbox_main = st.selectbox('NAVIGATE :mag_right:',('Main', 'Find', 'About'))

if Selectbox_main == 'Main':
    st.header(':red[Abstract]')
    st.subheader('YouTube Data Harvesting and Warehousing is a project that aims to allow users to access and analyze data from multiple YouTube channels. The project utilizes SQL, MongoDB, and Streamlit to create a user-friendly application that allows users to retrieve, store, and query YouTube channel and video data.')
    st.subheader('YouTube is a free video sharing website that makes it easy to watch online videos. You can even create and upload your own videos to share with others. Originally created in 2005, YouTube is now one of the most popular sites on the Web, with visitors watching around 6 billion hours of video every month.')
    st.image('mainpic.jpg')
    st.write('### :red[More about youtube] Shortly after the site opened on a limited (“beta”) basis in May 2005, it was attracting some 30,000 visitors per day. By the time YouTube was officially launched on December 15, 2005, it was serving more than two million video views each day. By January 2006 that number had increased to more than 25 million views. The number of videos available at the site surpassed 25 million in March 2006, with more than 20,000 new videos uploaded on a daily basis. By the summer of 2006, YouTube was serving more than 100 million videos per day, and the number of videos being uploaded to the site showed no sign of slowing down.')

if Selectbox_main == 'Find':
    st.title('Get your Details here :point_down:')
    tab2,tab3 = st.tabs(['Find and save details','Insights'])
    with tab2:
        id_input = st.text_input('Channel_id')
        st.write(':red[How to get your Channel ID ?]  Go to Main page of your selected Youtube channel  :arrow_forward:  Select About section  :arrow_forward:  Select Share icon, Copy Channel ID')
        get_button = st.button('Find')

        if id_input and get_button:
            if id_input not in all_channel_id():
                with st.spinner(":green[We are almost done fetching your favorite channel details]"):
                    youtube_channel = get_channel_details(id_input)
                    st.success(f"Details of {youtube_channel[0]['channelName']} is below, check that out")
                    st.table(youtube_channel)
            else:
                st.info('Details are already available kindly check the available channel list')


        if st.button("Send to mongodb"):
            with st.spinner("Uploading Channel Details"):
                youtube_channel = get_channel_details(id_input)
                youtube_videoid = get_video_ids(id_input)
                youtube_videodetails = getvideo_details(youtube_videoid)
                youtube_commentdetails = all_comments(youtube_videoid)
                st.toast('All the details are trasnsfered successfully to mongodb')

                db.Channels.insert_many(youtube_channel)
                db.Videos.insert_many(youtube_videodetails)
                try:
                    db.Comments.insert_many(youtube_commentdetails)
                except:
                    st.warning('No comments for this channel')
                st.success(f"Uploaded the details of {youtube_channel[0]['channelName']} Succesfully thanks for being patient :handshake:")

        channels = all_channel_names()
        channels.insert(0, 'Choose a channel')
        ch_input = st.selectbox("Available channels are below", options=channels)
        transform = st.button('Store in SQL')

        if ch_input and transform:
            try:
                with st.spinner("Transforming MongoDB data to Sql"):
                    insert_channels_tables_sql()
                    insert_videos_table_sql()
                    insert_to_comments_table_sql()
                    st.success('Transformed thanks for waiting patienlty')
            except:
                st.error("Error ! Kindly Check the SQL table for the same details")

    with tab3:
        FAQs = ['Frequently asked questions',
                    '1. What are the names of all the videos and their corresponding channels?',
                    '2. Which channels have the most number of videos, and how many videos do they have?',
                    '3. What are the top 10 most viewed videos and their respective channels?',
                    '4. How many comments were made on each video, and what are their corresponding video names?',
                    '5. Which videos have the highest number of likes, and what are their corresponding channel names?',
                    '6. What is the total number of likes and commment count for each video, and what are their corresponding video names?',
                    '7. What is the total number of views for each channel, and what are their corresponding channel names?',
                    '8. Which youtube channel has the highest number of subscribers?',
                    '9. Which videos have the highest number of comments, and what are their corresponding channel names?']
        Question = st.selectbox('Frequestly asked..', options = FAQs)

        if Question == '1. What are the names of all the videos and their corresponding channels?':
            query = 'SELECT channel_name, Video_name from videos;'
            mysql_cursor.execute(query)
            df = pd.DataFrame(mysql_cursor.fetchall(), columns=mysql_cursor.column_names)
            st.header('videos and their channel name')
            st.write(df)

        elif Question == '2. Which channels have the most number of videos, and how many videos do they have?':
            query = '''SELECT channelName, total_videos from channels order by total_videos DESC;'''
            mysql_cursor.execute(query)
            df = pd.DataFrame(mysql_cursor.fetchall(), columns=mysql_cursor.column_names)
            st.write(df)
            
        elif Question == '3. What are the top 10 most viewed videos and their respective channels?':
            query = '''SELECT channel_name, Video_name, view_count from videos order by view_count DESC '''
            mysql_cursor.execute(query)
            df = pd.DataFrame(mysql_cursor.fetchall(), columns=mysql_cursor.column_names)
            st.write(df)

        elif Question == '4. How many comments were made on each video, and what are their corresponding video names?':
            query = '''SELECT Video_name, comment_count from videos order by comment_count '''
            mysql_cursor.execute(query)
            df = pd.DataFrame(mysql_cursor.fetchall(),  columns=mysql_cursor.column_names)
            st.write(df)

        elif Question == '5. Which videos have the highest number of likes, and what are their corresponding channel names?':
            query = '''SELECT channel_name, likecount from videos order by likecount DESC'''
            mysql_cursor.execute(query)
            df = pd.DataFrame(mysql_cursor.fetchall(), columns=mysql_cursor.column_names)
            st.write(df)

        elif Question == '6. What is the total number of likes and commment count for each video, and what are their corresponding video names?':
            query = '''SELECT likecount, comment_count, Video_name from videos '''
            mysql_cursor.execute(query)
            df = pd.DataFrame(mysql_cursor.fetchall(), columns=mysql_cursor.column_names)
            st.write(df)
            
        elif Question == '7. What is the total number of views for each channel, and what are their corresponding channel names?':
            query = '''SELECT channel_name, SUM(view_count) as total_views
                        FROM videos
                        GROUP BY channel_name
                        ORDER BY total_views DESC;'''

            mysql_cursor.execute(query)
            df = pd.DataFrame(mysql_cursor.fetchall(), columns=mysql_cursor.column_names)
            st.write(df)

        elif Question == '8. Which youtube channel has the highest number of subscribers?':
            query = ''' SELECT channelName, subscriber_count from channels order by subscriber_count DESC;'''
            mysql_cursor.execute(query)
            df = pd.DataFrame(mysql_cursor.fetchall(), columns=mysql_cursor.column_names)
            st.write(df)

        elif Question == '9. Which videos have the highest number of comments, and what are their corresponding channel names?':
            query = ''' SELECT Video_name, comment_count, channel_name from videos  order by comment_count DESC LIMIT 10;'''
            mysql_cursor.execute(query)
            df = pd.DataFrame(mysql_cursor.fetchall(), columns=mysql_cursor.column_names)
            st.write(df)

if Selectbox_main == 'About':
    st.subheader(':red[Title:] YouTube Data Harvesting and Warehousing using SQL, MongoDB and Streamlit')  
    st.subheader(':red[Worked on:] Python scripting, Data Collection, MongoDB, Streamlit, API integration, Data Managment using MongoDB (Atlas) and SQL')
    st.subheader(':red[Domain:] Social Media')
    linkedin_url = "https://www.linkedin.com/in/karthikapril/"
    st.subheader(":red[Contact:] You can find me on [LinkedIn](" + linkedin_url + ") 🔬")
