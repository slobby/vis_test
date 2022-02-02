const chai = require("chai");
const chaiHttp = require("chai-http");
const fs = require("fs");
const { expect } = chai;
const net = require("net");
const { kill } = require("process");
const path = require("path");

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

        var a = datas.split(";");

        console.log("*" + a[0]);
        fs.readFile(
          path.join(path.dirname(__filename), "convert_out.txt"),
          "utf-8",
          function (error, dat) {
            if (error) throw error;

            dat = dat.replace(" ", "");

            var k = dat.split(";");

            var client = net.connect({ port: 8888 }, function () {
              client.write(k[1] + " ");

              client.setTimeout(10000);
            });

            client.on("data", function (data) {
              var now = new Date().toLocaleString();
              fs.readFile(
                "D:/app/convert_in.txt",
                "utf-8",
                function (error, inf) {
                  if (error) throw error; // если возникла ошибка
                  inf = inf.replace(" ", "");

                  var b = inf.split(";");
                  if (a[1] === b[0]) {
                    try {
                      expect(data.toString("utf-8")).to.be.equal(b[1] + "\n");

                      fs.appendFile(
                        path.join(path.dirname(__filename), "t1_out.txt"),
                        "\n" + "[" + now + "] " + 'Тест "Команда 1" пройден',
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
                    } catch {
                      expect(data.toString("utf-8")).to.be.not.equal(
                        b[1] + "\n"
                      );

                      fs.appendFile(
                        path.join(path.dirname(__filename), "t1_out.txt"),
                        "\n" + "[" + now + "] " + 'Тест "Команда 1" НЕ пройден',
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
                    }
                  }

                  client.end();
                  done();
                }
              );
            });
          }
        );
      }
    );
  });
});
