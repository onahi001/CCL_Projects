from flask import Flask, render_template, request, jsonify
import bdapp

app = Flask(__name__)

@app.route('/test', methods=['POST'])
def main():
    data = request.json
    feed = data.get('feed')
    reflux = data.get('reflux')
    alpha = data.get('alpha')
    q_value = data.get('q_value')
    no_plates = data.get('no_plates')
    xf = data.get('xf')
    xd = data.get('xd')
    xw = data.get('xw')
    
    try:
        xn_points, yn_points, rect_points, strip_points, q_points, no_plates = bdapp.mccabe_plot (alpha=alpha, xd=xd, xw=xw, xf=xf, F=feed, R=reflux, q=q_value)
        D, W = bdapp.stream(F=feed, xf=xf, xd=xd, xw=xw)
        x_eq, y_eq = bdapp.equilibrium_data(alpha=alpha)
        min_reflux = bdapp.min_reflux(alpha=alpha, xf=xf, xd=xd)
        graph_image = bdapp.x_y_plot(x_eq, y_eq, rect_points, strip_points, xn_points, yn_points, q_points, xf=xf, q=q_value)
        return jsonify({"graph_image":graph_image, "D":D, "W":W, "no_plates":no_plates, "min_reflux":min_reflux})
    except:
        print("error seen. Check Input")


@app.route('/reflux', methods=['POST'])
def reflux():
    data=request.json
    feed= data.get('feed')
    reflux = data.get('reflux')
    alpha = data.get('alpha')
    q_value = data.get('q_value')
    no_plates = data.get('no_plates')
    xf = data.get('xf')
    xd = data.get('xd')
    xw = data.get('xw')
    
    
    try:
        D, W = bdapp.stream(F=feed, xf=xf, xd=xd, xw=xw)
        reflux = bdapp.find_reflux(alpha=alpha, F=feed, D=D, W=W, q=q_value, n=no_plates, xd=xd, xw=xw)
        xn_points, yn_points, rect_points, strip_points, q_points, no_plates = bdapp.mccabe_plot (alpha=alpha, xd=xd, xw=xw, xf=xf, F=feed, R=reflux, q=q_value)
        print(f"this is {reflux}")
        x_eq, y_eq = bdapp.equilibrium_data(alpha=alpha)
        min_reflux = bdapp.min_reflux(alpha=alpha, xf=xf, xd=xd)
        graph_image = bdapp.x_y_plot(x_eq, y_eq, rect_points, strip_points, xn_points, yn_points, q_points, xf=xf, q=q_value)
        return jsonify({"graph_image":graph_image, "D":D, "W":W, "reflux":reflux, "min_reflux":min_reflux})
    except:
        print("error seen. Check Input")


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)

