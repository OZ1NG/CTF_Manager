# CTF Manager
> discord bot

## Introduce
ctftime.org의 rss 정보를 파싱하여 지정된 디스코드 텍스트 채널에 뿌려주는 봇입니다.

- 매 분마다 남은 시간 정보를 업데이트 해줍니다.  (사용자 지정 가능)
- 5분 마다 새로운 채널에 대한 정보를 가져옵니다. (사용자 지정 가능)

## Requirments
```
discord==2.1.0
requests==2.28.1
```

## How to usage
- 파싱 정보를 뿌릴 텍스트 채널은 텍스트 채널의 topic에 `#ctftime_P` 키워드가 존재하는 것으로 판단합니다. <br>따라서 미리 원하는 채널의 topic에 해당 키워드를 추가해야합니다.

```
sh ./run.sh
```

## Update
- 22.12.14 - first upload
