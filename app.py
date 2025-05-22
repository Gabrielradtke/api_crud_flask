# Importa as bibliotecas necessárias do Flask:
# Flask: cria o aplicativo web
# request: pega dados enviados pelo cliente (como JSON)
# jsonify: transforma Python em JSON para enviar de volta
from flask import Flask, request, jsonify

# Cria a aplicação Flask
app = Flask(__name__)

# "Banco de dados" em memória: lista de usuários
usuarios = []

# Controla o próximo ID a ser atribuído automaticamente
proximo_id = 1

# Quando acessarem /usuarios com método GET
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    # Retorna a lista de usuários convertida para JSON
    return jsonify(usuarios)

# Quando acessarem /usuarios com método POST
@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    global proximo_id  # Usa a variável global para gerar ID único

    # Pega os dados JSON enviados no corpo da requisição
    dados = request.get_json()

    # Validação simples: verifica se nome e idade existem
    if not dados or 'nome' not in dados or 'idade' not in dados:
        return jsonify({"erro": "JSON inválido. Forneça 'nome' e 'idade'."}), 400

    # Cria um novo usuário com ID, nome e idade
    novo_usuario = {
        "id": proximo_id,
        "nome": dados["nome"],
        "idade": dados["idade"]
    }

    # Adiciona o novo usuário à lista
    usuarios.append(novo_usuario)

    # Incrementa o ID para o próximo usuário
    proximo_id += 1

    # Retorna o novo usuário criado com status 201 (Created)
    return jsonify(novo_usuario), 201

# Quando acessarem /usuarios/1 com método PUT, por exemplo
@app.route('/usuarios/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    # Pega os dados enviados no corpo da requisição
    dados = request.get_json()

    # Procura o usuário com o ID informado
    for usuario in usuarios:
        if usuario['id'] == id:
            # Atualiza o nome e idade, se foram enviados
            usuario['nome'] = dados.get('nome', usuario['nome'])
            usuario['idade'] = dados.get('idade', usuario['idade'])

            # Retorna o usuário atualizado
            return jsonify(usuario)

    # Se não encontrou nenhum usuário com o ID, retorna erro
    return jsonify({"erro": "Usuário não encontrado"}), 404


# Quando acessarem /usuarios/1 com método DELETE, por exemplo
@app.route('/usuarios/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    # Procura o usuário pelo ID
    for usuario in usuarios:
        if usuario['id'] == id:
            # Remove da lista
            usuarios.remove(usuario)

            # Retorna mensagem de sucesso
            return jsonify({"mensagem": f"Usuário {id} removido com sucesso!"})

    # Se não encontrou, retorna erro
    return jsonify({"erro": "Usuário não encontrado"}), 404

# Só roda o app se este arquivo for o principal
if __name__ == '__main__':
    app.run(debug=True)  # Inicia o servidor Flask com modo debug (útil pra desenvolvimento)
