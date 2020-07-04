from flask import Flask, render_template, request, Response, send_file, Markup, session, redirect, abort
import requests
from threading import Thread
import time
import json
import os

app=Flask(__name__)
app.secret_key='fnitems'
types=['outfit', 'emote', 'backpack', 'pickaxe', 'glider', 'loadingscreen', 'contrail', 'emoji', 'wrap', 'spray', 'toy', 'banner', 'music']
bbtypes=['character', 'dance', 'backpack', 'pickaxe', 'glider', 'loadingscreen', 'skydivecontrail', 'emoji', 'itemwrap', 'spray', 'toy']
#https://benbotfn.tk/api/v1/exportAsset?path=Game/Athena/Items/Cosmetics/Series/CUBESeries.uasset
#https://github.com/EthanC/Athena/tree/master/assets/images
#<!--<p><font color="#fff">Play Music</font></p><span onclick="document.getElementById('{{ i['id'] }}').play()"><font color="#909090">&#9205;</font></span><span onclick="document.getElementById('{{ i['id'] }}').pause()"><font color="#909090">&#9208;</font></span>-->

def rs(l):l.sort();return l
  
@app.route('/')
def rootgp():return render_template('root.html', types=types)

@app.route('/all/<type>')
def itemsallgp(type):
  with open(f'json/{type}.json') as itemsf:
    items=json.load(itemsf)
  return render_template('items2.html', items=items)

@app.route("/list", methods=["GET"])
def listg():
  if not 'ml' in session:
    session['ml']=[]
  #print('get',session['ml'])
  return render_template('list.html', ml=session['ml'])

@app.route('/list', methods=['POST'])
def listp():
  if request.form.get('add'):id=request.form.get('add');session['ml']=[id]+[i for i in session['ml'] if not i == id]
  if request.form.get('remove'):id=request.form.get('remove');session['ml']=[i for i in session['ml'] if not i == id]
  #print('post',session['ml'])
  return '<script>history.go( -1 );</script>'

@app.route('/newitem')
def leakgp():
  with open('json/newitem.json') as itemsf:
    items=json.load(itemsf)
  return render_template('items4.html', items=items)

@app.route('/newid')
def leakidgp():
  with open('json/newitem.json') as itemsf:
    items=json.load(itemsf)
  return Markup('<br>'.join([i.get('id') for i in items]))

@app.route('/playlist')
def playlistgp():
  #with open('newitem.json') as itemsf:
  #  items=json.load(itemsf)
  #return render_template('items4.html', items=items)
  with open('playlist.txt') as f:
    pls=f.read().split()
  return Markup('<br>'.join(pls))

@app.route('/<type>')
def itemsgp(type):
  if type == 'favicon.ico':return redirect('https://fortnite-api.com/images/cosmetics/br/cid_005_athena_commando_m_default/icon.png')
  
  if type == 'all':
    with open(f'json/all.json', 'r') as itemsf:
      items=json.load(itemsf)
    with open('json/bb_mp.json', 'r') as mpsf:
      mps=json.load(mpsf)
    return render_template('items3.html', items=items, types=types, mps=mps, none=None, type=type)
  try:
    with open(f'json/{type}.json', 'r') as itemsf:
      items=json.load(itemsf)
  except:
    pass
  
  if type == 'music':
    with open('json/bb_mp.json', 'r') as mpsf:
      mps=json.load(mpsf)
    return render_template('items3.html', items=items, types=types, mps=mps, none=None, type=type)
  if type == 'playmusic':
    with open('json/bb_mp.json', 'r') as mpsf:
      mps=json.load(mpsf)
    return render_template('pm.html', types=types, mps=mps, none=None, type=type)
  return render_template('items3.html', items=items, types=types, type=type)

@app.route('/bb')
def bbrootgp():return render_template('root.html', types=bbtypes)

@app.route('/bb/<type>')
def itemsbbgp(type):
  if type == 'all':
    with open(f'json/bb_all.json', 'r') as itemsf:
      items=json.load(itemsf)
    return render_template('items3.html', items=items, types=bbtypes)
  
  with open(f'json/bb_{type}.json', 'r') as itemsf:
    items=json.load(itemsf)
  return render_template('items4.html', items=items, types=bbtypes)

@app.route('/css/<cssname>')
def cssgp(cssname):
  if not cssname:return 'usage:css/Filename'
  if not os.path.isfile(f'css/{cssname}'):return abort(404)
  with open(f'css/{cssname}', 'r') as cssf:
    css=cssf.read()
  return Response(css, mimetype='text/css')

@app.route('/image/<imagename>')
def imagegp(imagename):
  if not imagename:return 'usage:image/Filename'
  if not os.path.isfile(f'image/box_bottom_{imagename}.png'):send_file('image/box_bottom_common.png', mimetype='image/png')#return abort(404)
  return send_file(f'image/box_bottom_{imagename}.png', mimetype='image/png')

def apiloop():
  while True:
    print('getting from fortnite-api...')
    all=requests.get('https://fortnite-api.com/cosmetics/br/',headers={'x-api-key': 'd62c284cc87b1b1449643d41014abb78a212de67f21b6dd1012755bdf720e891'}).json()["data"]
    print('writing fortnite-api...')
    for t in types:
      with open(f'json/{t}.json', 'w', encoding="utf-8") as f:
        json.dump([i for i in all if i["type"] == t], f, indent='\t')
    else:
      with open('json/all.json', 'w', encoding="utf-8") as f:
        json.dump(all, f, indent='\t')
    print('writed fortnite-api')
    print('getting from benbotfn...')
    bball=requests.get('https://benbotfn.tk/api/v1/cosmetics/br').json()
    bbupcoming=requests.get('https://benbotfn.tk/api/v1/newCosmetics').json()['items']
    bbmusicpath=requests.get('https://benbotfn.tk/api/v1/files/search?path=FortniteGame/Content/Athena/Sounds/MusicPacks/').json()
    print('writing benbotfn...')
    for t in bbtypes:
      with open(f'json/bb_{t}.json', 'w', encoding="utf-8") as f:
        json.dump([i for i in bball if i["backendType"].lower().replace('athena', '') == t], f, indent='\t')
    else:
      with open('json/bb_all.json', 'w', encoding="utf-8") as f:
        json.dump(bball, f, indent='\t')
    with open('json/newitem.json', 'w', encoding="utf-8") as f:
      #ul=[i.get('id', 'None') for i in bbupcoming]
      #ul.sort()
      #rl=[]
      #for i in ul:
      #  for j in bbupcoming:
      #    if i in j.items:rl.append(j)
      #
      json.dump(bbupcoming, f, indent='\t')
    mps={}
    for i in bbmusicpath:
      if not '_cue' in i.lower():
        i=i.replace('FortniteGame', 'Game')
        mps.update({i.split('/')[-1].replace('.uasset', '').replace('Musicpack_', '').replace('MusicPack_', '').replace('Athena_', ''):i})
    with open('json/bb_mp.json', 'w', encoding="utf-8") as f:
      json.dump(mps, f, indent='\t')
    print('writed benbotfn')
        
    time.sleep(600)
Thread(target=apiloop,args=()).start()
app.run(host="0.0.0.0", port=3000, threaded=True)