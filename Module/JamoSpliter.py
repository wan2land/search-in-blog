# -*- coding:utf-8 -*-

#130813 아직 미완성
jaum = [unichr(i) for i in range(12593, 12623)]
moum = [unichr(i) for i in range(12623, 12644)]

c1 = [x.decode("utf-8") for x in "ㄱ,ㄲ,ㄴ,ㄷ,ㄸ,ㄹ,ㅁ,ㅂ,ㅃ,ㅅ,ㅆ,ㅇ,ㅈ,ㅉ,ㅊ,ㅋ,ㅌ,ㅍ,ㅎ,".split(',')]
c2 = [x.decode("utf-8") for x in "ㅏ,ㅐ,ㅑ,ㅒ,ㅓ,ㅔ,ㅕ,ㅖ,ㅗ,ㅘ,ㅙ,ㅚ,ㅛ,ㅜ,ㅝ,ㅞ,ㅟ,ㅠ,ㅡ,ㅢ,ㅣ,".split(',')]
c3 = [x.decode("utf-8") for x in " ,ㄱ,ㄲ,ㄳ,ㄴ,ㄵ,ㄶ,ㄷ,ㄹ,ㄺ,ㄻ,ㄼ,ㄽ,ㄾ,ㄿ,ㅀ,ㅁ,ㅂ,ㅄ,ㅅ,ㅆ,ㅇ,ㅈ,ㅊ,ㅋ,ㅌ,ㅍ,ㅎ,".split(',')]
c4 = [x.decode("utf-8") for x in "ㄱ,ㄲ,ㄳ,ㄴ,ㄵ,ㄶ,ㄷ,ㄸ,ㄹ,ㄺ,ㄻ,ㄼ,ㄽ,ㄾ,ㄿ,ㅀ,ㅁ,ㅂ,ㅃ,ㅄ,ㅅ,ㅆ,ㅇ,ㅈ,ㅉ,ㅊ,ㅋ,ㅌ,ㅍ,ㅎ,".split(',')]

l1 = 20 #( len(c1)+2 )/3
l2 = 21 #( len(c2) )/3 #(생략불가)
l3 = 28 #( len(c3) )/3

char_map = {
	'ㄱ':'r','ㄲ':'R','ㄴ':'s','ㄷ':'e','ㄸ':'E','ㄹ':'f','ㅁ':'a','ㅂ':'q','ㅃ':'Q','ㅅ':'t','ㅆ':'T','ㅇ':'d','ㅈ':'w','ㅉ':'W','ㅊ':'c','ㅋ':'z','ㅌ':'x','ㅍ':'v','ㅎ':'g',
	'ㅏ':'k','ㅐ':'o','ㅑ':'i','ㅒ':'O','ㅓ':'j','ㅔ':'p','ㅕ':'u','ㅖ':'P','ㅗ':'h','ㅘ':'hk','ㅙ':'ho','ㅚ':'hl','ㅛ':'y','ㅜ':'n','ㅝ':'nj','ㅞ':'np','ㅟ':'nl','ㅠ':'b','ㅡ':'m','ㅢ':'ml','ㅣ':'l',
	'ㄱ':'r','ㄲ':'R','ㄳ':'rt','ㄴ':'s','ㄵ':'sw','ㄶ':'sg','ㄷ':'e','ㄸ':'E','ㄹ':'f','ㄺ':'fr','ㄻ':'fa','ㄼ':'fq','ㄽ':'ft','ㄾ':'fx','ㄿ':'fv','ㅀ':'fg','ㅁ':'a','ㅂ':'q','ㅃ':'Q','ㅄ':'qt','ㅅ':'t','ㅆ':'T','ㅇ':'d','ㅈ':'w','ㅉ':'W','ㅊ':'c','ㅋ':'z','ㅌ':'x','ㅍ':'v','ㅎ':'g'
}


def divHangul(ch):
	val = ord(ch) # 44032 in utf-8
	if 44032 <= val and val < 55204:
		value = val - 44032    # 0xD544  - 0xAC00 = 10564
		z	=	value % l3 
		y	= (	value / l3 ) % l2 
		x	= (	value / l3 / l2 ) % l1
		if z == 0 :
			return	(c1[x], c2[y], None)
		else :
			return	(c1[x], c2[y], c3[z])

	elif 12593 <= val and val < 12623:
		return (c4[val-12593], None, None)

	elif 12623 <= val and val < 12644:
		return (c2[val-12623], None, None)

	else:
		return (ch, None, None)

def doit( text ) :
	if isinstance( text, str ) :
		text = text.decode('utf-8')

	# isinstance( text, unicode ) # is True

	result = []
	for character in text :
		items = divHangul(character)
		for item in items:
			if (item is not None) :
				if item.encode('utf-8') in char_map.keys() :
					item = char_map[item.encode('utf-8')]
				result.append( item )



	return ''.join(result)

if __name__ == "__main__" :

	text = "한글은 이렇게 처리됩니다."
	compare = "gksrmfdms dlfjgrp cjflehlqslek."
	result = doit( text )

	print result == compare

