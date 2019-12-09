# Описание
Клиент Telegram, которым можно управлять через POST-запросы. В данный момент реализована только отправка текстовых сообщений, при необходимости функциональность легко расширяется (см. документацию к Telethon).

# Сценарии использования
- сохранять из браузера интересные статьи для последующего удобного прочтения через Instant View (получается такой аналог Pocket). Instant View для любых статей делают боты @chotamreaderbot, @CorsaBot и др. Для удобной отправки ссылок ботам было написано расширение для браузера ([Firefox](https://addons.mozilla.org/en-US/firefox/addon/instant-view/)).
- одним кликом отправлять из браузера текст в Saved Messages (или любой другой чат). Например, через такой букмарклет:

```javascript
(
    function () {
        ba = 'http://yourbackend.example.com:8080'
        ch = 'me'
        d = document;
        b = d.body;
        var u = 'chat='+ch+'&text={searchTerms}';
        var x = new XMLHttpRequest();
        x.open("POST", ba, false);
        x.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        x.send(u);
        if (x.status != 200) {
            msg = '⚠️ ' + x.status + ': ' + x.statusText;
            bg = 'rgba(255, 136, 89, 0.7)';
        } else {
            msg = '✔️ Сохранено';
            bg = 'rgba(151, 225, 76, 0.7)'
        }
        k = d.createElement('style');
        k.textContent = '@keyframes showtgpopup{from{top:-35px;}to{top:0px;}}';
        b.appendChild(k);
        b.innerHTML = '<DIV id="tgsendpopup" style="z-index:99999;display:flex;justify-content:center;align-items:center;height:35px;top:-100px;width:100%;position:fixed;background-color:' + bg + ';font-size:16px;font-family:Verdana;animation:showtgpopup 1s;">' + msg + '</DIV>' + b.innerHTML;
    })();
```
В переменных ba и ch соответственно URL развернутого приложения и ID чата назначения (me означает Saved Mesages, оно же Избранное). Код минифицировать и запускать через расширение [SPC](https://addons.mozilla.org/en-US/firefox/addon/searchfrompopuporcontextmenu/) (Firefox).

- любая другая автоматизация, для которой не хватает возможностей Bot API

# Запросы
Параметры POST-запроса:

`chat` — username чата, либо его ID (при использовании ID дополнительно еще нужно указать тип чата в `chattype`)

`chattype` — channel, user или chat (например, супергруппа — это channel). Необязательный параметр.

`text` — текст сообщения.

`delete` — 0 или 1. Удалять сообщение сразу после отправки (удобно для ботов, чтобы в диалоге не было лишних сообщений). Необязательный параметр.

# Развертывание
- Получить api_id и api_hash для приложения на https://my.telegram.org
- С помощью фреймворка Telethon произвести аутентификацию на сервере Telegram, сохранить string session. См.: https://telethon.readthedocs.io/en/latest/concepts/sessions.html#string-sessions
- Отредактировать `config.py`, вписав в него значения, полученные на предыдущих шагах
- Развернуть, используя Dockerfile