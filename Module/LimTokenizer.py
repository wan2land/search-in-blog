# -*- coding:utf-8 -*-
import re
"""
FullText Module안에 들어있는 Standard Tokenizer를 대신할 수 있도록 만듦.
실제 문서에 너무 escape해야할 문자가 너무 많고 한글, 영어를 제외한 나머지는 처리할 필요 없도록 제작.
interface에서 요구하는 함수 자체가 doit()이었음. LimTokenizer.doit(text) 호출 시,
텍스트에서 토큰을 분리해서 이터레이터를 통해 하나씩 내보내 줌.
"""
class LimTokenizer :
	@staticmethod
	def doit(text) :
		for word in text.split() :
			#print word
			word = re.sub(r"[^가-힣0-9a-zA-Z]+", '', word)
			word = re.sub(r"\s+", '', word)

			#No-breaking space
			word = word.replace(chr(194)+chr(160), '')
			word = word.replace(chr(187)+chr(191), '')
			word = word.replace(chr(191)+chr(189), '')

			#word = word.replace(chr(189)+chr(141), '')
			#word = word.replace(chr(188)+chr(136), '')
			#word = word.replace(chr(188)+chr(137), '')
			#word = word.replace(chr(166)+chr(140), '')
			#word = word.replace(chr(164)+chr(179), '')
			#word = word.replace(chr(226)+chr(128)+chr(156), '')


			
			if len(word) < 2 :
				continue
			if word.isspace() :
				continue	

			yield word
			
def ords( text ) :
	result = ""
	for c in text :
		result = result + str(ord(c)) + ' / '
	return result

if __name__ == "__main__" :
	text = """     캘리포니아 오렌지 카운티의 뉴포트 비치, 대나 포인트와 함께 부촌으로 예술가들이 모여 사는 아름다운 도시입니다.                주차비가 비싼 뉴욕이나 시카고 와는 달리 캘리포니아는 대체적으로 저렴한 편인데, 이곳은 길거리에 코인이나 카드로 주차할곳이 많습니다.                           주변을 둘러보실때는 무료 셔틀 버스를 이용하시면 편리 합니다.  굿 ^^                       비치 주변으로 형성되어 있는 깨끗한 상가는 둘러보는 재미가 좋습니다.                                                                                                       비치가 한눈에 보이는 제일 좋은 자리의 식당, 항상 손님들로 붐비지만 역시 관광지의 식당답게 맛은 영,,                                                                                   "큰바다로" 의 미국 소개는 대부분 정확한 주소,대중교통,찾아가는 방법등을 알려 드립니다. 주소나 지도 부분을 클릭 하시면 구글의 더큰 지도등 상세한 정보를 볼수 있습니다.          * 찾아 가는길           * 나의 생각     엘에이 남부 오렌지 카운티의 부촌, 깨끗한 도시, 무료셔틀버스, 예술가들의 도시, 멋스런 동네를 둘러보다보면 마음까지 편안해지는 아름다운 비치가 있는 곳입니다.     * 관광지에서의 음식점 소개   관광지는 전망이 좋은 가장 좋은 자리가 대체적으로 장사가 잘되는 편인데 맛은 별로인곳이 많지요,, 하지만 사람들이 많이 찾아가는,, 또한 그곳을 여행한 블로거는 그 집을 소개하게 되고 또 다른 여행자나 블로거는 그집을 찾게되고 때로는 망설이다가도 먼곳을 찾아가 사진을 찍게되면 아까워 다시 소개하게 되는 그런 경우가 많은듯 합니다.   관광지에서의 식당소개는 조금은 더 신중하면 좋을듯 합니다. 조금은 중심을 벗어난 곳에 있는 제대로된 맛집을 찾는 재미도 좋습니다.   모두들 편안하고 행복한 하루 되세요^^       ** 여행은 설렘 "큰바다로" 떠나는 맛 난 여행은 편안함과 맛난 음식이 있는 곳을 소개합니다.              """
	for token in LimTokenizer.doit(text) :
		print token
		print ords(token)
