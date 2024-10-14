from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Armazenar múltiplos chats na memória
chats = {}  # {chat_id: chat_history}

# Respostas do chatbot
responses = {
    "Mapa de Coleta Seletiva em Belém": {
        "Amarelo, Vermelho e Azul": "Feira Bandeira Branca – Almirante Barroso com Drº Freitas\nPraça da Republica – Campina\nPraça Batista Campos – Batista Campos\nCarramachão Mosqueiro – Mosqueiro",
        "Verde": "Contêiner VERDE - Material Reciclável Misturado\nIgrejra Quadrangular – Timbó – Pedreira\nPraça Brasil – Umarizal\nPraça Dom Pedro – Cidade Velha\nPraça Felipe Patroni – Cidade velha\nArthur Bernardes – Próximo a Igreja N. Se. Do Perpetuo Socorro\nPraça Jaú – Sacramenta\nPraça da Bandeira – Campina\nPraça Amazonas – Jurunas\nPraça Floriano Peixoto – em frente ao Mercado de São Braz\nVER O RIO – Umarizal\nPraça Estivadores – Memorial dos 400 anos (Próximo ao Sesc Boulevard) Campina\nVer-o-peso – Comercio\nHorto Municipal – Batista Campos\nDoca de Souza Franco (Na frente do shopping Boulevard) – Doca\nPraça Marex – Val de Cans\nMosqueiro (Vila) – Mosqueiro\nMosqueiro (Morumbira) – Mosqueiro\nAlcindo Cacela – Unama – Umarizal\nConjunto Tapajós – Rua Alicante, ao lado do Antigo Posto Policial\n\nContêiner VERDE – IGLU material reciclável misturado\nResidencial Viver Primavera – Rodovia do Tapanã\nIcoaraci – Rua Manoel Barata – Icoaraci\nPraça D. Alberto Ramos – Marambaia\nOrla – Praia Grande – Outeiro\nEscola Bosque – Outeiro\nBosque Rodrigues Alves – Marco\nPraça Benedito Monteiro – Guamá\nAntônio Baena – Feira da 25 (final) – Marco\nSESAN – sede Alm. Barroso – Souza",
        "Lixo eletrônico": "Horto Municipal\nMercado de São Brás\nDoca com Antônio Barreto (Praça Pet)\nParque Shopping Belém (Augusto Montenegro)"
    },
    "Descarte de Materiais Recicláveis": {
        "Materiais Recicláveis": {
            "Plásticos": "Devem ser lavados, secos e descartados em locais específicos para coleta seletiva. Saiba onde encontrar pontos de descarte em 'Mapa de Coleta Seletiva em Belém'.",
            "Papel e Papelão": "Devem estar secos e não engordurados. Podem ser levados a centros de reciclagem e pontos de coleta. Saiba onde encontrar pontos de descarte em 'Mapa de Coleta Seletiva em Belém'.",
            "Metais": "Latas de alumínio e aço podem ser entregues em centros de reciclagem. Sucata metálica pode ser vendida em ferros-velhos ou levada a cooperativas de catadores. Saiba onde encontrar pontos de descarte em 'Mapa de Coleta Seletiva em Belém'.",
            "Vidros": "Devem ser limpos e separados por cor (verde, âmbar, incolor). O descarte é feito em pontos de coleta, já que o vidro não se decompõe facilmente. O cuidado desse material deve ser redobrado para evitar acidentes. Saiba onde encontrar pontos de descarte em 'Mapa de Coleta Seletiva em Belém'."
        },
        "Resíduos Orgânicos": {
            "Restos de alimentos e vegetais": "Podem ser destinados à compostagem, transformando-se em adubo natural.",
            "Restos de poda e jardinagem": "Podem ser compostados ou levados a ecopontos que aceitam resíduos verdes."
        },
        "Resíduos Perigosos": {
            "Eletrônicos (e-lixo)": "Devem ser levados a pontos de coleta específicos para eletrônicos. Saiba onde encontrar pontos de descarte em 'Mapa de Coleta Seletiva em Belém'.",
            "Pilhas e Baterias": "A recomendação é entregá-las em pontos de coleta específicos, como em estabelecimentos comerciais que oferecem essa opção ou nos mesmos pontos de descarte de eletrônicos. Saiba onde encontrar pontos de descarte em 'Mapa de Coleta Seletiva em Belém'.",
            "Resíduos Hospitalares": "Devem ser descartados em pontos de coleta específicos (hospitais, clínicas) ou em campanhas de coleta da prefeitura, para tratamento e incineração adequados.",
            "Produtos Químicos": "Devem ser levados a ecopontos ou a empresas especializadas na destinação desses materiais, nunca lançados no esgoto ou no solo."
        },
        "Entulhos da Construção Civil": {
            "Concreto, tijolos, telhas": "Podem ser levados a empresas de reciclagem de entulho ou ecopontos. Em alguns casos, esses materiais podem ser reutilizados em obras, como em bases para pavimentação.",
            "Madeiras": "Podem ser reaproveitadas ou levadas a cooperativas e pontos de descarte para reciclagem ou transformação em biomassa."
        },
        "Resíduos Orgânicos Industriais": {
            "Subprodutos industriais": "Devem ser tratados por empresas especializadas em tratamento de resíduos industriais. Alguns podem ser usados na geração de biogás ou compostagem industrial."
        },
        "Resíduos têxteis": {
            "Tecidos e sobras de confecções": "Podem ser levados a empresas de reciclagem têxtil ou cooperativas que fazem o reaproveitamento de materiais. Algumas indústrias da moda têm programas de recolhimento. Saiba onde encontrar pontos de descarte em 'Mapa de Coleta Seletiva em Belém'.",
            "Roupas usadas": "Podem ser doadas para instituições ou projetos sociais, ou levadas a pontos de coleta para reciclagem. Saiba onde encontrar pontos de descarte em 'Mapa de Coleta Seletiva em Belém'."
        },
        "Lixo Comum (Resíduo não reciclável)": {
            "Exemplos de Lixo Comum": "Papel sujo, guardanapos usados, absorventes, fraldas descartáveis, restos de alimentos não compostáveis (como ossos e cascas de ovos), embalagens contaminadas com gordura ou resíduos.",
            "Descarte de Lixo Comum": "Deve ser descartado em lixeiras comuns e encaminhado para aterros sanitários. Esse lixo não pode ser reciclado ou compostado."
        },
        "Resíduos radioativos": {
            "Exemplos de Resíduos Radioativos": "Equipamentos de radiologia, resíduos de tratamentos oncológicos, resíduos de usinas nucleares.",
            "Descarte de Resíduos Radioativos": "Esse tipo de resíduo requer tratamento e descarte altamente controlados, realizado por instituições especializadas. Eles são armazenados em locais apropriados, como depósitos subterrâneos ou em instalações de contenção, por longos períodos, devido ao risco de contaminação."
        }
    }
}

# Função para gerar respostas baseadas na entrada do usuário
def rule_based_response(user_message):
    # Primeira pergunta principal: Mapa de Coleta Seletiva em Belém
    if user_message == "Mapa de Coleta Seletiva em Belém":
        return "Escolha uma das opções: Amarelo, Vermelho e Azul / Verde / Lixo eletrônico"
    
    # Segunda pergunta principal: Descarte de Materiais Recicláveis
    elif user_message == "Descarte de Materiais Recicláveis":
        return "Escolha uma das opções: Materiais Recicláveis / Resíduos Orgânicos / Resíduos Perigosos / Entulhos da Construção Civil / Resíduos Orgânicos Industriais / Resíduos têxteis / Lixo Comum (Resíduo não reciclável) / Resíduos radioativos"
    
    # Função para navegar pelo dicionário de perguntas e respostas
    def find_response(category, message):
        if isinstance(category, dict):
            if message in category:
                return category[message]
            for key, subcategory in category.items():
                if isinstance(subcategory, dict):
                    result = find_response(subcategory, message)
                    if result:
                        return result
        return None

    # Verifica se a pergunta está dentro de "Mapa de Coleta Seletiva em Belém"
    response = find_response(responses["Mapa de Coleta Seletiva em Belém"], user_message)
    if response:
        return response if not isinstance(response, dict) else "Escolha uma das opções: " + " / ".join(response.keys())

    # Verifica se a pergunta está dentro de "Descarte de Materiais Recicláveis"
    response = find_response(responses["Descarte de Materiais Recicláveis"], user_message)
    if response:
        return response if not isinstance(response, dict) else "Escolha uma das opções: " + " / ".join(response.keys())
    
    return "Desculpe, não entendi. Por favor, escolha uma opção válida."

# Rota principal
@app.route('/')
def home():
    return render_template('index.html')

# Rota para enviar mensagens para um chat específico
@app.route('/send_message', methods=['POST'])
def send_message():
    chat_id = request.form['chat_id']
    user_message = request.form['message']
    bot_response = rule_based_response(user_message)
    
    # Adicionar a mensagem e a resposta ao histórico do chat especificado
    if chat_id in chats:
        chats[chat_id].append({'user': user_message, 'bot': bot_response})
    else:
        chats[chat_id] = [{'user': user_message, 'bot': bot_response}]

    return jsonify({'bot_response': bot_response, 'chat_history': chats[chat_id]})

# Rota para iniciar um novo chat
@app.route('/new_chat', methods=['POST'])
def new_chat():
    # Criar um novo ID de chat com base no timestamp
    chat_id = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    chats[chat_id] = []  # Inicializar o histórico de chat vazio

    # Mensagem de boas-vindas com as perguntas principais
    welcome_message = "Seja bem vindo(a) ao Eco Assistant! Por favor, escolha uma das seguintes opções:\n1. Mapa de Coleta Seletiva em Belém\n2. Descarte de Materiais Recicláveis"
    chats[chat_id].append({'user': 'Mensagem Inicial:', 'bot': welcome_message})

    return jsonify({'message': 'Novo chat iniciado com sucesso!', 'chat_id': chat_id, 'bot_response': welcome_message})

# Rota para obter o histórico de um chat específico
@app.route('/get_chat_history', methods=['GET'])
def get_chat_history():
    chat_id = request.args.get('chat_id')
    if chat_id in chats:
        return jsonify({'chat_history': chats[chat_id]})
    else:
        return jsonify({'chat_history': []})

# Rota para obter a lista de todos os chats
@app.route('/get_all_chats', methods=['GET'])
def get_all_chats():
    return jsonify({'chats': list(chats.keys())})

# Rota para excluir um chat
@app.route('/delete_chat', methods=['POST'])
def delete_chat():
    chat_id = request.form['chat_id']
    if chat_id in chats:
        del chats[chat_id]
        return jsonify({'message': f'Chat {chat_id} excluído com sucesso!'})
    else:
        return jsonify({'message': 'Chat não encontrado.'})

if __name__ == "__main__":
    app.run(debug=True)
