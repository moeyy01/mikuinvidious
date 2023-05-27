from bs4 import BeautifulSoup
from conf import always_pic_proxy

"""Format the result returned by cv link."""
def html_format_article(article_text):
	article_soup = BeautifulSoup(article_text, features='lxml')
	article_body = article_soup.find('div', id='read-article-holder')
	article_body.attrs = {}
	article_body['id'] = 'main-article'

	del_elems = []
	purge_elems = []
	for child in article_body.descendants:
		if not child.name:
			continue

		if child.name.startswith('h'):
			child.name = f'h{int(child.name[1:])+1}'

		if child.name == 'br' and child.parent.name != 'blockquote':
			del_elems.append(child)
			continue
		elif child.name == 'strong' and child.parent.name.startswith('h'):
			purge_elems.append(child.parent)

		if not hasattr(child, 'attrs'):
			continue

		if child.name == 'a':
			child['href'] = child['href'].split('//')[1].strip('www.bilibili.com')
			continue
		elif child.name == 'img':
			if always_pic_proxy:
				child['src'] = '/proxy/pic/http:' + child['data-src']
			else:
				child['src'] = child['data-src']
			del child['data-src']
			del child['data-size']
			continue
		elif child.name == 'span' and not child.parent in purge_elems:
			purge_elems.append(child.parent)
		
		child.attrs = {}

	for purge_elem in purge_elems:
		try:
			purge_elem.string = purge_elem.get_text()
		except:
			pass

	for del_elem in del_elems:
		try:
			del_elem.extract()
		except:
			pass

	return str(article_body)
