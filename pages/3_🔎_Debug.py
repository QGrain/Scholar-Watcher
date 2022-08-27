import streamlit as st
from scholar_watcher_api import *


def getConfigDict(conf):
    sections = ["Proxy", "Settings", "Authors"]
    d = {}
    for sec in sections:
        d[sec] = {}
        for author_label in conf.options(sec):
            d[sec][author_label] = conf[sec][author_label]
    return d


conf = ConfigParser()
conf.read("config.ini", encoding='utf-8')
d_config = getConfigDict(conf)

with open(conf["Settings"]["db_path"], "r", encoding="utf-8") as f:
    d_citation = json.load(f)


st.header('Show Info')

st.subheader('Print config.ini')
st.write('Print current config.ini:')
with st.expander("See config.ini"):
    st.json(dict(d_config))


st.subheader('Print citation.json')
st.write('Print current citation.json:')
with st.expander("See citation.json"):
    st.json(dict(d_citation))