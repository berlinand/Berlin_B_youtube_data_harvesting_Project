from pymongo import MongoClient
import streamlit as st
import pandas as pd
import mysql.connector

#*****************************Don't forget to change the value****************************
#paste your mongodb connection link  in Mongodblink variable to access your database
#connection variable is to connect mysql database, change the value in host ,user, password,database you are going to use,
# so that you can connect your mysql 
mongodblink="mongodb+srv:// put yor mongodb link that connected to your database"

connection=mysql.connector.connect(host='localhost',user='root',password='berlin',database='youtube')
mycursor=connection.cursor()

mg_connection= MongoClient(mongodblink)
mg_db = mg_connection['youtube']
mg_channel = mg_db['channel']
mg_videos = mg_db['videos']
mg_comments=mg_db['comments']




# 1.The show_mgchannelname function returns all the channel names in the form of a list from the MongoDB collection.
def show_mgchannelname():
      channel_name=[]
      for ch_datas in mg_channel.find({'Channel_Name':{'$exists':True}}):
          channel_name.append(ch_datas['Channel_Name'])
      return channel_name



#2. The connvert_channel_sql function return channel id ,
#   if view button is true , display channel details in dataframe .
#   if sql_button is true , migrating channel data from MongoDB to MYSQL
def convert_channel_sql(ch_name,view_button,sql_button):
   
          
           channel = mg_channel.find({'Channel_Name':ch_name},{'_id':0})
           
           df_channel=pd.DataFrame(channel)
           channel_id=str(df_channel.iloc[0,1])
           
          
           if view_button==True:
             st.subheader('channel:  '+f":violet[{ch_name}]")
             st.write(df_channel)
             
            
           if sql_button==True:
                mycursor.execute("show tables like 'Channels'")
                sq_ch=mycursor.fetchall()
                if len(sq_ch)==0:
                    query1="""create table Channels(Channel_Name varchar(255),
                                    Channel_Id varchar(255) primary key,
                                     Subscription_Count int,
                                      Channel_Views bigint,
                                      Channel_Description text,
                                       Video_Count int)"""
                    mycursor.execute(query1)
                
                query2=f"""update Channels set Channel_Name="{df_channel.iloc[0,0].replace('"',"'")}",   
                       Subscription_Count={df_channel.iloc[0,2]},
                        Channel_Views={df_channel.iloc[0,3]},
                        Channel_Description="{df_channel.iloc[0,4].replace('"',"'")}",
                        Video_Count={df_channel.iloc[0,5]}
                          where Channel_Id='{channel_id}'"""
                
                query3=f"""insert into Channels(Channel_Name,Channel_Id,Subscription_Count,Channel_Views,Channel_Description,Video_Count)
                  values("{df_channel.iloc[0,0].replace('"',"'")}","{df_channel.iloc[0,1]}",{df_channel.iloc[0,2]},
                  {df_channel.iloc[0,3]},"{df_channel.iloc[0,4].replace('"',"'")}",{df_channel.iloc[0,5]})"""
                


                try: 
                     
                     mycursor.execute(query3)
                     connection.commit()
                except:
                     mycursor.execute(query2)
                     connection.commit()
             
                
                    
                    
    
           return channel_id    

#3. The connvert_videos_sql function return video_ids ,
#   if view button is true , display Video details in dataframe .
#   if sql_button is true , migrating video data from MongoDB to MYSQL           
def convert_videos_sql(channel_id,view_button,sql_button): 
    
     vi=mg_videos.find({'Channel_Id':channel_id},{'_id':0})
     df_video=pd.DataFrame(vi)
     video_ids=[]
     video_idss=df_video[df_video.columns[0]]
     for y in video_idss:
         video_ids.append(y) 
     if view_button==True:
        st.subheader('videos:')
        st.write(df_video)
          
     if sql_button ==True:
       mycursor.execute("show tables like 'Videos'")
       sq_vi=mycursor.fetchall()
       if len(sq_vi)==0:
            query1="""create table Videos(Video_Id varchar(255) primary key,
                        Video_Name varchar(255),
                        Video_Description text,
                        Tags varchar(800),
                        PublishedAt varchar(255),
                        View_Count int,
                        Like_Count int,
                        Favorite_Count int,
                        Comment_Count int,
                        Duration_Sec int,
                        Thumbnail varchar(255),
                        Channel_Id varchar(255),
                        foreign key (Channel_Id) references Channels(Channel_Id), 
                        Caption_Status varchar(20))"""
            mycursor.execute(query1)

      
        
       for x in range(0,len(df_video)):
           
           video_id=df_video.iloc[x,0]
           
           duration= df_video.iloc[x,9]
#           duration_sec in second
           dt=duration.removeprefix('PT')
           if dt.find('H')!=-1:
               if dt.find('M')==-1 and dt.find('S')==-1:
                   h,s=dt.removesuffix("H")
                   duration_sec=(int(h)*3600)
               elif dt.find('M')==-1:
                 h,s=dt.replace("H"," ").removesuffix("S").split()
                 duration_sec=(int(h)*3600)+int(s)  
               elif dt.find('S')==-1:
                    h,m=dt.replace("H"," ").removesuffix('M').split()
                    duration_sec=(int(h)*3600)+(int(m)*60)
               else:
                 h,m,s=dt.replace("H"," ").replace('M',' ').removesuffix("S").split()
                 duration_sec=(int(h)*3600)+(int(m)*60)+int(s)

           elif dt.find('M')!=-1:   
               if dt.find('S')==-1:
                 m= dt.replace('M',' ')
                 duration_sec=(int(m)*60)
               else:
                 m,s= dt.replace('M',' ').removesuffix("S").split()
                 duration_sec=(int(m)*60)+int(s)

           else : 
               s=dt.removesuffix('S')
               duration_sec=int(s)
               


           tag=df_video.iloc[x,3]
           tags=str(tag).removeprefix('[').removesuffix(']').replace('"'," ' " )
          

           query2=f"""update Videos set Video_Name="{df_video.iloc[x,1].replace('"',"'" )}",
                  Video_Description="{df_video.iloc[x,2].replace('"',"'" )}",
                  Tags="{tags}",PublishedAt="{df_video.iloc[x,4]}",View_Count={df_video.iloc[x,5]},
                  like_Count={df_video.iloc[x,6]},Favorite_Count={df_video.iloc[x,7]},
                  Comment_Count={df_video.iloc[x,8]},Duration_sec={duration_sec},
                  Thumbnail="{df_video.iloc[x,10]}",Caption_Status="{df_video.iloc[x,12]}"
                  where Video_Id="{video_id}" """
           

           query3=f"""insert into Videos(Video_Id,Video_Name,Video_Description,Tags,PublishedAt,
                     View_Count,like_Count,Favorite_Count,Comment_Count,Duration_Sec,
                     Thumbnail,Channel_Id,Caption_Status) values("{df_video.iloc[x,0]}",
                     "{df_video.iloc[x,1].replace('"',"'" )}","{df_video.iloc[x,2].replace('"',"'" )}",
                     "{tags}","{df_video.iloc[x,4]}",
                     {df_video.iloc[x,5]},{df_video.iloc[x,6]},{df_video.iloc[x,7]},{df_video.iloc[x,8]},
                     {duration_sec},"{df_video.iloc[x,10]}","{df_video.iloc[x,11]}","{df_video.iloc[x,12]}"
                    )"""
           
           try: 
             mycursor.execute(query3)
             connection.commit()

           except:
                mycursor.execute(query2)
                connection.commit()
           
     return video_ids    


#4. The connvert_comments_sql function return Nothing ,
#   if view button is true , display comments details in dataframe .
#   if sql_button is true , migrating comment data from MongoDB to MYSQL            
def convert_comments_sql(video_ids,view_button,sql_button):
    if  view_button==True:
      st.subheader('comments:')
    for video_id in video_ids:
       
      
       comments= mg_comments.find({'Video_Id':video_id},{'_id':0})  
       df_comment=pd.DataFrame(comments)
     

       if  view_button==True:
           st.write(df_comment)

       if sql_button==True:
          mycursor.execute("show tables like 'Comments'")
          sql_comm=mycursor.fetchall()  
          if len(sql_comm)==0:
              query1="""create table Comments(Comment_Id varchar(255) primary key,Video_Id varchar(255),
                       Comment_Text text,Comment_Author varchar(255),Comment_PublishedAt varchar(255),
                       foreign key (Video_Id) references Videos(Video_Id)) """
              
              mycursor.execute(query1)
          for x in range(0,len(df_comment)):
             query2=f"""update Comments set Comment_Text="{df_comment.iloc[x,2].replace('"',"'" )}",
                      Comment_Author="{df_comment.iloc[x,3]}",
                     Comment_PublishedAt="{df_comment.iloc[x,4]}"
                     where Comment_Id="{df_comment.iloc[x,1]}" """

             query3=f"""insert into Comments(Comment_Id,Video_Id,Comment_Text,Comment_Author,Comment_PublishedAt) values(
                  "{df_comment.iloc[x,1]}",
                  "{df_comment.iloc[x,0]}", "{df_comment.iloc[x,2].replace('"',"'" )}",   
                  "{df_comment.iloc[x,3]}","{df_comment.iloc[x,4]}" ) """  
             
             try:
                mycursor.execute(query3)
                connection.commit()
             except:
              
               mycursor.execute(query2)
               connection.commit()


      
          
   
#5. The my_sql function return nothing but all the above eight function are callback by the user request in this function
def my_sql(selection,view_button,sql_button):     
     if len(selection)>0: 
          channel_name= selection.split(',')
    
          for ch_name in channel_name:        
            
             channel_id= convert_channel_sql(ch_name,view_button,sql_button)
             video_ids=convert_videos_sql(channel_id,view_button,sql_button)
             comment=convert_comments_sql(video_ids,view_button,sql_button)
     else:
       st.warning('please select atleast one channel')
#--------------------------------------------------------------------------------------------------------------------------------

st.title(":blue[Migrating ] :red[YouTube ] :blue[Channel Data]")
st.header(":orange[MongoDB]  :arrow_right_hook:  :green[ MYSQL]")
st.subheader("SELECT CHANNEL NAMES:")
selected=st.multiselect(label="here",options=show_mgchannelname(),placeholder="Select one or more channel names")
selection=str(",".join(selected))
st.write("you've selected"+f":green[  {selection}]")
p1,p2,p3=st.columns(3)
view_button=p1.button(label='view data in table structure')
clear_button=p2.button(label= 'clear')
sql_button=p3.button(label="save to mysql")
if view_button:
   with st.spinner(':orange[please wait...]'):
     my_sql(selection,view_button,sql_button)
   st.balloons()
if sql_button:
    with st.spinner(':orange[please wait Migrating data...]'):
      my_sql(selection,view_button,sql_button)
    st.snow()
    st.success('Done :+1:')




#------------------------------------------------------------------------------------------------------------------------