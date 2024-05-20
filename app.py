from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/check_spam', methods=['POST'])
def check_spam():
    email_text = request.form['email_text']
    # Dummy spam check logic
    if "spam" in email_text.lower():
        result = "This is spam."
    else:
        result = "This is not spam."
    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)
