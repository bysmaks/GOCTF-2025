from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello_world ():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>task osint</title>
    <style>
        html, body {
            height: 100%;
        }

        body {
            background-repeat: repeat;
            background: linear-gradient(to bottom, #000000a0, #000000a0), url('static/world.png') no-repeat 50%, linear-gradient(to bottom, #87CEEB, #00bfff);
            color: white; 
            text-align: center;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .container {
        background: #69696990;
        border: 1px solid black;
        border-radius: 15px;
        color: white;
        padding: 5px; 
        justify-content: flex-start;
        align-items: center;
        margin-bottom: 10px;
        width: 700px;
        }

        form {
        margin-top: 10px;
        }

        input[type="submit"] {
        border-radius: 5px;
        background-color: blue;
        color: white;
        padding: 8px 16px;
        cursor: pointer;
        border: none;
        transition: background-color 0.3s;
        }

        input[type="submit"]:hover {
        background-color: black;
        }


        label {
            display: inline-block;
            font-size: 18px;
            text-align: left;
            margin-right: 10px;
            margin-bottom: 5px;
        }

        form label, form input {
            display: inline-block;
            margin-bottom: 10px;
        }

        form input {
            width: 200px;
            margin-left: 10px;
        }

        form {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .form-row {
            display: flex;
            justify-content: flex-start;
            align-items: center;
            margin-bottom: 10px;
            width: 350px;
        }

        .form-row label {
            width: 100px;
            text-align: right;
            margin-right: 10px;
        }

        .form-row input {
            flex: 1;
            padding: 5px;
        }

        #y {
            margin-top: 5px; 
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Получите флаг!</h1>
        <form onsubmit="submitForm(); return false;">
            <div class="form-row">
                <label for="FIO">ФИО:</label>
                <input name="FIO" id="FIO" />
            </div>
            <div class="form-row">
                <label for="x">Широта:</label>
                <input name="x" id="x" />
            </div>
            <div class="form-row">
                <label for="y">Долгота:</label>
                <input name="y" id="y" />
            </div>
            <div class="form-row">
                <input type="submit" value="Отправить" />
            </div>
        </form>
        <p id="flag"></p>
    </div>
    <script>
        function submitForm() {
            var x = document.getElementById("x").value;
            var y = document.getElementById("y").value;
            var fio = document.getElementById("FIO").value;

            fetch("/try", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: "x=" + encodeURIComponent(x) + "&y=" + encodeURIComponent(y) + "&FIO=" + encodeURIComponent(fio)
            })
            .then(response => response.text())
            .then(data => document.getElementById("flag").textContent = data);
        }
    </script>
</body>
</html>
"""

@app.route('/try', methods=["POST"])
def try_flag():
    try:
        x = request.form['x']
        y = request.form['y']
        FIO = request.form['FIO']

        if x == "52.216172" and y == "24.397040" and FIO == "Наумчик Алексей Григорьевич":
            return """Flag is GOCTF{P@rt1zan0_pr@d33d0_28723491131}."""
    except Exception as e:
        print(e)

    return """Nice try!"""

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)
