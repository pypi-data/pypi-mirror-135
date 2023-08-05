import http.client as httplib
import os
import random
from datetime import datetime
import websocket
import string
from threading import Thread
import json
import requests
from gsdbs.dbclient import GSDBS
from twisted.internet import task, reactor
from multiprocessing.dummy import Pool
import logging
import os.path

""" SockJS Client class  """


class MissionControl(Thread):

    def __init__(self, cnode, prefix, gsdbs, execute, heartbeatintervall=10):
        self._mandantname = ""
        self.counter = 0
        self.cnode = cnode
        self._gsdbs = gsdbs
        self._prefix = prefix
        self.execute = execute
        self.heartbeatintervall = heartbeatintervall * 1000
        self._pool = Pool(self._gsdbs.credentials["poolsize"])
        self._logger = logging.getLogger(__name__)
        Thread.__init__(self)
        self.connect()

    def connect(self):
        self.get_socket_info()
        self.start()

    def disconnect(self):
        pass

    def run(self):

        self._r1 = str(random.randint(0, 1000))
        self._conn_id = self.random_str(8)
        websocket.enableTrace(False)

        self._ws = websocket.WebSocketApp(
            ("ws://" if "localhost" in self._gsdbs.credentials["wshost"] else "wss://")
            + self._gsdbs.credentials["wshost"] + ":" + str(self._gsdbs.credentials["wsport"]) +
            self._prefix +
            "/" +
            self._r1 +
            "/" +
            self._conn_id +
            "/websocket?access_token=" +
            self._gsdbs.getAccessToken(),
            # on_cont_message=self.on_message,
            on_message=self.on_message,
            on_open=self.on_open,
            on_error=self.on_error,
            on_close=self.on_close)

        self._ws.run_forever()

    def get_socket_info(self):
        conn = 0
        try:
            if self._gsdbs.credentials["wsport"] == 8081:
                conn = httplib.HTTPConnection(self._gsdbs.credentials["wshost"], self._gsdbs.credentials["wsport"])
            else:
                conn = httplib.HTTPSConnection(self._gsdbs.credentials["wshost"], self._gsdbs.credentials["wsport"])

            self._logger.info(" Getting info from " + self._gsdbs.credentials["wshost"])
            conn.request('GET', self._prefix + '/info',
                         headers={"Authorization": "Bearer " + self._gsdbs.getAccessToken()
                                  # , "Origin": "https://glass-sphere-ai.de"
                                  }
                         )
            response = conn.getresponse()


        except  Exception as e:
            self._logger.exception(e)
        finally:
            if not conn: conn.close()

    def on_message(self, ws, message):
        # self.processMessage(message)
        self._pool.apply_async(self.processMessage, args=[message], callback=self.on_success,
                               error_callback=self.on_errorPost)

    def on_success(self, r):
        self._logger.info('message succeed')

    def on_errorPost(self, error):
        self._logger.exception('message failed :' + error)

    def processMessage(self, message):
        # sleep(0.05)

        if message == 'a["\\n"]':
            self._logger.info("beat:" + datetime.now().strftime("%H:%M:%S"))
            self._ws.send('["\\n"]')
            self.counter = self.counter + 1
            # if self.counter % self.heartbeatintervall == 0:
            self.ETHome()
            # self.counter = 0

        if message == "o":
            pass
        if message.startswith("a"):
            self._logger.info("Received Message")
            if "{" in message:
                try:

                    mssgbdy = json.loads(
                        message[message.find("{"):message.find("\\u0000")].replace("\\\"", "\"").replace("\\n",
                                                                                                         " ").replace(
                            "\\r", " ").replace("\\t", " "))
                    self.execute(self._gsdbs, mssgbdy, self.onNext)

                    if "isCommand" not in mssgbdy:
                        if self.str2bool(mssgbdy["isComputingStep"]) and mssgbdy["computingstep"] != '':
                            self.markJobAsDone(mssgbdy["jobid"], mssgbdy["groupid"], mssgbdy["computingstep"])
                except Exception as e:
                    self._logger.exception("JobFailed" + str(e))
                    self.markJobAsFailed(mssgbdy["jobid"])

        else:

            pass

    def str2bool(self, v):
        return v.lower() in ("yes", "true", "t", "1")

    def call_api(self, transactionid, send):
        x = 16388
        res = [send[y - x:y] for y in range(x, len(send) + x, x)]
        for x in res:
            self._ws.send("[\"" + x + "\"]")

    def on_success(self, r):
        self._logger.info('Post succeed')

    def on_errorPost(self, error):
        self._logger.info('Post requests failed')

    def onNext(self, target, json1, data):
        try:
            data["mandantname"] = self._mandantname

            url = "http://" + self._gsdbs.credentials["wshost"] + ":" + str(
                self._gsdbs.credentials["wsport"]) + "/missioncontrol/onnext"
            json2 = {"jobid": json1["jobid"], "groupid": json1["groupid"],
                     "accesstoken": self._gsdbs.getAccessToken(),
                     "computingstep": json1["computingstep"],
                     "target": target,
                     "cnode": self.cnode,
                     "data": data}
            headers = {"Content-Type": "application/json",
                       "Authorization": "Bearer " + self._gsdbs.getAccessToken()}

            datastring = json.dumps(json2).replace("\"", "\'")

            transactionid = 'tx-' + self.random_str(8)
            send = 'SEND\\n' \
                   'destination:/queue/onnext\\n' \
                   'durable:false\\n' \
                   'exclusive:false\\n' \
                   'auto-delete:false\\n\\n' \
                   + datastring + '\\u0000'
            self.call_api(transactionid, send)

        except Exception as e:
            return e

    def utf8len(self, s):

        encoded_string = s.encode('utf-8')
        byte_array = bytearray(s)

        return len(s.encode('utf-8'))

    def on_error(self, ws, error):
        self._logger.exception(error)

    def on_close(self, ws, close_status_code, close_msg):
        self._logger.exception(
            "### closed: Code->" + close_status_code + "Message:" + close_msg + ":" + datetime.now().strftime(
                "%H:%M:%S") + "###")

    def on_open(self, ws):
        connect = '\"CONNECT\\naccept-version:1.2,1.0\\nheart-beat:' + str(self.heartbeatintervall) + ',' + str(
            self.heartbeatintervall) + '\\nprefetch-count:1\\nauto-delete:true\\nexclusive:true\\nx-single-active-consumer:true\\n\\n\\u0000\"'
        self._ws.send("[" + connect + "]")
        sub = f'\"SUBSCRIBE\\nid:{self.random_str(4)}\\ndestination:/queue/{self.getQueue()}\\n\\n\\u0000\"'
        # sub = f'\"SUBSCRIBE\\nid:{self.random_str(4)}\\ndestination:/queue/detector\\n\\n\\u0000\"'
        self._ws.send("[" + sub + "]")
        self.ETHome()
        self._logger.info("open:" + datetime.now().strftime("%H:%M:%S"))

    def ETHome(self):
        headers = {'Authorization': 'Bearer ' + self._gsdbs.getAccessToken()}
        protokoll = "https://"
        if "localhost" in self._gsdbs.credentials["wshost"]:
            protokoll = "http://"
        resp = requests.get(protokoll + self._gsdbs.credentials["wshost"] + ":" + str(
            self._gsdbs.credentials["wsport"]) + "/missioncontrol/register",
                            headers=headers)
        resp.raise_for_status()
        self._gsdbs.executeStatement(f"""
                                        mutation{{
                                          addDTable(
                                            dtablename:"cnode",
                                            superDTable:DTABLE,
                                            sriBuildInfo:"${{cnode}}",
                                            dataLinks:[
                                              {{alias:"cnode",locale:DE,superPropertyURI:DYNAMIC_DATALINK,DataType:STRING}}
                                              {{alias:"desciption",locale:DE,superPropertyURI:DYNAMIC_DATALINK,DataType:STRING}}
                                            ]
                                            data:[
                                              ["cnode","desciption"],
                                              ["{self.cnode}","desciption"]
                                            ]
                                          )
                                        }}
                                        """)

    def getQueue(self):
        headers = {'Authorization': 'Bearer ' + self._gsdbs.getAccessToken()}
        try:
            resp = requests.get(self._gsdbs.credentials['userinfourl'], headers=headers)
            resp.raise_for_status()
            userinfo = resp.json()
            self._mandantname = userinfo["mandant"]["mandantName"]
            return userinfo["mandant"]["mandantName"] + "-" + self.cnode  # + "-" + self._conn_id
        except:
            return ""

    def random_str(self, length):
        letters = string.ascii_lowercase + string.digits
        return ''.join(random.choice(letters) for c in range(length))

    def markJobAsDone(self, jobid, groupid, computingstep):

        json2 = {"jobid": jobid, "groupid": groupid, "accesstoken": self._gsdbs.getAccessToken(),
                 "computingstep": computingstep, "cnode": self.cnode}
        datastring = json.dumps(json2).replace("\"", "\\\"")

        transactionid = 'tx-' + self.random_str(8)
        send = 'SEND\\ndestination:/queue/onnotify\\ndurable:false\\nexclusive:false\\nauto-delete:false\\n\\n' + datastring + '\\u0000'
        self.call_api(transactionid, send)

        self._logger.info("job done")

    def markJobAsFailed(self, jobid):
        self._gsdbs.executeStatement(f"""
                mutation{{
                        updateDTable(
                  dtablename:"gsasyncjob",
                   where: [
                      {{connective: BLANK, column: gsasyncjob_jobid, operator: EQUAL, value: "{jobid}"}}
                        {{connective: AND, column: gsasyncjob_cnode, operator: EQUAL, value: "{self.cnode}"}}
                  ],
                  updatelist:[
                    {{datalink:gsasyncjob_jobstatus,value:"failed"}}
                  ]
                )
                }}
            """)


class MissionControlClient:

    def __init__(self, execute, gsdbspath=os.path.dirname(os.path.realpath(__file__)), logginglevel=logging.WARNING,
                 initmethod=None):
        self.execute = execute
        self.gsdbs = GSDBS(gsdbspath)
        self.cnode = self.gsdbs.credentials["cnode"]
        self.client = None
        self.logginglevel = self.gsdbs.credentials["logginglevel"]
        if initmethod is not None:
            self.initMethod = initmethod
        self.init()

    def createClient(self):
        self.client = MissionControl(self.cnode,
                                     '/gs-guide-websocket',
                                     self.gsdbs,
                                     self.execute,
                                     60)

    def checkThreadRunning(self):
        if self.client is None or not self.client.is_alive():
            reactor.callFromThread(self.createClient)

    def init(self):
        logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=self.logginglevel)
        if self.initMethod is not None:
            self.initMethod(self.gsdbs)

        l = task.LoopingCall(self.checkThreadRunning)
        l.start(1.0)
        reactor.run()
