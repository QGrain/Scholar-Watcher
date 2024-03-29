<h1 align="center">
  Scholar-Watcher
</h1>

<p align="center">
  A web app for watching the authors' google scholar, which is based on scholarly and streamlit.
</p>

<p align="center">
<a href="https://github.com/QGrain/Scholar-Watcher/blob/main/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/QGrain/Scholar-Watcher"></a>
<a href="https://github.com/QGrain/Scholar-Watcher/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/QGrain/Scholar-Watcher"></a>
<a href="https://github.com/QGrain/Scholar-Watcher/network"><img alt="GitHub forks" src="https://img.shields.io/github/forks/QGrain/Scholar-Watcher"></a>
<a href="https://github.com/QGrain/Scholar-Watcher/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/QGrain/Scholar-Watcher"></a>
  <img alt="LGTM Grade" src="https://img.shields.io/lgtm/grade/python/github/QGrain/Scholar-Watcher">
</p>


## Features

- Fetch the **citations and changes** of the registered authors. (Support default daily update and force update)
- Display details and Chart Analysis of **Focus Authors**.
- Support add/modify **the registered authors**. (Now disabled for the security concern)
- Display the **latest K publications** of **Focus Authors**.

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

# config the config.ini
# make sure your host could visit Google Scholar. maybe https_proxy needed.
##   (1) if host server could, then set mode = server
##   (2) if host server could not, then set https_proxy and set mode = local

# run Scholar-Watcher app
streamlit run 1_🏠_Scholar_Watcher.py # which is the home page
```

## Change-Log
- v0.1.0 (2022-08-06)
  - Basic framework done with streamlit
  - Could debug locally
- v0.1.1 (2022-08-13)
  - Deploy on streamlit cloud, now it is open for access
- v0.1.2 (2022-08-14)
  - Add a new feature mentioned in [#issue2](https://github.com/QGrain/Scholar-Watcher/issues/2)
- v0.1.3 alpha (2022-08-26)
  - Support auto update at 00:00:01 on server's localtime (That is 08:00:01 of GMT+8)
- v0.1.3 beta (2022-08-28)
  - Remove auto update for the sake of Streamlit cloud. Add Debug page to show info

## Development and Contribution

Any improvements (not only in [Todo](#Todo)) are welcome, in the form of PR.

## Todo

- [x] Add Chart Analysis for focus authors.
- [ ] Add daily auto update. **(Bug to fix)**
- [ ] Add database support.
- [ ] Add Authentication.
- [ ] Add Security Check.
- [x] Deploy on Server.
- [x] Add latest K publications.
- [x] Add show citation log in Debug page.

> Seems that the demo website is down... I should consider fixing the database problems.

## Stargazers over time

[![Stargazers over time](https://starchart.cc/QGrain/Scholar-Watcher.svg)](https://starchart.cc/QGrain/Scholar-Watcher)

