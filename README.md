# Access_log_ana
概要
Apache HTTP サーバのアクセスログを解析するプログラム

## 詳細
通常、Apache のアクセスログは、以下の形式で
/var/log/httpd/access_log ファイルに出力される。
%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"
それぞれの項目の意味は以下のとおりである。
- %h    リモートホスト名
- %l    クライアントの識別子
- %u    認証ユーザー名
- %t    リクエストを受信した時刻([day/month/year:hour:minute:second zone]の書式)
- %r    リクエストの最初の行
- %>s   最後のレスポンスのステータス
- %b    HTTPヘッダを除くレスポンスのバイト数。0バイトの場合は「-」と表示される
- %{Referer}i    サーバが受信したリクエストヘッダのReferer
- %{User-Agent}i サーバが受信したリクエストヘッダのUser-Agent

---アクセスログの例---
10.2.3.4 - - [18/Apr/2005:00:10:47 +0900] "GET / HTTP/1.1" 200 854 "-" "Mozilla/4.0 (compatible; MSIE 5.5; Windows 98)"
10.2.3.4 - - [18/Apr/2005:00:10:47 +0900] "GET /style.css HTTP/1.1" 200 102 "http://www.geekpage.jp/" "Mozilla/4.0 (compatible; MSIE 5.5; Windows 98)"
10.2.3.4 - - [18/Apr/2005:00:10:47 +0900] "GET /img/title.png HTTP/1.1" 304 - "http://www.geekpage.jp/" "Mozilla/4.0 (compatible; MSIE 5.5; Windows 98)"
## 使用方法
https://github.com/Hina1008/Task/issues/2#issue-594801044

引数に、アクセスログファイルのパス指定して実行(複数可)
その後、期間を指定。
時間帯毎にアクセス数の多いリモートホストの順にアクセス件数の一覧を表示する

## 実行結果例
https://github.com/Hina1008/Task/issues/4#issue-594804637

## 使用外部ライブラリ
numpy                 1.16.4 
pandas                0.25.1 
