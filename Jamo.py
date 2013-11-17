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

def divText( text ) :
	result = []
	for character in text :
		items = divHangul(character)
		for item in items:
			if (item is not None) :
				result.append(item)

	return result

if __name__ == "__main__" :

	while(1) :
		text = raw_input("Input : ").decode("utf-8")
		result = divText( text )
		print "".join(result)

