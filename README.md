
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
   
 ```bash
$(py3.6 env) python setup.py install 
``` 
___
### **Description**
data 의 start point 에 따라 크게 두가지 기능으로 나누어짐.

##### **Spout** 
Kafka consumer. 
Kafka 로 부터 데이터를 받아서 pipeline 이 시작되는 형태   
- input 
    - kafka msg
- output
    - 실행시 입력받은 특정 폴더에 가공된 파일들을 생성
    
##### **Pipeline**
input, output 폴더를 입력값으로 받아서 동작하는 일반적인 형태
- input
    - 실행시 가공할 데이터가 있는 폴더를 input 으로 받음
- output
    - 실행시 받은 결과폴더에 가공된 파일들을 생성.

___
### **Feature**
작성중...
##### **Common**
```markdown

```
##### **Spout**
```markdown

```
##### **Pipeline**
```markdown

```    
___
### **Run**
##### **Spout** 
작성중...
```bash
...
```

##### **Pipeline**
작성중...
```bash
...
```
___

### **TODO**
작성중
