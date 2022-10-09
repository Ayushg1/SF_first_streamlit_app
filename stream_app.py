import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
streamlit.title('My Parent new healthy dinner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')#It will show the fruit name while selecting without this it only show the no
# Let's put a pick list here so they can pick the fruit they want to include 
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
# Let's put a pre defined pick list option here so they can pick the fruit they want to include 
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

#Store the selected value in a variable 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
#To show only the selected fruit in the table
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
#streamlit.dataframe(my_fruit_list)
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")

#streamlit.write('The user entered ', fruit_choice)
#import requests
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get a information")
#streamlit.text(fruityvice_response.json())#just writes the data to the screen
# take the json response and normalize it
  else:
    #fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    #fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    back_from_function = get_fruityvice_data(fruit_choice)
    # output it to the screen as table
    #streamlit.dataframe(fruityvice_normalized)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()
  


#import snowflake.connector
#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")#it will fetch the sf username, acc and region
#my_data_row = my_cur.fetchone()
#streamlit.text("Hello from Snowflake:")# it will print the text which is mention
#streamlit.text(my_data_row)# it will show the sf fetch data

#my_cur.execute("SELECT * from fruit_load_list")
#my_data_row = my_cur.fetchone()# this fetch only one record
#my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contain:")
#streamlit.dataframe(my_data_rows)# it will show the sf fetch data

#snowflake related function
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()
  
  
#add a button to load the fruit list
if streamlit.button('Get Fruit load list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)
  
#snowflake related function to insert data
def insert_row_SF(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.fruit_load_list values ('from streamlit')")# this is use to add the value from streamlit into the table
    return "Thanks for adding" + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
#add a button to add the fruit name
if streamlit.button('Add a Fruit to the list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_SF(add_my_fruit)
  streamlit.text(back_from_function)

#don't run anything past this
streamlit.stop()
 
#add_my_fruit = streamlit.text_input('What fruit would you like to add?','Kiwi')
#streamlit.write('Thanks for adding ', add_my_fruit)
#my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.fruit_load_list values ('from streamlit')")# this is use to add the value from streamlit into the table
