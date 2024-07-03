from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
import mysql.connector


def inserir():
    '''função para capturar os dados da tela formulario'''
    produto = formulario.txtProduto.text()
    preco = formulario.txtPreco.text()
    estoque = formulario.txtEstoque.text()
    formulario.lblMsg.setText('DADOS CADASTRADOS COM SUCESSO')

    #faz a conexão e inserção no banco de dados
    cursor = conexao.cursor() #var que recebe a conexao e faz uma varredura no db
    comando_SQL = f'''INSERT INTO produtos (nome,preco,estoque) 
    VALUES ('{str(produto)}','{float(preco)}','{int(estoque)}')'''
    cursor.execute(comando_SQL)
    conexao.commit() #envia as informações ao db

    #seta os valores vazios a janela dps do cadastro
    formulario.txtProduto.setText('')
    formulario.txtPreco.setText('')
    formulario.txtEstoque.setText('')


def lista_relatorio():
    '''Mostra relatório de itens'''
    lista.show()
    cursor = conexao.cursor()
    comando_SQL = 'SELECT * FROM produtos' #leitura do bd
    cursor.execute(comando_SQL)
    leitura_banco = cursor.fetchall() #diferenciação l,c e atribui a leiturabanco

    lista.tableWidget.setRowCount(len(leitura_banco)) #seta quantidade linhas na tabela
    lista.tableWidget.setColumnCount(4) #quantidade de colunas

    for L in range(len(leitura_banco)):
        for C in range(0, 4):
            lista.tableWidget.setItem(L, C, QTableWidgetItem(str(leitura_banco[L][C])))

id_atual = int


def excluir():
    remover = lista.tableWidget.currentRow()
    lista.tableWidget.removeRow(remover)

    cursor = conexao.cursor()
    cursor.execute('SELECT id FROM produtos')
    leitura_banco = cursor.fetchall()
    valor_id = leitura_banco[remover][0]
    comando_SQL = f'DELETE FROM produtos WHERE ID = "{(valor_id)}"'
    cursor.execute(comando_SQL)

    conexao.commit()
def edit():
    editar.show()
    global id_atual
    dados = lista.tableWidget.currentRow()
    cursor = conexao.cursor()
    cursor.execute('SELECT id FROM produtos')
    leitura_banco = cursor.fetchall()
    valor_id = leitura_banco [dados][0]
    comando_SQL = f'SELECT * FROM produtos WHERE ID = "{valor_id}"'
    cursor.execute(comando_SQL)
    leitura_banco = cursor.fetchall()

    id_atual = valor_id
    editar.txtAlterarId.setText(str(leitura_banco[0][0]))
    editar.txtAlterarProduto.setText(leitura_banco[0][1])
    editar.txtAlterarPreco.setText(str(leitura_banco[0][2]))
    editar.txtAlterarEstoque.setText(str(leitura_banco[0][3]))


def salvar_dados():
    global id_atual

    id = int(editar.txtAlterarId.text())
    nome = editar.txtAlterarProduto.text()
    preco = float(editar.txtAlterarPreco.text())
    estoque = int(editar.txtAlterarEstoque.text())

    cursor = conexao.cursor()
    sql = "UPDATE produtos SET id = %s, nome = %s, preco = %s, estoque = %s WHERE id = %s;"
    valores = (id, nome, preco, estoque, id)

    cursor.execute(sql, valores)

    editar.close()
    lista.close()
    formulario.show()

    conexao.commit()

#Cria variavel para receber conexão com o db, com as informações necessarias
conexao = mysql.connector.connect(
    host="localhost",
    user="dev",
    password="1234",
    database="cadastro_produtos"
)

app = QtWidgets.QApplication([])

formulario = uic.loadUi('formulario.ui')
formulario.btnCadastrar.clicked.connect(inserir)
formulario.btnRelatorio.clicked.connect(lista_relatorio)

lista = uic.loadUi('lista.ui')
lista.btnAlterarRegistro.clicked.connect(edit)
lista.btnApagarRegistro.clicked.connect(excluir)

editar = uic.loadUi('editar.ui')
editar.btnConfirmarAlteracao.clicked.connect(salvar_dados)

formulario.show()
app.exec()
