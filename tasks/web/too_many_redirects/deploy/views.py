from init import app
from flask import redirect, request, make_response, render_template
from random import shuffle

flag_orig = "TyumenCTF{3rr_t00_m4ny_r3d1r3cts_F93CD9}"
flag = [[i, flag_orig[i]] for i in range(len(flag_orig))]
shuffle(flag)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/run")
def run():
    return redirect("/get?idx=0")

@app.route(f"/get")
def get_flag():
    try:
        if request.args:
            idx = int(request.args.get("idx"))
            part = flag[idx]
            resp = make_response(redirect(f"/get?idx={idx+1}"))
            resp.headers["Flag"] = f"{part[0]}_{part[1]}"
            return resp
        return redirect("/")
    except Exception as e:
        return redirect("/")
