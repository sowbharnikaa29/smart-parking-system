from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# In-memory storage for parking slots (for demo purposes)
parking_slots = {f'Slot {i}': None for i in range(1, 11)}

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        print(f"DEBUG: username='{username}', password='{password}'")  # Debug output
        # Simple hardcoded authentication for demo
        if username == 'admin' and password == 'admin':
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error = 'Invalid credentials. Please try again.'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    message = ''
    if request.method == 'POST':
        vehicle_number = request.form['vehicle_number']
        slot = request.form['slot']
        if parking_slots[slot] is None:
            parking_slots[slot] = vehicle_number
            message = f'Vehicle {vehicle_number} parked in {slot}.'
        else:
            message = f'{slot} is already occupied.'
    return render_template('index.html', slots=parking_slots, message=message)

@app.route('/leave/<slot>')
def leave(slot):
    parking_slots[slot] = None
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
