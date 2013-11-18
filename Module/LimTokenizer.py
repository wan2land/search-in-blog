# -*- coding:utf-8 -*-
# -*- coding:euc-kr -*-
import re

class LimTokenizer :
	@staticmethod
	def doit(text) :
		for word in text.split() :
			#print word
			word = re.sub('[^가-힣0-9a-zA-Z]+', '', word)
			
			if len(word) == 0 :
				continue
			if word.isspace() :
				continue	
			yield word
			
			#   word = re.sub('[~!@#$%^&*()_+{}|:\"<>?`-=[]\;\',./]+', '', word)
			

if __name__ == "__main__" :
	str = """	 "캘리"포★★니아 오''렌지"  %%  # '카'운티의' "뉴;포ⓘ트 비치,, 대나. ⓘ  good:-))		 많습니다.				굿 ^^			   비치 주 좋습니다.													영,,										   "큰바다로" 의 있습니다.	  * 찾아 가는길	   * 나의 생각	 "큰바다로" 떠나는 맛 난 여행은 편안함과 맛난 음식이 있는 곳을 소개합니다.		  """

	for token in LimTokenizer.doit(str) :
		print token
