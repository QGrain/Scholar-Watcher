import streamlit as st
from scholar_watcher_api import *


def getAuthorDict(conf):
    d_authors = {}
    for author_label in conf.options('Authors'):
        d_authors[author_label] = conf['Authors'][author_label]
    return d_authors


conf = ConfigParser()
conf.read("config.ini", encoding='utf-8')
d_authors = getAuthorDict(conf)

st.header('Configurations')

st.subheader('Add Author')
st.write('Scholar Watcher also supports adding more authors for watching. Current in-watching authors are as follows:')
with st.expander("See current authors"):
    st.json(dict(d_authors))

add_input1, add_input2 = st.columns(2)
add_user_label = add_input1.text_input(label='Input the author name (no cap/blank)', key='add-input1', help='the option in config section', value='zhiyuzhang')
add_user_id = add_input2.text_input(label='Input the Google scholar ID of the author', key='add-input2', help='the string after "user=" in thr url', value='px8_S6IAAAAJ')
st.write(f'Are you sure to add "{add_user_label} = {add_user_id}" ?')

add_check = st.button('Yes', key='add-button')
if add_check == True:
    if add_user_label in d_authors.keys():
        st.warning(f'user_name **{add_user_label}** already in configuration, cannot add duplication!')
    elif add_user_id in d_authors.values():
        st.warning(f'user_id **{add_user_id}** already in configuration, cannot add duplication!')
    # todo: better to add valid check for the id
    else:
        conf.set('Authors', add_user_label, add_user_id)
        conf.write(open("config.ini", "w", encoding='utf-8'))
        add_success = st.success(f'Success add author: **{add_user_label} = {add_user_id}**')
        conf.read("config.ini", encoding='utf-8')
        d_authors = getAuthorDict(conf)
        add_success = st.success(f'Success add author: **{add_user_label} = {add_user_id}**, and update related variable')
    add_check = False

st.subheader('Update Author')
st.write('Scholar Watcher also supports adding more authors for watching.')

update_input1, update_input2 = st.columns(2)
update_user_label = update_input1.text_input(label='Input the author name (no cap/blank)', key='update-input1', help='the option in config section', value='zhiyuzhang')
update_user_id = update_input2.text_input(label='Input the Google scholar ID of the author', key='update-input2', help='the string after "user=" in thr url', value='px8_S6IAAAAJ')
st.write(f'Are you sure to update to "{update_user_label} = {update_user_id}" ?')

update_check = st.button('Yes', key='update-button')
if update_check == True:
    if update_user_label not in d_authors.keys():
        st.warning(f'user_name **{update_user_label}** not in configuration, cannot update no one!')
    # todo: better to add valid check for the id
    else:
        conf.set('Authors', update_user_label, update_user_id)
        conf.write(open("config.ini", "w", encoding='utf-8'))
        update_success = st.success(f'Success update author: **{add_user_label} = {update_user_id}**')
        conf.read("config.ini", encoding='utf-8')
        d_authors = getAuthorDict(conf)
        update_success = st.success(f'Success update author: **{add_user_label} = {update_user_id}**, and update related variable')
    update_check = False