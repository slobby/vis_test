const chai = require("chai");
const chaiHttp = require("chai-http");
const fs = require("fs");
//let server = require('./src/api');
const { expect } = chai;
const net = require("net");
const { kill } = require("process");

chai.use(chaiHttp);
chai.should();

fs.open("D:/app/t1_log.txt", (err, fd) => {
  if (err) throw err;
  console.log("File t1_log.txt created");
});

fs.open("D:/app/t1_out.txt", (err, fd) => {
  if (err) throw err;
  console.log("File t1_out.txt created");
});

describe("Проверка выполнения команд", function () {
  it("Команда 1", function (done) {
    fs.readFile(
      path.join(path.dirname(__filename), "t1_exp.txt"),
      "utf-8",
      function (error, datas) {
        if (error) throw error; // если возникла ошибка
        datas = datas.replace(" ", "");
        console.log(datas);
        var str = datas.split("\r\n");
        console.log(str); // выводим считанные данные
        for (j = 0; j < str.length; j++) {
          var a = str[j].split(";");
          console.log("*" + a[0]);
          fs.readFile(
            path.join(path.dirname(__filename), "convert_out.txt"),
            "utf-8",
            function (error, dat) {
              if (error) throw error;

              dat = dat.replace(" ", "");
              console.log(dat);
              var str1 = dat.toString("utf-8").split("\r\n");
              console.log(str1);
              a: for (i = 0; i < str1.length; i++) {
                var k = str1[i].split(";");
                console.log("*" + k[0] + k[0].length);
                console.log("_" + a[0] + k[0].length);

                if (a[0] === k[0]) {
                  var client = net.connect({ port: 8888 }, function () {
                    console.log(k[1]);
                    client.write(k[1] + " ");

                    client.setTimeout(10000);
                  });
                }

                client.on("data", function (data) {
                  var now = new Date().toLocaleString();
                  fs.readFile(
                    path.join(path.dirname(__filename), "convert_in.txt"),
                    "utf-8",
                    function (error, inf) {
                      if (error) throw error; // если возникла ошибка
                      inf = inf.replace(" ", "");
                      var str2 = inf.toString("utf-8").split("\r\n");
                      b: for (e = 0; e < str2.length; e++) {
                        var b = str2[e].split(";");
                        console.log["-" + b[0]];
                        if (
                          a[1] === b[0] &&
                          expect(data.toString("utf-8")).to.be.equal(
                            b[1] + "\n"
                          )
                        ) {
                          try {
                            // console.log(data.toString('utf-8'));
                            // console.log(str[1].toString('utf-8'));
                            //fs.readFile('D:/app/convert_in.txt', 'utf-8',  function(error,inf){
                            //   if(error) throw error; // если возникла ошибка
                            //   inf = inf.replace(' ','');
                            //   var f = inf.split(';')  // перебор по файлу с полученными значениями
                            //for (i in f )
                            //{

                            //var i = i.split(';');
                            //var j = i[0].split(';');

                            //expect(data.toString('utf-8')).to.be.equal(b[1]+'\n')

                            // if(a[1]===b[0] && expect(data.toString('utf-8')).to.be.equal(b[1]+'\n')){
                            //expect(data.toString('utf-8')).to.be.equal(b[1]+'\n')

                            fs.appendFile(
                              path.join(path.dirname(__filename), "t1_out.txt"),
                              "\n" +
                                "[" +
                                now +
                                "] " +
                                'Тест "Команда 1" пройден',
                              (err) => {
                                if (err) throw err;
                              }
                            );

                            fs.appendFile(
                              path.join(path.dirname(__filename), "t1_log.txt"),
                              "[" +
                                now +
                                "] " +
                                "отправили: " +
                                k[1] +
                                "\tполучили: " +
                                data.toString(),
                              "utf-8",
                              (err) => {
                                if (err) throw err;
                              }
                            );

                            //else continue b;

                            //
                          } catch {
                            expect(data.toString("utf-8")).to.be.not.equal(
                              b[1] + "\n"
                            );

                            fs.appendFile(
                              path.join(path.dirname(__filename), "t1_out.txt"),
                              "\n" +
                                "[" +
                                now +
                                "] " +
                                'Тест "Команда 1" НЕ пройден',
                              (err) => {
                                if (err) throw err;
                              }
                            );

                            fs.appendFile(
                              path.join(path.dirname(__filename), "t1_log.txt"),
                              "[" +
                                now +
                                "] " +
                                "отправили: " +
                                k[1] +
                                "\tполучили: " +
                                data.toString(),
                              "utf-8",
                              (err) => {
                                if (err) throw err;
                              }
                            );

                            //}

                            // expect(data.toString('utf-8')).to.be.not.equal(f[1]+'\n');
                            // //expect(data.toString('utf-8')).to.not.eql(a+'\n')
                            // fs.appendFile('D:/app/t1_out.txt','\n'+'['+ now + '] '+'Тест "Команда 1" НЕ пройден', (err) => {
                            // if (err) throw err })

                            // fs.appendFile('D:/app/t1_log.txt','['+ now + '] '+ 'отправили: ' + c[1] + '\tполучили: ' + data.toString(),'utf-8',(err) => {
                            //     if (err) throw err });
                          }

                          //}
                        } else continue b;
                        //}
                      }

                      client.end();
                      done();
                    }
                  );
                });
              }
            }
          );
        }
      }
    );
  });
});
// it('Команда 2', function (done) {

//     var client = net.connect({ port: 8888 },
//         function() {
//             client.write('Enter the command number  ');
//         }
//     );

//     client.on('data', function(data) {

//         const a = '2';
//         try{
//             expect(data.toString('utf-8')).to.be.eql(a+'\n')
//             fs.appendFile('D:/app/Test2.txt','\nТест "Команда 2" пройден', (err) => {
//          if (err) throw err });
//          fs.appendFile('D:/app/Test.txt', a + '-' + data.toString(),'utf-8',(err) => {
//             if (err) throw err });
//             //console.log(`jhjhj'${data}`);

//          }
//          catch {
//              //expect(data.toString('utf-8')).to.not.eql(a+'\n')
//              fs.appendFile('D:/app/Test2.txt','\nТест "Команда 2" не пройден', (err) => {
//              if (err) throw err })

//          }

//         //  fs.appendFile('D:/app/Test.txt', a + '-' + data.toString(),'utf-8',(err) => {
//         //  if (err) throw err });
//         //  //console.log(`jhjhj'${data}`);
//         //  client.end();
//         //  done();

//         client.end();
//         done()

//         // if (expect(data.toString('utf-8')).to.be.eql(a+'\n')){
//         //     fs.appendFile('D:/app/Test2.txt','\nТест "Команда 2" пройден', (err) => {
//         //         if (err) throw err });

//         // }
//         // else if(expect(data.toString('utf-8')).to.not.eql(a+'\n')){
//         //     fs.appendFile('D:/app/Test2.txt','\nТест "Команда 2" не пройден', (err) => {
//         //     if (err) throw err })

//         // }

//         // fs.appendFile('D:/app/Test.txt', a + '-' + data.toString(),'utf-8',(err) => {
//         // if (err) throw err });
//         // //console.log(`jhjhj'${data}`);
//         // client.end();
//         // done();

//     });

//done();

// });
