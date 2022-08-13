# Scholar-Watcher
A web app for watching the authors' google scholar, which is based on scholarly and streamlit.


## Features

- Fetch the **citations and changes** of the registered authors. (Support default daily update and force update)
- Display details and Chart Analysis of **Focus Authors**.
- Support add/modify **the registered authors**. (Now disabled for the security concern)
- Display the **recent publications** of **Focus Authors**. (Incoming)


## Demo

- View demo through this [demo-link](https://qgrain-scholar-watcher-1--scholar-watcher-holt9c.streamlitapp.com/):

<img src="https://raw.githubusercontent.com/QGrain/picgo-bed/main/figure-2022/202208062119477.png"/>


## Self-Host

Generally, there is only one hosted Scholar-Watch needed for each group, as they can customize their own registered authors in their fields. So here is the way for self-host.

```bash
# (recommended)create a conda env, you should install conda/miniconda first
conda create -n streamlit python=3.7
conda activate streamlit

# install dependencies
pip install -r requirements.txt

# run Scholar-Watcher app
streamlit run 1_🏠_Scholar_Watcher.py # which is the home page
```

## Development and Contribution

Any improvements (not only in [Todo](#Todo)) are welcome, in the form of PR.

## Todo

- [x] Add Chart Analysis for focus authors.
- [ ] Add daily auto update.
- [ ] Add database support.
- [ ] Add Authentication.
- [ ] Add Security Check.
- [x] Deploy on Server.
- [ ] Add recent publications.
