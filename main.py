from webblog import app

# de acordo com a estrutura do código, o arquivo main é utilizado apenas para rodar o app
# garante que o código abaixo irá rodar somente se o arquivo em questao estiver rodando
if __name__ == '__main__':
    # debug=True para não ser necessário resetar o código após novas alterações, basta F5 no browser
    app.run(debug=True)
