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
    res.send({'code': '000000', 'msg': 'SUCCESS', 'data': {}});
});

io.on('connection', function(socket){
    code = socket.handshake.query.code
    console.log('query' + code)
    if (code === undefined) {
        console.log('非法请求');
        return;
    }
    console.log('a user connected' + '===' + code + '===');
    socket.on(code, function(msg){
        io.emit(code, msg);
        //client.set('nodejs_test', msg, redis.print)
        client.publish('save_msg', JSON.stringify(msg))
        //client.publish('save_msg', msg.toString('utf8'))
        console.log('message: ' + msg + '===' + code + '====');
    });
    socket.on('disconnect', function(){
        console.log('user disconnected');
    });
});

http.listen(8001, function(){
    console.log('listening on *:8001');
});
