from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta'  # Cambia esto por una clave secreta más segura

# Lista de seminarios disponibles
seminarios_disponibles = [
    'Seminario de Tecnología',
    'Seminario de Salud',
    'Seminario de Educación',
    'Seminario de Innovación'
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrar_inscrito', methods=['GET', 'POST'])
def registrar_inscrito():
    if request.method == 'POST':
        inscrito = {
            'id': request.form['id'],
            'nombre': request.form['nombre'],
            'apellido': request.form['apellido'],
            'fecha': request.form['fecha'],
            'turno': request.form['turno'],
            'seminario': request.form.getlist('seminarios')  # Obtener seminarios seleccionados
        }

        # Comprobar si la sesión de inscritos existe
        if 'inscritos' not in session:
            session['inscritos'] = []

        # Verificar si el ID es único
        for i in session['inscritos']:
            if i['id'] == inscrito['id']:
                flash('El ID ya existe. Introduce uno único.', 'error')
                return redirect(url_for('registrar_inscrito'))

        session['inscritos'].append(inscrito)
        session.modified = True
        flash('Inscrito registrado exitosamente.', 'success')
        return redirect(url_for('listar_inscritos'))

    return render_template('registrar_inscrito.html', seminarios=seminarios_disponibles)

@app.route('/listar_inscritos')
def listar_inscritos():
    inscritos = session.get('inscritos', [])
    return render_template('listar_inscritos.html', inscritos=inscritos)

@app.route('/editar_inscrito/<string:inscrito_id>', methods=['GET', 'POST'])
def editar_inscrito(inscrito_id):
    inscritos = session.get('inscritos', [])
    
    # Encontrar el inscrito a editar
    inscrito_a_editar = next((i for i in inscritos if i['id'] == inscrito_id), None)
    
    if request.method == 'POST':
        # Actualizar inscrito
        inscrito_actualizado = {
            'id': request.form['id'],
            'nombre': request.form['nombre'],
            'apellido': request.form['apellido'],
            'fecha': request.form['fecha'],
            'turno': request.form['turno'],
            'seminario': request.form.getlist('seminarios')  # Obtener seminarios seleccionados
        }

        # Verificar que el ID no esté en uso por otro inscrito
        for i in inscritos:
            if i['id'] != inscrito_id and i['id'] == inscrito_actualizado['id']:
                flash('El ID ya existe. Introduce uno único.', 'error')
                return redirect(url_for('editar_inscrito', inscrito_id=inscrito_id))

        # Actualizar la lista de inscritos
        session['inscritos'] = [inscrito_actualizado if i['id'] == inscrito_id else i for i in inscritos]
        session.modified = True
        flash('Inscrito editado exitosamente.', 'success')
        return redirect(url_for('listar_inscritos'))

    return render_template('editar_inscrito.html', inscrito=inscrito_a_editar, seminarios=seminarios_disponibles)

@app.route('/eliminar_inscrito/<string:inscrito_id>')
def eliminar_inscrito(inscrito_id):
    if 'inscritos' in session:
        session['inscritos'] = [i for i in session['inscritos'] if i['id'] != inscrito_id]
        session.modified = True
        flash('Inscrito eliminado exitosamente.', 'success')
    return redirect(url_for('listar_inscritos'))

if __name__ == '__main__':
    app.run(debug=True)
