import os
import streamlit as st
from streamlit_chat import message
from langchain_community.llms import HuggingFaceEndpoint
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import (ConversationBufferMemory, 
                                                  ConversationSummaryMemory, 
                                                  ConversationBufferWindowMemory
               
                                                  )

if 'conversation' not in st.session_state:
    st.session_state['conversation'] = None

if 'message' not in st.session_state:
    st.session_state['message'] = []

if 'API_Key' not in st.session_state:
    st.session_state['API_Key'] =''


#Staring Ui Code here :

st.set_page_config('Hi i am chat bot you can talk with me ' , page_icon= ':robot_face:')
st.markdown("<h1 style='text-align: center;'>How can I assist you? </h1>", unsafe_allow_html=True)

st.sidebar.title("😎")
api_key_input = st.sidebar.text_input("Enter your API Key here:", type='password')

if api_key_input:
    st.session_state['API_Key'] = api_key_input
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = st.session_state['API_Key']  # Set the environment variable

summarise_button = st.sidebar.button("Summarise the conversation", key="summarise")

if summarise_button:
    summarise_placeholder = st.sidebar.write("Nice chatting with you my friend ❤️:\n\n"+st.session_state['conversation'].memory.buffer)



def get_text(userInput ,api_key):

    if st.session_state['conversation'] is None:

        llm  = HuggingFaceEndpoint(repo_id="mistralai/Mistral-7B-Instruct-v0.2" , max_length=10, temperature=1.0, huggingfacehub_api_token=api_key)

        st.session_state['conversation'] = ConversationChain(
        llm = llm,
        verbose = True,
        memory= ConversationSummaryMemory(llm=llm)
        )

    response = st.session_state['conversation'].predict(input=userInput)
    print (st.session_state['conversation'].memory.buffer)

    return response


response_container = st.container()

container = st.container()


with container:
    with st.form(key='my_form' , clear_on_submit=True):
        user_input = st.text_area("Your question goes here :" , key=input  ,height=100)
        submit_button = st.form_submit_button(label="Send")


        if submit_button:
            st.session_state['message'].append(user_input)
            model_response = get_text(user_input ,st.session_state['API_Key'] )
            st.session_state['message'].append(model_response)

            with response_container:
                for i in range(len(st.session_state['message'])):
                        if (i % 2) == 0:
                            message(st.session_state['message'][i], is_user=True, key=str(i) + '_user')
                        else:
                            message(st.session_state['message'][i], key=str(i) + '_AI')


         