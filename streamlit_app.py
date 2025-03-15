# # Import python packages
# import streamlit as st
# import requests


# from snowflake.snowpark.functions import col



# # Write directly to the app
# st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
# st.write("Choose the fruits you want in your custom Smoothie!")

# name_on_order = st.text_input('Name on Smoothie:')
# st.write('The name on your Smoothie will be:', name_on_order)

# cnx = st.connection("snowflake")
# session = cnx.session()


# my_dataframe = session.table("smoothies.public.fruit_options").select((col('FRUIT_NAME')))
# # st.dataframe(data=my_dataframe, use_container_width=True)
# # st.stop()

# # pandas
# pd_df = my_dataframe.to_pandas()
# # st.dataframe(pd_df)
# # st.stop()


# ingredients_list = st.multiselect(
#     'Choose up to 5 ingredients:', 
#      my_dataframe,
#     max_selections=5
# )

# if ingredients_list:
#     ingredients_string = ''

#     for fruit_chosen in ingredients_list:
#         ingredients_string += fruit_chosen + ' '

#         search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
#         st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        
#         st.subheader(fruit_chosen + ' Nutrition Information')
#         smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
#         df_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

#     # st.write(ingredients_string)

#     my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
#             values ('""" + ingredients_string + """','""" + name_on_order + """')"""

#     # st.write(my_insert_stmt)
#     # st.stop()
#     time_to_insert = st.button('Submit Order')

#     if time_to_insert:
#         session.sql(my_insert_stmt).collect()
#         st.success('Your Smoothie is ordered!', icon="✅")

# # END


#####################################################


import streamlit
streamlit.title('I am healthy and wealthy. What a great feeling !!!. Kudos to Baru for providing me healthy food daily :)')
streamlit.header('🥗 🥣 Breakfast Menu')
streamlit.text('🐔 Dosa, Vada, Idly, Sambar')
streamlit.text('🍞 Poori, Sagu, Paneer Butter masala')
streamlit.text('🥑 Hard-Boiled Free-Range Egg')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas
import requests
import snowflake.connector
from urllib.error import URLError

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

#Create repeatable code block (function)
def get_fruityvice_data(this_fruit_choice):
      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
      fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      return fruityvice_normalized
    
streamlit.header('FruityVice Fruit Advice !')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
      streamlit.error("Please select a fruit to get the information")
  else:
      back_from_function=get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)

except URLError as e:
  streamlit.error()
#streamlit.stop()

streamlit.header("View our fruit list. Add your Favourites !")
#snowflake related functions
def get_fruit_load_list():
      with my_cnx.cursor() as my_cur:
            my_cur.execute("SELECT * from fruit_load_list")
            return my_cur.fetchall()

#Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
      my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
      my_data_row=get_fruit_load_list()
      my_cnx.close()
      streamlit.dataframe(my_data_row)

#Allow end user to add fruit to list
def insert_row_snowflake(new_fruit):
      with my_cnx.cursor() as my_cur:
            my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('" + new_fruit + "')");
            return "Thanks for adding " +new_fruit
      
add_my_fruit = streamlit.text_input('What fruit would you like to add','Kiwi')
if streamlit.button('Add a fruit to the list'):
      my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
      back_from_function=insert_row_snowflake(add_my_fruit)
      my_cnx.close()
      streamlit.text(back_from_function)
