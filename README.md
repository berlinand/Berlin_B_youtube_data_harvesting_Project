# YouTube Data Harvesting and Warehousing using MYSQL, MongoDB and Streamlit
## Introduction:
   
  **Fetching YouTube data using the YouTube Data API, storing it in MongoDB or an unstructured database, migrating the data from MongoDB to 
a MySQL structured database, and visualizing it with Streamlit dashboards for analysis and exploration.**

## workflow:

![Untitled](https://github.com/berlinand/Berlin_B_youtube_data_harvesting_Project/assets/154864172/d37a5e04-7321-4c85-bea6-dbd94d2b340b)

## user interface streamlit vs code:
 **Homepage:**
   .
  ![Screenshot 2024-02-23 202239](https://github.com/berlinand/Berlin_B_youtube_data_harvesting_Project/assets/154864172/07aebc6a-3fa2-4e3b-902d-9e49bdeb2ec1)

Enter one or more channel IDs, separated by commas, in the text box

![Screenshot 2024-02-23 202403](https://github.com/berlinand/Berlin_B_youtube_data_harvesting_Project/assets/154864172/94d1dfff-3ba1-4fc0-8a85-3b14c6cb27fe)
1. After entering the channel ID, you can choose how many videos and comments you want
2. If you don't enter a date for published video before or after text box, the API will provide details for the channel's most recent or latest videos
3. If you enter both a date for videos published before and a date for videos published after in the text boxes, make sure the channel uploaded a video between those dates, or you will receive an error
 ![Screenshot 2024-02-23 202949](https://github.com/berlinand/Berlin_B_youtube_data_harvesting_Project/assets/154864172/eeed949c-f723-4aec-bce3-5302aba27f75)
4. To store duplicate data in the MongoDB database, check the checkbox
5. You can view the data before storing it in MongoDB by clicking the 'View Channel Details' button.
![Screenshot 2024-02-23 203015](https://github.com/berlinand/Berlin_B_youtube_data_harvesting_Project/assets/154864172/912a6ac8-b794-420e-be7b-fcde932cc658)
6. Now, store the data in MongoDB by clicking 'Store Data to MongoDB'

**CODE**
1. Make sure to enter your YouTube API key and MongoDB link in the api_key and mongodblink variables
![Screenshot 2024-02-23 212932](https://github.com/berlinand/Berlin_B_youtube_data_harvesting_Project/assets/154864172/bf95a3a1-7ce2-4e48-a769-2150eafb4ff0)
2. we are using four function from youtube api to fetch data from youtube
     - channels()---->getting--channel details---->need---channel id
 ![Screenshot 2024-02-23 214912](https://github.com/berlinand/Berlin_B_youtube_data_harvesting_Project/assets/154864172/04e90cf7-945b-4f77-93f2-2bf5410fd47e)
     - search()-------> getting---video ids---->need------channel id
          * i am using maxResults=vcount, vcount is video count,so there will be no leakeage of the youtube API quota
![Screenshot 2024-02-23 215409](https://github.com/berlinand/Berlin_B_youtube_data_harvesting_Project/assets/154864172/53aede50-8974-4e8c-a42d-e63c8eab3785)

     - videos()-------->getting--video details--->need---video id
![Screenshot 2024-02-23 214948](https://github.com/berlinand/Berlin_B_youtube_data_harvesting_Project/assets/154864172/77ce75b5-2474-4506-a788-02e37d684ecc)
    - commentsThreads()---->getting--comment details--->need---video id
      * i am using maxResults=comment_count, so there will be no wastage of the youtube API quota
  ![Screenshot 2024-02-23 215006](https://github.com/berlinand/Berlin_B_youtube_data_harvesting_Project/assets/154864172/949d1a1e-969b-4a20-b56b-75a4977b3dd1)


**MongoDB to MYSQL**
Migrating data from MongoDB to MySQL
![Screenshot 2024-02-23 203342](https://github.com/berlinand/Berlin_B_youtube_data_harvesting_Project/assets/154864172/d5707f1f-f31c-4e87-bf93-edfc470aae08)
 1. click the dropdown to select one or more channel names

![Screenshot 2024-02-23 203446](https://github.com/berlinand/Berlin_B_youtube_data_harvesting_Project/assets/154864172/a70a9dc9-541d-4e4c-b704-5762cee9378b)
2.After selecting the channel names, you can view the channel details from MongoDB by clicking the 'View Data in Table Structure' button or 'Save to MySQL' button to store the data.
![Screenshot 2024-02-23 203742](https://github.com/berlinand/Berlin_B_youtube_data_harvesting_Project/assets/154864172/35b3c863-e0c6-40a7-bfa1-f5c0c3e97122)

**code**
Make sure to enter your MongoDB link in the mongodblink variable and Enter your valid MYSQL connection 
![Screenshot 2024-02-23 223026](https://github.com/berlinand/Berlin_B_youtube_data_harvesting_Project/assets/154864172/8fbe4b6f-2689-4169-8e5a-a2153a06803c)

**MYSQL**
Click the dropdown to select one out of ten questions, and the output will be displayed in a table structure

![Screenshot 2024-02-23 203802](https://github.com/berlinand/Berlin_B_youtube_data_harvesting_Project/assets/154864172/df9ce3fe-4aee-48a9-aa04-650b9573124e)
In More: you can select the checkbox to display the tables, i.e., channels, videos, and comments and Merging all three tables into one table from MySQL

![Screenshot 2024-02-23 203839](https://github.com/berlinand/Berlin_B_youtube_data_harvesting_Project/assets/154864172/1963248d-d25a-4639-abf3-37fbef53b036)
**code**
before runing the code, Enter your valid MYSQL connection 
![Screenshot 2024-02-23 224938](https://github.com/berlinand/Berlin_B_youtube_data_harvesting_Project/assets/154864172/dfc25c99-59c8-4a21-9c8f-1846570b756e)
