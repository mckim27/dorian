
# **Dorian**
News Text Data Pipeline Application

This application can be run in <a href="https://github.com/pachyderm/pachyderm" target="_blank">Pachyderm</a> or standalone.

![Code Language](https://img.shields.io/badge/python-3.7-blue.svg) ![Window Supported](https://img.shields.io/badge/windows-not%20supported-red.svg) ![build](https://img.shields.io/circleci/token/YOURTOKEN/project/github/RedSparr0w/node-csgo-parser/master.svg)
   
___
### **Requirements**

- Data Spout Feature
    - <a href="https://kafka.apache.org" target="_blank">Apache Kafka 2.2</a>

___
### **Installation**
    
#### Ionian requires :
    logzero>=1.5.0
    kafka-python>=1.4.6
    beautifulsoup4>=4.7.1
    fire>=0.1.3
    termcolor>=1.1.0
    pyfiglet>='0.8'
    colorama>='0.3.9'
 ```bash
$(py3.6 env) python setup.py install 
``` 
___
### **Description**
data 의 start point 에 따라 크게 두가지 기능으로 나누어짐.

##### **Spout** 
Kafka consumer. 
Kafka 로 부터 데이터를 받아서 pipeline 이 시작되는 형태   
- Data input 
    - kafka msg
- Data output
    - 실행시 입력받은 특정 폴더에 가공된 파일들을 생성
    
##### **Pipeline**
input, output 폴더를 입력값으로 받아서 동작하는 일반적인 형태
- Data input
    - 실행시 가공할 데이터가 있는 폴더를 input 으로 받음
- Data output
    - 실행시 받은 결과폴더에 가공된 파일들을 생성.

___
##### **Spout**
Run
- 'run' command 이전까지는 entry point 가 되는 python 파일의 param
    - broker_hosts : kafka broker hosts
    - group_id : kafka consumer 의 group id
    - topic_name : consume 할 topic 의 이름.
    - out_path : 결과 파일이 저장되어질 경로
    - print_banner : banner 출력 여부. 0 or 1
```bash
python spout.py --broker_hosts 192.168.0.31:9092 192.168.0.32:9092 \
    --topic_name=news_raw_contents --group_id=news_raw_contents_consumer \ 
    --out_path ./pfs/out 0 \
    run scrapper scrap-daumnews-article-contents file-save
```
    
##### **Pipeline**
Run
- 'run' command 이전까지는 entry point 가 되는 python 파일의 param
    - in_path : source file folder path
    - out_path : result file folder path
    - print_banner : banner 출력 여부. 0 or 1
```bash
python pipeline.py --in_path pfs/daum_news_raw_html --out_path pfs/out \
    --print_banner 0 \
    run scrapper scrap-daumnews-article-contents convert cleanse.cleanser.Cleanser text_length_validation remove_special_ch file_sav
```    
___
### **Function feature**
- news data 의 scrapping, cleansing 기능 
- 기본적으로 Module class 를 상속 받아서 기능을 구현.
- fire 이용하여 func chaining 방식으로 동작을 실행함. 
##### **Common**

- **file_save**
    - class 에 member 변수로 세팅되어 있는 data 에 file_name 과 contents 로 파일 저장. 

- **convert**
    - 다른 Module 로의 convert 기능.
    - func 연속적으로 호출시 다른 Module 로의 변경이 필요한 경우 사용. 
    - param 으로 변경할 class 의 full package 이름을 받음.
        - ex) cleanse.cleanser.Cleanser

##### **Scrapper**
- **scrap_daumnews_article_contents**
    - daum news html 데이터로 기사 본문의 text 를 scrapping

      
##### **Cleanser**
- **text_length_validation**
    - 특정 길이 이하의 text 인지 검사 아닐 경우 해당 data 사용안하게 하는 func.
    
- **remove_special_ch**
    - 한글과 '.', 한줄 개행을 제외한 나머지를 모두 없애는 func    