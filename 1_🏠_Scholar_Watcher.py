from concurrent.futures import thread
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scholar_watcher_api import *
from math import ceil


conf = ConfigParser()
conf.read("config.ini", encoding='utf-8')
Proxy = conf['Proxy']
Authors = conf['Authors']
Settings = conf['Settings']

# need to add server check here
if Settings['mode'] == 'local':
    os.environ["http_proxy"] = Proxy['http_proxy']
    os.environ["https_proxy"] = conf['Proxy']['https_proxy']

searcher = SearchEngine()
citation = Citation(Settings['db_path'])

# auto update at 2 am everyday
# see there is a todo about this timer
# initial_timer = threading.Timer(getSecondsToTime(1, 1, 0), autoUpdateEveryDay, (searcher, citation, conf)).start()
# timer_manager = TimerManager(initial_timer)

# default checkUpdate()
checkUpdate(searcher, citation, conf, single_author=None, force=False)
d_all = citation.read()
d_citation = citation.present()
df_present = pd.DataFrame(d_citation).T


st.set_page_config(
     page_title="Scholar Watcher 2022@Zhiyu Zhang",
     page_icon="🧊",
     layout=Settings['layout'],
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://www.extremelycoolapp.com/help',
         'Report a bug': "https://www.extremelycoolapp.com/bug",
         'About': "## Scholar Watcher\n ## 2022@Zhiyu Zhang"
    }
)

# 🎈🧨✨🎉🎯🎖️
st.title('Scholar Watcher 🏠')
st.header('1 Google Scholar Citations')

cite_tab1, cite_tab2 = st.tabs(['DataFrame (Interactable)', 'Table (Static)'])
with cite_tab1:
    st.info('💡 Tips: This DataFrame is **interactable**. You can **sort** the columns by clicking the column name and **resize** the columns by dragging the borders.')
    st.dataframe(df_present, height=385, width=500)

with cite_tab2:
    st.info('💡 Tips: This table is **static**.')
    st.table(df_present)

st.warning('Citation table would update **once a day**. Force update would update **immediately** and **time-costly**.')
btn_click = st.button('Force Update', help='This would update the citation immediately')


if btn_click == True:
    progress_msg = st.empty()
    progress_bar = st.progress(0)  
    for i, author_label in enumerate(Authors):
        progress_msg.text(f'Iterate {i+1}/{len(Authors)} authors')
        p = int(i/len(Authors) * 100)
        checkUpdate(searcher, citation, conf, single_author=author_label, force=True)
        progress_bar.progress(p)
    progress_bar.progress(100)
    btn_click = False
    st.success('Force check citation update done!')
    st.balloons()


# Add a selectbox to the sidebar:
layout_selectbox = st.sidebar.selectbox(
    'Page layout',
    ('centered', 'wide')
)

d = st.sidebar.date_input(
    "Select a date filter",
    date(2022, 8, 6))
st.sidebar.write('You select:', d)
st.sidebar.info('Well this ⬆ sidebar module is still in developing actually.')



st.header('2 Focus Authors')

focus_authors = st.multiselect(
     'Pleasec select the focus authors',
     conf['Authors'],
     ['kaichen', 'guozhumeng', 'xiaofengwang'],
     help='Choose the focus authors, and display the analytics.')
# st.text(f'You have selected {len(focus_authors)} authors to focus on.')
st.info(f'You have selected **{len(focus_authors)}** authors to focus on.')

focus_author_ids = []
focus_chart_columns = []
for focus_author_label in focus_authors:
    focus_chart_columns.append(focus_author_label)
    focus_author_ids.append(Authors[focus_author_label])

tab1, tab2, tab3, tab4 = st.tabs(['🚀 Metrix', '📈 Charts', '🔎 Recent Publications', '🎯 Todo'])
with tab1:
    st.subheader('Citation Metrix 🚀')
    if len(focus_authors) == 0:
        st.warning('No focus author')
    else:
        if Settings['layout'] == 'wide':
            max_col_num = 8
        else:
            max_col_num = 5
        row_num = ceil(len(focus_authors) / max_col_num)
        matrix = []
        for i in range(row_num):
            matrix.append(st.columns(max_col_num))
        for i in range(len(focus_authors)):
            row = int(i/max_col_num)
            col = i % max_col_num
            author_name = d_all[Authors[focus_authors[i]]]['name']
            matrix[row][col].metric(label=focus_authors[i], value=d_citation[author_name]['citation'], delta=d_citation[author_name]['increase'])

with tab2:
    st.subheader('Analysis Charts 📈')
    if len(focus_authors) == 0:
        st.warning('No focus author')
    else:
        # focus_plot_data, earliest_date = getPlotData(d_all, author_ids)
        # plt.title('Focus Authors Citation Over Time')
        # for i in range(len(focus_authors)):
        #     fig = plt.plot(focus_plot_data[i]['X_DATA'], focus_plot_data[i]['Y_DATA'], label=focus_authors[i])
        # plt.legend()
        # plt.xlabel('Date')
        # plt.ylabel('Citation')
        # st.pyplot(fig)

        # print(author_ids)
        focus_chart_data = pd.DataFrame(np.array(citation.getSequence(focus_author_ids)).T, columns=focus_chart_columns)
        # focus_chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['a', 'b', 'c'])
        # print(focus_chart_data)

        st.line_chart(focus_chart_data)
        st.write('Todo...')

with tab3:
    st.subheader('Recent Publications 🔎')
    st.warning('This is runtime fetching, so it will take some time. **Please wait after pressing Go...**')
    tab3_col1, tab3_col2 = st.columns(2)
    latest_k = tab3_col1.number_input(label='Input Latest K (1~20) Publications to fetch', min_value=1, max_value=20, value=3, step=1, format='%d')
    tab3_col2.caption('Click here ⬇')
    latest_go = tab3_col2.button('GO!')
    if latest_go == True:
        for i, author_id in enumerate(focus_author_ids):
            # recent_pubs = searcher.fetchRecentTopKPub(author_id, 3)
            latest_pubs = fetchLatestKPub(author_id, latest_k)
            with st.expander(f"{focus_authors[i]}\'s latest {latest_k} publications"):
                # st.write(recent_pubs)
                st.write(latest_pubs)
        latest_go = False

with tab4:
    st.subheader('Todo 🎯')
    st.warning('Todo, you can raise issues to help improve this. (https://github.com/QGrain/Scholar-Watcher/issues)')


st.header('3 About This Site')

st.markdown('Hello, welcome to **Scholar Watcher**, which could watching the google scholar citation changes of the following authors.')

with st.expander("Easter Egg"):
    # st.snow()
    st.write("""
        Emmm, I am supposed to put an Easter egg here. But I don't have anyting.  :p
        \nSo, what about following me on github (https://github.com/QGrain/)?
    """)
    st.image("https://avatars.githubusercontent.com/u/38586306?v=4")
