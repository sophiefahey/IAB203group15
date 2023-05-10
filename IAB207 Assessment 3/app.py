from assessment3 import create_app
#^^^will default to __init___


#this makes the interpreter run app
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)