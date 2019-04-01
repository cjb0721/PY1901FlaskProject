from flask import Flask, render_template, request, redirect, make_response
import datetime
from orm import model, manageorm
app = Flask(__name__)
app.send_file_max_age_default = datetime.timedelta(seconds=1)
app.debug = True

@app.route('/')
def index():
    # html = "<h1>hello world</h1>"
    # return html
    html = "index.html"
    # name = "猪猪侠"
    name = request.cookies.get("name")
    titles = "九九乘法表"
    n = range(1, 10)
    return render_template(html, username=name, title=titles, m=n)


@app.route('/regist', methods=["GET", "POST"])
def regist():
    # if request.method == "GET":
    #     html = "regist.html"
    #     return render_template(html)
    # elif request.method == "POST":
        name = request.form['user']
        pwd = request.form['pwd']
        # try:
        #     manageorm.insertUser(name, pwd)
        #     return redirect('/login')
        # except:
        #     return redirect('/regist')
        if name and pwd:
            manageorm.insertUser(name, pwd)
        return redirect('/')


@app.route('/login', methods=["GET", "POST"])
def login():
    # if request.method == "GET":
    #     html = "login.html"
    #     return render_template(html)
    # elif request.method == "POST":
        name = request.form['user']
        pwd = request.form['pwd']
        try:
            result = manageorm.checkUser(name, pwd)
            res = make_response(redirect('/list'))
            res.set_cookie("name", str(result), expires=datetime.datetime.now()+datetime.timedelta(days=7))
            res.set_cookie("user", name, expires=datetime.datetime.now()+datetime.timedelta(days=7))
            return res
        except:
            return redirect('/')


@app.route('/quit')
def quit():
    res = make_response(redirect('/'))
    res.delete_cookie("name")
    return res


@app.route('/list')
def list():
    userid = request.cookies.get("name")
    user = request.cookies.get("user")
    html = "list.html"
    list = manageorm.queryPro(userid)
    return render_template(html, user=user, info=list)


@app.route('/delete/<int:id>')
def delete(id):
    userid = request.cookies.get("name")
    manageorm.deletePro(id=id, userid=userid)
    return redirect('/list')


@app.route('/update/<int:id>', methods=["GET", "POST"])
def update(id):
    userid = request.cookies.get("name")
    user = request.cookies.get("user")
    if request.method == "GET":
        html = "updatePro.html"
        detail = manageorm.queryProOne(id, userid)
        return render_template(html, user=user, id=id, detail=detail, username=userid)
    elif request.method == "POST":
        print("Post请求获取页面")
        id = id
        body = request.form["body"]
        try:
            manageorm.updatePro(id=id, body=body, userid=userid)
            return redirect('/list')
        except:
            return redirect('/update/'+id)


@app.route('/detail/<int:id>')
def detail(id):
    userid = request.cookies.get("name")
    user = request.cookies.get("user")
    html = "detail.html"
    detail = manageorm.queryProOne(id, userid)
    return render_template(html, user=user, id=id, detail=detail, username=userid)


@app.route('/projectAdd', methods=["GET", "POST"])
def projectAdd():
    if request.method == "GET":
        html = "projectAdd.html"
        return render_template(html)
    elif request.method == "POST":
        proname = request.form['proname']
        probody = request.form['probody']
        userid = request.cookies.get("name")
        if proname and probody and len(probody) < 200:
            detail = manageorm.queryPro(userid)
            f = True
            for d in detail:
                if proname == d[1]:
                    f = False
            if f:
                try:
                    manageorm.insertPro(proname, probody, userid)
                    return redirect('/list')
                except:
                    return redirect('/projectAdd')
            else:
                return redirect('/projectAdd')
        else:
            return redirect('/projectAdd')


if __name__ == "__main__":
    app.run(host="localhost", port=8866)
