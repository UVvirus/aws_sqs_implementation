from flask import Flask, render_template,redirect,url_for
from get_response import get_user_input,nmap_scan
from sqs_operations import send_to_queue,receive_msg_from_queue
from forms import Inputform


app=Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'


@app.route("/",methods=["GET","POST"])
async def main():
    form=Inputform()
    if form.validate_on_submit():
        domain_name=form.name.data

        user_input=get_user_input(domain_name)
        await send_to_queue(user_input)

        domain_name_to_scan=await receive_msg_from_queue()
        await nmap_scan(domain_name_to_scan)

        return redirect(url_for('success'))
    return render_template('index.html',form=form)

@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
        app.run(debug=True)