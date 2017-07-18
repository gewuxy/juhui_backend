var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var https = require('https');
var redis = require('redis');
var client = redis.createClient();
client.select(1, function(){});
var bodyParser = require('body-parser')
app.use( bodyParser.json() );       // to support JSON-encoded bodies
app.use(bodyParser.urlencoded({     // to support URL-encoded bodies
  extended: true
}));

var code = ""
app.get('/', function(req, res){
    //res.sendFile(__dirname + '/index.html');
    console.log('enter app.get / ')
    code = req.query.code;
    console.log(code);
    res.sendFile(__dirname + '/index.html');
});

app.post('/last_price/', function(req, res){
    console.log('enter last_price')
    data = req.body;
    console.log(data);
    io.emit('last_price', data);
    res.send("000000")
});
 
app.post('/send_msg/', function(req, res){
    console.log('enter send_msg');
    data = req.body;
    code = data.code;
    console.log('code: ' + code + 'data: ' + data);
    io.emit(code, data);
    client.publish('save_msg',JSON.stringify(data))
    res.send({'code': '000000', 'msg': 'SUCCESS', 'data': {}});
});

io.on('connection', function(socket){
    console.log('a user connected');
    code = socket.handshake.query.code;
    console.log('code is ' + code);
    // 推送人气数和自选数
    popularity_key = 'juhui_chat_popularity_' + code
    popularity_val = client.get(popularity_key)
    if (popularity_val){
        popularity_val = Number(popularity_val) + 1
    }else{
        popularity_val = 1
    }
    client.set(popularity_key, popularity_val);
    select_key = 'juhui_chat_select_' + code;
    select_val = client.get(select_key);
    if (select_val){
        select_val = Number(select_val);
    }else{
        select_val = 0;
    }
    popular_select_data = {'is_msg': '0', 'popularity': popularity_val, 'select': select_val};
    io.emit(code, popular_select_data);
    console.log('emit popular_select_data: ' + popular_select_data)
    
    socket.on(code, function(msg){
        msg['is_msg'] = '1'
        io.emit(code, msg);
        client.publish('save_msg', JSON.stringify(msg));
        console.log('message: ' + JSON.stringify(msg) + '===' + code + '====');
    });
    socket.on('disconnect', function(){
        console.log('user disconnected');
        io.emit(code, {'is_msg': '0', 'popularity': '-1', 'select': '0'});
    });
});

http.listen(8001, function(){
    console.log('listening on *:8001');
});
