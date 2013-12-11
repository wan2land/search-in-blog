# Search'n Blog Library

파이썬을 기본으로 하였으며, MySQL을 활용하여 쉽게 FullText를 사용하도록 만든 라이브러리입니다. 기본 MySQL에 Fulltext기능이 내장되어 있으나 성능 부분이 조금 미흡하고, 기능도 제한이 있어 하나 제작하게 되었습니다.

## Dependencies

다음과 같은 라이브러리가 사용되었습니다.

- Python MySQLdb
- Python Shapely

또한 위 라이브러리 중 Shapely를 사용할때 컴퓨터에서 다음 요구사항이 필요할 수 있습니다.

- 맥의 경우 brew install geos
- 리눅스의 경우 sudo apt-get install libgeos-dev

웹을 테스트 해보고 싶다면 다음과 같은 추가 라이브러리가 필요합니다.

- flask (Web Library)

또한, Module.FullText.py 를 수행하고자 할땐 다음과 같은 라이브러리가 추가로 필요합니다.

- Tkinter (GUI Library)


## 실행

그냥 간단한 테스트는 config/snb.json 파일을 설정(config/SAMPLE 참고)하시고, ```python Main.py```를 실행하시면 됩니다. 원격 접속하는 데이터베이스에는 원격 접근을 허용해주어야 합니다.(MySQL은 127.0.0.1의 접근만을 허용하고 있습니다.)

### 상세한 테스트 및 벤치마크 보기

마찬가지로 ```config/snb.json```, ```config/onlyone.json``` 파일 수정 하시고 ```python Test.py```를 실행하면 됩니다. 여기서는 상세한 옵션이 있는데 자세한 내용은 Test.py 파일 내부 주석을 확인하시기 바랍니다.

### 웹테스트

이 부분은 해당 라이브러리를 어떻게 활용가능한지에 대한 테스트입니다. 기존 python flask에 대한 이해가 있어야 합니다.

```python WebMain.py``` 실행하면 *localhost:5000*를 통해서 웹으로 접근이 가능합니다. ```config/web.json```을 사용합니다.

## 기타..

제대로 완성하지 못한 프로젝트지만 혹시 문의사항 있으면 me@wani.kr로 남겨주시면 항상 답변해드리도록 하겠습니다. :)