# /* bbapi.py
#  * Copyright (C) 2023 MikuInvidious Team
#  *
#  * This software is free software; you can redistribute it and/or
#  * modify it under the terms of the GNU General Public License as
#  * published by the Free Software Foundation; either version 3 of
#  * the License, or (at your option) any later version.
#  *
#  * This software is distributed in the hope that it will be useful,
#  * but WITHOUT ANY WARRANTY; without even the implied warranty of
#  * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  * General Public License for more details.
#  *
#  * You should have received a copy of the GNU General Public License
#  * along with this library. If not, see <http://www.gnu.org/licenses/>.
#  */

import requests

from conf import cookies
from vidconv import bv2av

# FBI WARNING: DONT TRY TO VISIT IT
default_bvid = 'BV1GJ411x7h7'

safe_headers = {
	'Referer': 'https://www.bilibili.com',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
}

sess_ok = False
sess = requests.Session()
sess.headers.update(safe_headers)
sess.cookies.update(cookies)

"""Get video info from BVid"""
def bbapi_info_from_bvid(bvid = default_bvid):
	req = requests.get('http://api.bilibili.com/x/web-interface/view',
	                   params = { 'bvid': bvid },
	                   headers = safe_headers)
	return req.json()

"""Get subvideos from BVid"""
def bbapi_subvid_from_bvid(bvid = default_bvid):
	req = requests.get('http://api.bilibili.com/x/player/pagelist',
	                   params = { 'bvid': bvid },
	                   headers = safe_headers)
	return req.json()

"""Get video source from BVid"""
def bbapi_src_from_bvid(cid, bvid = default_bvid, quality = 16):
	req = requests.get(f'http://api.bilibili.com/x/player/playurl',
	                   params = { 'bvid': bvid, 'cid': cid, 'qn': quality },
	                   cookies = cookies,
	                   headers = safe_headers)
	return req.json()

"""Get video recommendation from BVid"""
def bbapi_related_from_bvid(bvid = default_bvid):
	req = requests.get('http://api.bilibili.com/x/web-interface/archive/related',
	                   params = { 'bvid': bvid },
	                   headers = safe_headers)
	return req.json()

"""Get video comments from BVid"""
def bbapi_cum_from_bvid(bvid = default_bvid):
	data = { 'type': 1, 'oid': bv2av(bvid), 'sort': 1 }
	req = requests.get('http://api.bilibili.com/x/v2/reply',
	                   params = data,
	                   headers = safe_headers)
	return req.json()

"""Get members' videos from mid with paging"""
def bbapi_vids_from_mid_paging(mid, page_num = 1, page_count = 25):
	req = requests.get('http://api.bilibili.com/x/space/wbi/arc/search',
	                   params = { 'mid': mid, 'pn': page_num, 'ps': page_count },
	                   headers = safe_headers)
	return req.json()

"""Get userinfo from mid"""
def bbapi_uinfo_from_mid(mid):
	req = requests.get('http://api.bilibili.com/x/space/wbi/acc/info',
	                   params = { 'mid': mid },
	                   headers = safe_headers)
	return req.json()

"""Get user card from mid"""
def bbapi_ucard_from_mid(mid):
	req = requests.get('http://api.bilibili.com/x/web-interface/card',
	                   params = { 'mid': mid, 'photo': False },
	                   headers = safe_headers)
	return req.json()

"""Search videos from kward"""
def bbapi_vids_from_kward(kward, pn = 1):
	global sess_ok
	if not sess_ok:
		sess.get('https://www.bilibili.com')
		sess_ok = True

	sparams = {
		'search_type': 'video',
		'keyword': kward,
		'order': 'totalrank',
		'duration': 0,
		'tids': 0,
		'page': pn,
	}

	req = sess.get('http://api.bilibili.com/x/web-interface/search/type',
	               params = sparams,
				   headers = safe_headers)
	return req.json()

"""Get basic infomation about a CV"""
def bbapi_info_from_cv(cv):
	req = requests.get('http://api.bilibili.com/x/article/viewinfo',
	                   params = { 'id': cv },
	                   headers = safe_headers)
	return req.json()