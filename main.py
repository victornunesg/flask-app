from webblog import app, database

""" De acordo com a estrutura do código, o arquivo main é utilizado apenas para rodar o app. O código abaixo garante que
o app irá rodar somente se o arquivo em questão, 'main.py', estiver rodando. """

if __name__ == '__main__':
    # debug=True para não ser necessário resetar o código após novas alterações, basta F5 no browser
    app.run(debug=True)
