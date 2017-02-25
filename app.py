from flask import Flask, render_template, json, request
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('rps.html')


@app.route('/rps_choose', methods=['POST'])
def rps():
    
    _result = request.form['rps_option']
    
    if _result:
        result_str = 'You chose {}'.format(_result)
        json_map = {}
        json_map["message"] = result_str
        
        return json.dumps(json_map)
