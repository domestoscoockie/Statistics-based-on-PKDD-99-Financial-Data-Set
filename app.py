from PKDD import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True, host='0.0.0.0', port=5000)

