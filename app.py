from flask import Flask, render_template, request, jsonify, redirect
import sqlite3

app = Flask(__name__)
DB_PATH = "power_management.db"

# Initialize the database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appliances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            power_consumption REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    """
    Renders the homepage with appliance management options.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM appliances")
    appliances = cursor.fetchall()
    conn.close()
    return render_template("index.html", appliances=appliances)

@app.route("/add_appliance", methods=["POST"])
def add_appliance():
    """
    Adds a new appliance with its power consumption.
    """
    name = request.form.get("name")
    power_consumption = float(request.form.get("power_consumption"))
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO appliances (name, power_consumption) VALUES (?, ?)", (name, power_consumption))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/edit_appliance/<int:id>", methods=["POST"])
def edit_appliance(id):
    """
    Updates the power consumption of an existing appliance.
    """
    new_power = float(request.form.get("new_power"))
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE appliances SET power_consumption = ? WHERE id = ?", (new_power, id))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route('/delete_appliance/<int:appliance_id>', methods=['POST'])
def delete_appliance(appliance_id):
    try:
        conn = sqlite3.connect('appliances.db')
        cursor = conn.cursor()

        # Delete the appliance with the given ID
        cursor.execute('DELETE FROM appliances WHERE id = ?', (appliance_id,))
        conn.commit()
        conn.close()

        return redirect('/')
    except Exception as e:
        return f"An error occurred: {e}", 500

@app.route("/predict", methods=["POST"])
def predict_consumption():
    """
    Predicts energy consumption based on user inputs for appliance usage.
    """
    data = request.form
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, power_consumption FROM appliances")
    appliances = cursor.fetchall()
    conn.close()

    total_consumption = 0
    for appliance in appliances:
        name = appliance[0]
        power = appliance[1]
        count = int(data.get(f"{name}_count", 0))
        hours = float(data.get(f"{name}_hours", 0))
        total_consumption += count * power * hours

    return jsonify({"prediction": total_consumption})

@app.route("/set_limit", methods=["POST"])
def set_limit():
    """
    Checks if the predicted consumption exceeds the user-defined limit.
    Provides tips and solutions to reduce consumption.
    """
    limit = float(request.form.get("limit"))
    consumption = float(request.form.get("consumption"))

    if consumption > limit:
        # Generate tips to reduce consumption
        tips = [
            "Reduce usage hours for high-power appliances.",
            "Unplug appliances when not in use.",
            "Use energy-efficient appliances.",
            "Turn off unused lights and electronics.",
        ]
        return jsonify({"status": "limit_exceeded", "tips": tips, "exceeded_by": consumption - limit})
    else:
        return jsonify({"status": "within_limit"})

if __name__ == "__main__":
    app.run(debug=True)
