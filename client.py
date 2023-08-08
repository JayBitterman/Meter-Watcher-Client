import socket as s
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        action = "None"
        if request.form.get('Park') == 'Park':
            action = "park"
        elif request.form.get('Tattle') == 'Tattle':
            action = "tattle"
        # SOCK_STREAM = TCP
        client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)

        # Connect client to server IP and port
        # Online Server IP
        address, port = "3.94.59.235", 6789

        client_socket.connect((address, port))

        try:
            # Send action message to server
            client_socket.send(bytes(action, encoding='UTF-8'))

        except Exception as msg:
            print(msg)

        # Listen for server tattles
        while True:
            try:
                # Receive tattle from server
                server_msg = client_socket.recv(1024).decode()
                if not server_msg:
                    break
                elif server_msg == 'Meter Maid in your area! Run!':
                    return redirect('warning')
            except Exception as msg:
                print(msg)
                # Close upon error
                client_socket.close()
                break
    return render_template('index.html')


@app.route('/warning')
def warning():
    return render_template('warning.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
