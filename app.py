from _cffi_backend import string
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from sqlalchemy.sql import exists
import asyncio
import json
import aiohttp
import os
from aiohttp import ClientSession
import rsa
from base64 import b64encode, b64decode

app = Flask(__name__)
app.secret_key = "Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/dentao'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    CPF = db.Column(db.String(11))
    templano = db.Column(db.String(1))
    nomeplano = db.Column(db.String(100))
    tipoplano = db.Column(db.String(100))
    prontuario = db.Column(db.String(100))
    datanasc = db.Column(db.Date())
    dependente = db.Column(db.String(1))
    ultcons = db.Column(db.Date())

    def __init__(self, nome, CPF, templano, nomeplano, tipoplano, prontuario, datanasc, dependente, ultcons):
        self.nome = nome
        self.CPF = CPF
        self.templano = templano
        self.nomeplano = nomeplano
        self.tipoplano = tipoplano
        self.prontuario = prontuario
        self.datanasc = datanasc
        self.dependente = dependente
        self.ultcons = ultcons

class Orcamento(db.Model):
    idorc = db.Column(db.Integer, primary_key=True)
    idproc = db.Column(db.String(10000))
    denprot = db.Column(db.String(10000))
    descproc = db.Column(db.String(10000))
    identista = db.Column(db.Integer())
    dataaval = db.Column(db.Date())
    ass = db.Column(db.String(10000))
    dass = db.Column(db.String(10000))
    pkey = db.Column(db.String(10000))
    valor = db.Column(db.Numeric(65, 2))

    def __init__(self, idproc, denprot, descproc, identista, dataaval, ass, dass, pkey, valor):
        self.idproc = idproc
        self.denprot = denprot
        self.descproc = descproc
        self.identista = identista
        self.dataaval = dataaval
        self.ass = ass
        self.dass = dass
        self.pkey = pkey
        self.valor = valor

class Tabela(db.Model):
    idp = db.Column(db.Integer, primary_key=True)
    val = db.Column(db.Numeric(65, 2))

    def __init__(self, val):
        self.val = val

class Pedido(db.Model):
    idped = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(100))
    motivo = db.Column(db.String(10000))
    dataped = db.Column(db.Date())
    datares = db.Column(db.Date())

    def __init__(self, idped, status, motivo, dataped, datares):
        self.idped = idped
        self.status = status
        self.motivo = motivo
        self.dataped = dataped
        self.datares = datares

class Acompanhamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idorc = db.Column(db.Integer())
    dataini = db.Column(db.Date())
    datafim = db.Column(db.Date())
    identista = db.Column(db.Integer())
    itemorc = db.Column(db.String(100))

    def __init__(self, idorc, dataini, datafim, itemorc, identista):
        self.idorc = idorc
        self.dataini = dataini
        self.datafim = datafim
        self.identista = identista
        self.itemorc = itemorc

async def get_pedido(session, url):
    async with session.get(url) as resp:
        pedido = await resp.json()
        return pedido

@app.route('/api', methods=['GET', 'POST'])
def apage():
    y = request.form.get('x')
    if y == '':
        flash("Entrada Inválida")
        return redirect(url_for('dentista'))
    asyncio.run(getall(y))
    mydata = db.session.query(Pedido).order_by(Pedido.idped)
    return render_template("api.html",pedidos=mydata)

async def getall(x):

    async with aiohttp.ClientSession() as session:
        tasks = []
        if int(x)<0:
            x=int(x)*-1
        elif int(x)==0:
            x = 1
        y = int(x)+1
        for id in range(1, y):
            url = f"http://localhost:3002/api/planosaude?idped={id}"
            tasks.append(asyncio.ensure_future(get_pedido(session, url)))

        pedidos = await asyncio.gather(*tasks)
        i = 0
        for pedido in pedidos:
            idped = pedido[i]['idped']
            status = pedido[i]['status']
            motivo = pedido[i]['motivo']
            dataped = pedido[i]['dataped']
            datares = pedido[i]['datares']
            query_ped = Pedido.query.filter_by(idped=idped)
            exist = query_ped.count()
            if exist != 0:
                my_data = Pedido.query.get(idped)
                my_data.status = status
                my_data.motivo = motivo
                my_data.dataped = dataped
                my_data.datares = datares
            else:
                my_data = Pedido(idped, status, motivo, dataped, datares)
                db.session.add(my_data)
            db.session.commit()
            i = i+1

@app.route('/')
def Index():
    all_data = Cliente.query.all()
    return render_template("index.html", clientes=all_data)

@app.route('/dentista')
def dentista():
    all_data = Orcamento.query.all()
    all_desc = Tabela.query.all()
    return render_template("dentista.html", orcamentos=all_data, tabela=all_desc)

@app.route('/search', methods=['GET', 'POST'])
def search():
        CPF = request.form.get('CPF')
        my_data = Cliente.query.filter_by(CPF=CPF).first()
        if my_data is None:
            return redirect(url_for('Index'))
        else:
            return cpage(my_data.CPF)

@app.route('/cpage/<CPF>/', methods=['GET', 'POST'])
def cpage(CPF):
    my_data = Cliente.query.filter_by(CPF=CPF).first()

    return render_template("cliente.html",
                           id=my_data.id,
                           nome=my_data.nome,
                           CPF=my_data.CPF,
                           templano=my_data.templano,
                           nomeplano=my_data.nomeplano,
                           tipoplano=my_data.tipoplano,
                           prontuario=my_data.prontuario,
                           datanasc=my_data.datanasc,
                           dependente=my_data.dependente,
                           ultcons=my_data.ultcons)

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        nome = request.form['nome']
        CPF = request.form['CPF']
        templano = request.form['templano']
        nomeplano = request.form['nomeplano']
        tipoplano = request.form['tipoplano']
        prontuario = request.form['prontuario']
        ultcons = request.form['ultcons']
        datanasc = request.form['datanasc']
        dependente = request.form['dependente']
        errorcode=0
        all_data = Cliente.query.all()
        if (int(CPF)/10000000000<1):
            if errorcode == 0:
                errorcode = 1
            else:
                errorcode = 7

        elif (int(CPF)/10000000000>=10):
            if errorcode == 0:
                errorcode = 2
            else:
                errorcode = 7

        if (int(prontuario)<=0 or int(prontuario)>=2147483647):
            if errorcode == 0:
                errorcode = 3
            else:
                errorcode = 7

        elif (templano == 'S' and nomeplano == 'Particular' or tipoplano == 'Pagar inteiro'):
            if errorcode == 0:
                errorcode = 6
            else:
                errorcode = 7

        for row in all_data:
            if (prontuario == row.prontuario):
                if errorcode == 0:
                    errorcode = 4
                else:
                    errorcode = 7
            if (CPF == row.CPF):
                if errorcode == 0:
                    errorcode = 5
                else:
                    errorcode = 6

        if errorcode == 1:
            flash("CPF Inválido (Curto demais)")
            return redirect(url_for('Index'))
        elif errorcode == 2:
            flash("CPF Inválido (Longo demais)")
            return redirect(url_for('Index'))
        elif errorcode == 3:
            flash("Prontuário Inválido")
            return redirect(url_for('Index'))
        elif errorcode == 4:
            flash("Prontuário já cadastrado")
            return redirect(url_for('Index'))
        elif errorcode == 5:
            flash("CPF já cadastrado")
            return redirect(url_for('Index'))
        elif errorcode == 6:
            flash("Especiifique corretamente os dados do plano de saúde")
            return redirect(url_for('Index'))
        elif errorcode == 7:
            flash("Múltiplos erros, envio cancelado")
            return redirect(url_for('Index'))

        if templano=='N':
            nomeplano = 'Particular'
            tipoplano = 'Pagar inteiro'

        my_data = Cliente(nome, CPF, templano, nomeplano, tipoplano, prontuario, datanasc, dependente, ultcons)
        db.session.add(my_data)
        db.session.commit()

        flash("Cliente inserido")

    return redirect(url_for('Index'))

@app.route('/inserto', methods=['POST'])
def inserto():
    if request.method == 'POST':
        idproc = request.form['idproc']
        denprot = request.form['denprot']
        descproc = request.form['descproc']
        identista = request.form['identista']
        dataaval = request.form['dataaval']
        ass = request.form['ass']
        valor = request.form['valor']
        keysize = 1024
        (public, private) = rsa.newkeys(keysize)
        signature = b64encode(rsa.sign(ass, private, "SHA-256"))
        dass = signature
        key = public

        if (int(identista)<=0 or int(identista)>=2147483647):
            flash("ID de Dentista Inválido")
            return redirect(url_for('dentista'))

        my_data = Orcamento(idproc, denprot, descproc, identista, dataaval, ass, dass, key, valor)
        db.session.add(my_data)
        db.session.commit()

        flash("Orçamento inserido")

        return redirect(url_for('dentista'))

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Cliente.query.get(request.form.get('id'))
        my_data.nome = request.form['nome']
        my_data.CPF = request.form['CPF']
        my_data.templano = request.form['templano']
        my_data.nomeplano = request.form['nomeplano']
        my_data.tipoplano = request.form['tipoplano']
        my_data.prontuario = request.form['prontuario']
        my_data.ultcons = request.form['ultcons']
        my_data.datanasc = request.form['datanasc']
        my_data.dependente = request.form['dependente']
        errorcoder=0
        all_data = Cliente.query.all()

        if (int(my_data.CPF) / 10000000000 < 1):
            if errorcoder == 0:
                errorcoder = 1
                flash("1")
            else:
                errorcoder = 6

        elif (int(my_data.CPF) / 10000000000 >= 10):
            if errorcoder == 0:
                errorcoder = 2
            else:
                errorcoder = 6

        elif (int(my_data.prontuario) <= 0 or int(my_data.prontuario)>=2147483647):
            if errorcoder == 0:
                errorcoder = 3

            else:
                errorcoder = 6

        elif (my_data.templano == 'S' and my_data.nomeplano == 'Particular' or my_data.tipoplano == 'Pagar inteiro'):
            if errorcoder == 0:
                errorcoder = 4

            else:
                errorcoder = 6

        if errorcoder == 1:
            flash("CPF Inválido (Curto demais)")
            return redirect(url_for('Index'))
        elif errorcoder == 2:
            flash("CPF Inválido (Longo demais)")
            return redirect(url_for('Index'))
        elif errorcoder == 3:
            flash("Prontuário Inválido")
            return redirect(url_for('Index'))
        elif errorcoder == 4:
            flash("Especiifique corretamente os dados do plano de saúde")
            return redirect(url_for('Index'))
        elif errorcoder == 6:
            flash("Múltiplos erros, envio cancelado")
            return redirect(url_for('Index'))

        if my_data.templano == 'N':
            my_data.nomeplano = 'Particular'
            my_data.tipoplano = 'Pagar inteiro'

        db.session.commit()
        flash("Cliente editado!")

        return redirect(url_for('Index'))

@app.route('/updateo', methods=['GET', 'POST'])
def updateo():
    if request.method == 'POST':
        my_data = Orcamento.query.get(request.form.get('idorc'))
        my_data.idproc = request.form['idproc']
        my_data.denprot = request.form['denprot']
        my_data.descproc = request.form['descproc']
        my_data.identista = request.form['identista']
        my_data.dataaval = request.form['dataaval']
        my_data.ass = request.form['ass']
        my_data.dass = request.form['dass']
        my_data.key = request.form['key']
        my_data.valor = request.form['valor']

        if (int(my_data.identista)<=0 or  int(my_data.identista)>=2147483647):
            flash("ID de Dentista Inválido")
            return redirect(url_for('dentista'))

        db.session.commit()
        flash("Orçamento editado!")

        return redirect(url_for('dentista'))

@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Cliente.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Cliente removido :(")

    return redirect(url_for('Index'))

@app.route('/deleteo/<idorc>/', methods=['GET', 'POST'])
def deleteo(idorc):
    my_data = Orcamento.query.get(idorc)
    db.session.delete(my_data)
    db.session.commit()
    flash("Orçamento removido :(")

    return redirect(url_for('dentista'))

if __name__ == "__main__":
    app.run(debug=True)