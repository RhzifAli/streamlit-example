import streamlit as st
import time
from datetime import datetime
import requests


st.set_page_config(page_title="My Webpage", page_icon=":tada:", layout="wide")

url = "https://i.instagram.com/api/v1/direct_v2/get_presence/"

headers = {
    'x-csrftoken': 'JIqamHNQRJlbPXMsGxpbhk2KY0Vzmgn9',
    'x-ig-app-id': '936619743392459',
    'cookie': 'ig_did=50A7C5AA-6647-45F1-B7AA-643341B08B3D; ig_nrcb=1; mid=YXhEXAALAAEd8OHslYccyq4NDOdn; '
              'fbm_124024574287414=base_domain=.instagram.com; ds_user_id=8438207407; '
              'sessionid=8438207407%3AOSGm5mPgUiLYqW%3A19; csrftoken=JIqamHNQRJlbPXMsGxpbhk2KY0Vzmgn9; '
              'datr=JvuYYhqnj2y_1ysUAv5FQb95; '
              'shbid="10740\\0548438207407\\0541686922381'
              ':01f76e266bb173cf5894ff44fce9dc5f4cc3f5b9b154253229668bad9b161e861c77aa45"; '
              'shbts="1655386381\\0548438207407\\0541686922381'
              ':01f794891fec74b0577be9248cd6a0eeb74f51e2d1509b99272a221dbf19ab26580b2972"; '
              'rur="CLN\\0548438207407\\0541686922464'
              ':01f73872e1c3f5981901f7dfbca0ac06780406c66c75426cfb9969921427d0046018406e"; '
              'csrftoken=JIqamHNQRJlbPXMsGxpbhk2KY0Vzmgn9; ds_user_id=8438207407; '
              'ig_did=00BE72C3-CBC1-43BC-8619-38634F78E074; ig_nrcb=1; mid=Yf5GdwAEAAH3pj7rycxkj8mALiei; '
              'shbid="10740\\0548438207407\\0541686922052'
              ':01f73d7edd3c45331b08b183ac1ffa264dee328d00ad29f0297d741d935e7b10b04810ff"; '
              'shbts="1655386052\\0548438207407\\0541686922052'
              ':01f7805b8e599ed966171845f4bacceea6a828cda763d2c640766934a9417eac85b0dc6e" '
}


def get_status():
    response = requests.get(url, headers=headers)
    is_active = response.json()['user_presence']['38490942936']['is_active']
    timestamp = int(str(response.json()['user_presence']['38490942936']['last_activity_at_ms'])[:10])
    last_activity = datetime.fromtimestamp(timestamp).time()
    return is_active, last_activity


# 48936407918
is_still_offline = False
is_still_online = False

while True:
    status = get_status()

    if not status[0] and not is_still_offline:
        try:
            time_spent = f"{int(str(status[1]).split(':')[0]) - int(old_status[0]) * 60 + int(str(status[1]).split(':')[1]) - int(old_status[1])} minutes and {int(str(status[1]).split(':')[2]) - int(old_status[2])} seconds |"
            st.write("for", time_spent, status[1])
            is_still_offline = True
            is_still_online = False
        except Exception:
            print("Currently offline")
    elif status[0] and not is_still_online:
        st.write(status[1], '| Online')
        is_still_offline = False
        is_still_online = True
    old_status = str(status[1]).split(':')
    time.sleep(2)
