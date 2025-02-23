from flask import Flask, request, render_template
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def upload_bot():
    message = None  # Default message is None
    if request.method == 'POST':
        bot_file = request.files['bot_file']
        if bot_file and bot_file.filename.endswith('.py'):
            bot_path = os.path.join(UPLOAD_FOLDER, bot_file.filename)
            bot_file.save(bot_path)

            req_file = request.files.get('requirements_file')
            if req_file:
                req_path = os.path.join(UPLOAD_FOLDER, 'requirements.txt')
                req_file.save(req_path)
                try:
                    subprocess.run(['pip', 'install', '-r', req_path], check=True)
                except Exception as e:
                    message = f"⚠️ Error installing dependencies: {str(e)}"
                    return render_template('index.html', message=message)

            try:
                subprocess.Popen(['python', bot_path])
                message = "✅ Bot Successfully Hosted!"
            except Exception as e:
                message = f"⚠️ Error running bot: {str(e)}"

    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
