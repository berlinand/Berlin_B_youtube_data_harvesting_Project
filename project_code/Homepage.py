import streamlit as st
from googleapiclient.discovery import build
from pymongo import MongoClient
import pandas as pd

#*****************************Don't forget to change the value****************************
#paste your youtube api key in api_key variable"
#paste your mongodb connection link  in Mongodblink variable to access your database

api_key="put your youtube api key"
mongodblink="mongodb+srv:// put yor mongodb link that connected to your database"


max_video=50
max_comments=50

mg_connection= MongoClient(mongodblink)
mg_db = mg_connection['youtube']
mg_col_channel = mg_db['channel']
mg_col_video = mg_db['videos']
mg_col_comment= mg_db['comments']


# 1.The youtube_data function return youtube channel details from Channel id using channels function
def youtube_data(channel_id):
   youtube=build('youtube','v3',developerKey=api_key)
   request= youtube.channels().list(
      id=channel_id,
      part='snippet,statistics,contentDetails'
      
   )
   response = request.execute()
   return response



# 2.The video_id function return video id  using search function 
def video_id(channel_id,vcount,bn ,an):
  
   youtube=build('youtube','v3',developerKey=api_key)
   if len(bn)==0:
      before=None
   else:
      before=str(bn).strip()
   if len(an)==0:
      after=None
   else:
      after=str(an).strip()
   
   request = youtube.search().list(
        channelId=channel_id,
        part="snippet",
        order="date",
        maxResults=vcount,
        type="video",
        publishedBefore=before,
        publishedAfter=after
   
    )  
   vid_response= request.execute()
 
   return  vid_response


# 3.The video_datails function return video details from video id using videos function 
def video_details(video_id,vcount):
  youtube=build('youtube','v3',developerKey=api_key)
  request = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        maxResults=vcount,
       
        id =video_id
    )
  vi_response = request.execute()
  return vi_response

# 4.The video_com function return comment details from video id using commentThreads function
def video_com(video_id,comment_count):
  youtube=build('youtube','v3',developerKey=api_key)
  request = youtube.commentThreads().list(
        part="snippet",
    
        maxResults= comment_count,
        videoId =video_id
    )
  com_response = request.execute()
  
  return com_response


# 5.The channel_datas fuction return channel data and if mongodb_button is true or clicked , the data is stored in a MongoDB collection.
def channel_datas(response,Mongodb_button,ch_duplicate): 
  try:
    channel_data ={
     'Channel_Name': response['items'][0]['snippet']['title'],
     'Channel_Id':response['items'][0]['id'],
     'Subscription_Count':response['items'][0]['statistics']['subscriberCount'],
     'Channel_Views':response['items'][0]['statistics']['viewCount'],
     'Channel_Description':response['items'][0]['snippet']['description'],
     'Video_Count':response['items'][0]['statistics']['videoCount']
    
      }
  except:
    channel_data=None

  if Mongodb_button==True: 
   try:
     
    
     try:
      for data in mg_col_channel.find({"Channel_Id":channel_data[ 'Channel_Id']}):

        if ch_duplicate==False: 
           mg_col_channel.delete_many(data)
           st.warning(f"Channel_Id={channel_data['Channel_Id']} ,duplicate or old channel details deleted ")
      mg_col_channel.insert_one(channel_data)
      st.write(f":green[Channel Id={channel_data['Channel_Id']},storing new channel details in mongodb]")
     except:
        mg_col_channel.insert_one(channel_data)
        st.write(f":green[Channel Id={channel_data['Channel_Id']},storing new channel details in mongodb]")
   except Exception as e:
     st.warning(f':red[Mongodb ERROR: please check it and {e}]')     
          
  return channel_data



# 6.The video_data function return vi_data i.e., video data and if mongodb_button is true or clicked , the data is stored in a MongoDB collection.
def video_data( vid_response,vcount,x,Mongodb_button,vid_duplicate):

   try:
    video_id= vid_response['items'][x]['id']['videoId']
   except Exception as e:
             st.warning(f":red[please check the date time value or if channel has no video also put an error and the error {e}]")
             

   vi_response = video_details(video_id,vcount) 
      
   try:
      Tags=vi_response['items'][0]['snippet']['tags']
   except :
     Tags=None 

   vi_data={
     "Video_Id":vi_response['items'][0]['id'],
     "Video_Name":vi_response['items'][0]['snippet']['title'],
     "Video_Description":vi_response['items'][0]['snippet']['description'],
     "Tags": Tags,
     "PublishedAt":vi_response['items'][0]['snippet']['publishedAt'],
    "View_Count":vi_response['items'][0]['statistics']['viewCount'],
     "Like_Count":vi_response['items'][0]['statistics']['likeCount'],
      "Favorite_Count":vi_response['items'][0]['statistics']['favoriteCount'],
     "Comment_Count":vi_response['items'][0]['statistics']['commentCount'],
      "Duration":vi_response['items'][0]['contentDetails']['duration'],
      "Thumbnail":vi_response['items'][0]['snippet']['thumbnails']['default']['url'],
      'Channel_Id':vi_response['items'][0]['snippet']['channelId'],
      "Caption_Status":vi_response['items'][0]['contentDetails']['caption'],
    }  
   if Mongodb_button==True: 
    try:
      
     
      video_id= vi_data["Video_Id"]
      if vid_duplicate==False:
       try:
        for datas in mg_col_video.find({"Video_Id": video_id},{}):
          
           mg_col_video.delete_many(datas)
         
           st.warning(f"video id={video_id} ,duplicate or old video details deleted ")
       except :
        st.write("check mongodb")
      
      mg_col_video.insert_one(vi_data)
      st.write(f":green[video id={video_id},storing new video details in mongodb]")
    except Exception as e:
      st.warning(f":red[ERROR check mongodb connection and {e} ]")

   return vi_data
  
   


# 7.The comm_data function return comment data and if mongodb_button is true or clicked , the data is stored in a MongoDB collection.
def comm_data(com_response,j,Mongodb_button,comm_duplicate):
    
     Comment_datas= {
                   "Video_Id":com_response['items'][j][ 'snippet']['videoId'],
                   "Comment_Id":com_response['items'][j] ['id'],
                    "Comment_Text": com_response['items'][j][ 'snippet']['topLevelComment']['snippet']['textDisplay'],
                    "Comment_Author":com_response['items'][j][ 'snippet']['topLevelComment']['snippet']['authorDisplayName'],
                     "Comment_PublishedAt":com_response['items'][j][ 'snippet']['topLevelComment']['snippet']['publishedAt']
                     }
     if Mongodb_button==True: 
        try:
           
            
            comment_id=Comment_datas['Comment_Id']
            if comm_duplicate==False:
             try:
                for datas in mg_col_comment.find({ "Comment_Id":comment_id},{}):
          
                     mg_col_comment.delete_many(datas)
         
                     st.warning(f"Comment_Id={comment_id} ,duplicate or old comment details deleted ")
             except :
                 st.write("check mongo db")
             st.write(f":green[Comment_Id ={comment_id},storing new comment details in mongodb]")
             mg_col_comment.insert_one(Comment_datas)
        except Exception as e:
             st.warning(f":red[ERROR check mongodb connection and {e} ]")
     
     return {f"Comment_Id_{j}": Comment_datas}




# 8.The vi_comment function return  vi_data i.e., video data updated with comment data
def vi_comment(com_response,comment_count,vi_data,Mongodb_button,comm_duplicate):
    
    comments = {'Comments': {}}

                         
    for j in range(0,comment_count):
          viewcomdatas=comm_data(com_response,j,Mongodb_button,comm_duplicate)
          comments['Comments'].update(viewcomdatas)
    vi_data.update(comments)
   
    return   vi_data
 
   
  
# 9.The click1 function return nothing but all the above eight function are callback by the user request in this function
def click1(vcount,comment_count,channel_ids,bn,an,ch_duplicate,vid_duplicate,comm_duplicate,view_button,Mongodb_button):

 if len(channel_ids)>0:

  channel_Details=channel_ids.split(',')
 
  for channel_id in channel_Details:
   
    
    response = youtube_data(channel_id)
    channel_data= channel_datas(response,Mongodb_button,ch_duplicate)
      
    if view_button==True:
           youtube_view={"Channel_Name": channel_data}

    vicount=vcount
    if int(channel_data['Video_Count'])== 0 or vicount==0:
       st.warning(":red[Either video count is zero or channel vedio count is zero]")
       if view_button==True: 
        st.write( youtube_view)
    else:
      if int(channel_data['Video_Count'])>=vcount:
         vicount=vcount
      else:
         vicount=int(channel_data['Video_Count'])
         st.warning(f":orange[ALert{':'} video count is more than channel, channel video count{':'} ]:blue[{vicount}] :orange[ but channel videos are saved ]")
      if response.get('items'):
          try:
           vid_response= video_id(channel_id,vicount,bn,an)
          except Exception as e:
             st.warning(f":red[please check date time value and the error {e}]")
             
          for x in range(0,vicount):
           
              vi_data =video_data(vid_response,vicount,x,Mongodb_button,vid_duplicate )
      
              if int(vi_data["Comment_Count"])== 0 or comment_count==0:
                  st.warning(":red[Either comment count is zero or vedio comment count is zero]")
                  comment_counti=0
                  
           
              elif int(vi_data["Comment_Count"])>=comment_count:
                 comment_counti=comment_count
                 
              else:
                 comment_counti= int(vi_data["Comment_Count"])
              video_ids=vi_data["Video_Id"] 
              
              com_response= video_com(video_ids,comment_counti)
              
              vi_comm_datas=vi_comment(com_response,comment_counti,vi_data,Mongodb_button,comm_duplicate)
              if view_button==True:
                vi_comm_datas={f"Video_Id_{x}" : vi_data}
               
                youtube_view.update( vi_comm_datas)
          if view_button==True:      
            st.write(youtube_view)

      else:
           st.markdown('**ENTER CHANNEL ID ABOVE**')

 else:
    st.warning(":orange[Enter atleast one channel id]")
 


#--------------------------------------------------------------------------------------------------------------------------------------



    
st.title(":red[YOUTUBE]:blue[ DATA HARVESTING]")
st.header(":violet[Fetch data] 	:crossed_swords: :orange[Store data]")
st.subheader("ENTER YOUTUBE CHANNEL ID")
channel_id=st.text_input("HERE",placeholder='Enter one or more channel IDs, separated by commas')


st.warning(f""":red[NOTE{':'}]:blue[ The published before and published after, date-time value is ]
           :orange[ {'1970-01-31T00:00:00Z '}]:blue[ in the format]:orange[{' yyyy-mm-ddThh:mm:ssZ:-'}]
            If entering both before and after values,
          the video published after date should be lower than before -- if not,index out of range error will occur.""")
col1,col2,col3,col4=st.columns(spec=[3,3,4,4]) 
v_count1=col1.number_input(label='video count',max_value=max_video,min_value=0)
v_count2=col2.number_input(label='comment count',max_value= max_comments ,min_value=0)
pub_bef=col3.text_input(label="video published before",placeholder="1970-01-31T23:48:50Z")
pub_aft=col4.text_input(label="video published after",placeholder="1970-01-31T23:48:50Z")
ch1,ch2,ch3=st.columns(3) 
ch_duplicate=ch1.checkbox(label='channel duplicate',value=False)
vid_duplicate=ch2.checkbox(label='video duplicate',value=False)
comm_duplicate=ch3.checkbox(label='comment duplicate',value=False)
s1,s2,s3=st.columns(spec=[2,1,3])
view_button=s1.button(label='view channel details')
clear=s2.button(label='Clear')
Mongodb_button =s3.button(label='Store data to MongoDB')

try:
 if view_button :
   with st.spinner(':orange[please wait...]'):
     click1(v_count1,v_count2,channel_id,pub_bef,pub_aft,ch_duplicate,vid_duplicate,comm_duplicate,view_button,Mongodb_button) 
   st.balloons()
 if Mongodb_button:
   with st.spinner(':orange[please wait Storing data...]'): 
     click1(v_count1,v_count2,channel_id,pub_bef,pub_aft,ch_duplicate,vid_duplicate,comm_duplicate,view_button,Mongodb_button)
   st.snow()
except TypeError as e:
    st.warning(f":red[ERROR{':'} please enter proper channel id and {e}]")
 

#--------------------------------------------------------------------------------------------------------------------


