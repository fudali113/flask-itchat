# -*- coding: UTF-8 -*- 
import itchat
import logging
from flask import Flask, jsonify, send_file, request, render_template, url_for, redirect

app = Flask(__name__)
logger = logging.getLogger('app')

mychat = mychat = itchat.Core()

@app.route("/", methods=['GET'])
def index():
    return redirect('static/index.html')


@app.route('/qr', methods=['GET'])
def get_QR():
    mychat.get_QRuuid()
    logger.info("----", mychat.uuid)
    qr_io = mychat.get_QR(enableCmdQR=2)
    qr_io.seek(0)
    return send_file(qr_io, mimetype='image/png')


@app.route('/login', methods=['GET'])
def get_isLogging():
    logger.info("----", mychat.uuid)
    if not mychat.uuid:
        return jsonify({'error': 'please request /qr and scan QR'})
    status = mychat.check_login()
    if status == '200':
        isLoggedIn = True
    elif status == '201':
        return jsonify({'error': 'Please press confirm on your phone.'})
    elif status == '408':
        return jsonify({'error': 'please request /qr and scan QR', 'status': status})
    mychat.web_init()
    mychat.show_mobile_login()
    mychat.get_contact(True)
    mychat.start_receiving()
    return jsonify({'isLoggin': mychat.alive})


@app.route('/send', methods=['POST'])
def sendMsg():
    if not mychat.alive:
        return jsonify({'error': '请先登录'})
    json = request.json
    return jsonify(mychat.send(json[u'message'], findUserByName(mychat, json[u'name'])))

@app.route('/send-group', methods=['POST'])
def sendGroupMsg():
    if not mychat.alive:
        return jsonify({'error': '请先登录'})
    json = request.json
    return jsonify(mychat.send(json[u'message'], findGroupUserByName(mychat,json[u'name'])))


def findGroupUserByName(mychat, name):
    users = mychat.search_chatrooms(name=name)
    return users[0]['UserName']

def findUserByName(mychat, name):
    users = mychat.search_friends(name=name)
    return users[0]['UserName']


if __name__ == '__main__':
    app.run()
