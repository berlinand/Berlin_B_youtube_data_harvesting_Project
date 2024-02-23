import streamlit as st
import pandas as pd
import mysql.connector


#*****************************Don't forget to change the value****************************
#connection variable is to connect mysql database, change the value in host ,user, password,database you are going to use,
# so that you can connect your mysql 

connection=mysql.connector.connect(host='localhost',user='root',password='berlin',database='youtube')
mycursor=connection.cursor()




#The query function runs corresponding to the selected question and displays the results in a dataframe.
def query(selected):
 
   if selected=="What are the names of all the videos and their corresponding channels?":
        query1="""select Channels.Channel_Name,Videos.Video_Name from Channels left join Videos on Channels.Channel_Id=Videos.Channel_Id
                  order by Channels.Channel_Name"""
        mycursor.execute(query1)
        result1=mycursor.fetchall()
        df=pd.DataFrame(result1,columns=["Channel Name","Video Name"])
        st.dataframe(df)

      
   if selected =="Which channels have the most number of videos, and how many videos do they have?":
     
      query2="select Channels.Channel_Name,Channels.Video_Count from Channels order by Video_count DESC limit 5"
      mycursor.execute(query2)
      result2=mycursor.fetchall()
      df=pd.DataFrame(result2,columns=["Channel Name","Video count"])
      st.dataframe(df)

   if selected=="What are the top 10 most viewed videos and their respective channels?":
      
      query3="""select Videos.Video_Name ,Videos.View_Count,Channels.Channel_Name from Channels left join Videos 
                on Channels.Channel_ID=Videos.Channel_Id
                order by View_count DESC limit 10"""
      
      mycursor.execute(query3)
      result3=mycursor.fetchall()
      df=pd.DataFrame(result3,columns=["Video Name","View count","Channel Name"])
      st.dataframe(df)


   if selected=="How many comments were made on each video, and what are their corresponding video names?":
      query4="select Videos.Video_Name ,Videos.Comment_Count from  Videos order by Comment_count DESC "

      mycursor.execute(query4)
      result4=mycursor.fetchall()
      df=pd.DataFrame(result4,columns=["Video Name","Comment count"])
      st.dataframe(df)
    

   if selected=="Which videos have the highest number of likes, and what are their corresponding channel names?":
      query5="""select Videos.Video_Name,Videos.Like_Count,Channels.Channel_Name from Channels left join Videos 
                on Channels.Channel_ID=Videos.Channel_Id
                order by Like_count DESC limit 10"""

      mycursor.execute(query5)
      result5=mycursor.fetchall()
      df=pd.DataFrame(result5,columns=["Video Name","Like count","Channel Name"])
      st.dataframe(df)

   if selected=="What is the total number of likes for each video, and what are their corresponding video names?":
      query6="select Videos.Video_Name ,Videos.Like_Count from  Videos order by Like_count DESC"
      
      mycursor.execute(query6)
      result6=mycursor.fetchall()
      df=pd.DataFrame(result6,columns=["Video Name","Like Count"])
      st.dataframe(df)


   if selected=="What is the total number of views for each channel, and what are their corresponding channel names?":
      query7="select Channels.Channel_Name, Channels.Channel_Views from Channels order by Channel_Views DESC"
    
      mycursor.execute(query7)
      result7=mycursor.fetchall()
      df=pd.DataFrame(result7,columns=["Channel Name","Channel Views"])
      st.dataframe(df)


   if selected== "What are the names of all the channels that have published videos in the year 2022?":
      query8="""select Channels.Channel_Name,Videos.Video_Name from Channels left join Videos 
             on Channels.Channel_Id=Videos.Channel_Id where PublishedAt like'%2022%' """
      mycursor.execute(query8)
      result8=mycursor.fetchall()
      df=pd.DataFrame(result8,columns=["Channel Name","Video Name"])
      st.dataframe(df)

   if selected=="What is the average duration of all videos in each channel, and what are their corresponding channel names?":
      query9="""select Channels.Channel_Name,avg(Videos.Duration_Sec) as avg_duration
               from Channels left join Videos on Channels.Channel_Id=Videos.Channel_Id
               group by Channels.Channel_Id,Videos.Channel_Id
               order by avg_duration DESC  """
      
      mycursor.execute(query9)
      result9=mycursor.fetchall()
      df=pd.DataFrame(result9,columns=["Channel Name","Avgerage Duration in Second"])
      st.dataframe(df)

   if selected=="Which videos have the highest number of comments, and what are their corresponding channel names?":
        query10="""select Videos.Video_Name,Videos.Comment_Count,Channels.Channel_Name from Videos left join Channels
                  on Videos.Channel_Id=Channels.Channel_Id 
                  order by Videos.Comment_Count desc limit 10"""
        
        mycursor.execute(query10)
        result10=mycursor.fetchall()
        df=pd.DataFrame(result10,columns=["Video Name","Comment Count"," Channel Name"])
        st.dataframe(df)


#The show channel function shows all the data in Channels table from mysql database
def show_channels():
   
      query11="select * from Channels"
      mycursor.execute(query11)
      result11=mycursor.fetchall()
      df=pd.DataFrame(result11,columns=["Channel_Name","Channel_Id",
                                        "Subscription_Count","Channel_Views","Channel_Description","Video_Count"])
      st.dataframe(df)


#The show videos function shows all the data in Videos table from mysql database
def show_videos():
   
      query12="select * from Videos"
      mycursor.execute(query12)
      result12=mycursor.fetchall()
      df=pd.DataFrame(result12,columns=["Video_Id","Video_Name",'Video_Description','Tags','PublishedAt',
                     'View_Count','like_Count','Favorite_Count','Comment_Count','Duration_Sec',
                     'Thumbnail','Channel_Id','Caption_Status'])
      st.dataframe(df)


#The show Comments function shows all the data in Comments table from mysql database
def show_comments():
   
      query13="select * from Comments"
      mycursor.execute(query13)
      result13=mycursor.fetchall()
      df=pd.DataFrame(result13,columns=["Comment_Id",'Video_Id','Comment_Text','Comment_Author','Comment_PublishedAt'])
      st.dataframe(df)    


##The show all function shows all the data in Channels,Videos and Comments tables in a single table 
def show_all():
      query14="""select Channel_Name,Channels.Channel_Id,Subscription_Count,Channel_Views,Channel_Description,Video_Count,
      Videos.Video_Id,Video_Name,Video_Description,Tags,PublishedAt,
                     View_Count,like_Count,Favorite_Count,Comment_Count,Duration_Sec,
                     Thumbnail,Caption_Status,Comment_Id,Comment_Text,Comment_Author,Comment_PublishedAt
        from Channels left join Videos on Channels.Channel_Id=Videos.Channel_Id
                left join Comments on Videos.Video_id=Comments.Video_Id
                order by Channel_Name """
      mycursor.execute(query14)
      result14=mycursor.fetchall()
      df=pd.DataFrame(result14,columns=["Channel_Name","Channel_Id",
                                        "Subscription_Count","Channel_Views","Channel_Description","Video_Count",
                                        "Video_Id","Video_Name",'Video_Description','Tags','PublishedAt',
                                       'View_Count','like_Count','Favorite_Count','Comment_Count','Duration_Sec',
                                                  'Thumbnail','Caption_Status',
                     "Comment_Id",'Comment_Text','Comment_Author','Comment_PublishedAt'])
      st.dataframe(df)

#The year function wil show the channel name, video name and published date&time    
def year(years):
    year=years.split(',')
    for x in year:
      st.subheader(f"Year{':'} :red[{x}]")
      query15=f"""select Channels.Channel_Name,Videos.Video_Name,PublishedAt from Channels left join Videos 
             on Channels.Channel_Id=Videos.Channel_Id where PublishedAt like'%{x}%' """
      mycursor.execute(query15)
      result15=mycursor.fetchall()
      df=pd.DataFrame(result15,columns=["Channel Name","Video Name","PublishedAt"])
      st.dataframe(df)   
    
#----------------------------------------------------------------------------------------------------------------------------
      
st.title(" :one::zero: :green[MYSQL] :orange[Query]")
ques=["What are the names of all the videos and their corresponding channels?",
      "Which channels have the most number of videos, and how many videos do they have?",
      "What are the top 10 most viewed videos and their respective channels?",
      "How many comments were made on each video, and what are their corresponding video names?",
      "Which videos have the highest number of likes, and what are their corresponding channel names?",
      "What is the total number of likes for each video, and what are their corresponding video names?",
      "What is the total number of views for each channel, and what are their corresponding channel names?",
      "What are the names of all the channels that have published videos in the year 2022?",
      "What is the average duration of all videos in each channel, and what are their corresponding channel names?",
      "Which videos have the highest number of comments, and what are their corresponding channel names?"
      ]

st.subheader("select a question")
selected=st.selectbox(label='here',options=ques,placeholder="select any one",index=None)
if selected in ques:
 query(selected)
st.subheader(f":violet[More{':'}]")
c1,c2,c3,c4=st.columns(4)
ch_channel=c1.checkbox(label="show Channels")
ch_videos=c2.checkbox(label='show videos')
ch_comments=c3.checkbox(label="show comments")
ch_all=c4.checkbox(label="show_All")
if ch_channel==True:
   show_channels()
if ch_videos==True:
   show_videos()
if ch_comments==True:
   show_comments()
if ch_all==True:
    show_all()
years=['2015','2016','2017','2018','2019','2020','2021','2022','2023','2024']

year_select=st.multiselect(label=f'select a videos published year{':'}',
                           options=years)

select_year=str(",".join(year_select))
st.write("you've selected"+f" :green{year_select}")
a1,a2=st.columns(2)
year_button=a1.button(label='output')
clear_button=a2.button(label="clear")
if year_button==True:
   if len(year_select)>0:
     with st.spinner(':orange[please wait...]'):
      year(select_year)
     st.balloons()

   else:
      st.warning(f"select atleast one option") 
    
    
#------------------------------------------------------------------------------------------------------------------------
 

