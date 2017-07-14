var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var https = require('https');
var redis = require('redis');
var client = redis.createClient();
client.select(1, function(){});

var code = ""
app.get('/', function(req, res){
    //res.sendFile(__dirname + '/index.html');
    code = req.query.code;
    console.log(code);
    /***
    var url = 'https://jh.qiuxiaokun.com/api/chat/comment/?count=2&code=' + code
    var datas = "";
    https.get(url, (res1) => {
        console.log('statusCode: ' + res1.statusCode);
        console.log('headers: ' + res1.headers);

        res1.on('data', (d) => {
            console.log('data: ' + d + 'url: ' + url);
            //process.stdout.write(d);
            global.returnData = d
        });
    }).on('error', (e) => {
       console.error(e);
   });
   console.log('====datas===');
   console.log(global.returnData);
   res.send(global.returnData);
   ***/
   //res.send({});
   res.sendFile(__dirname + '/index.html');
});

app.get('/last_price/', function(req, res){
    //res.sendFile(__dirname + '/index.html');
    code = req.query.code;
    price = req.query.price;
    time = req.query.time
    console.log(code);
    console.log(price);
    io.emit('last_price', {'code': code, 'price': price, 'time': time});
    res.send("000000")
});
 
/***
var code = "";
app.get('/', function(req, res){
    code = req.query.code;
    res.send({})
    //res.sendFile(__dirname + '/index.html');
});
***/

io.on('connection', function(socket){
    console.log('a user connected');
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
