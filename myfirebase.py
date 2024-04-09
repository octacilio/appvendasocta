import requests
from kivy.app import App
class MyFirebase():
    API_KEY = "AIzaSyACHCO5W0waay5l65wVbBg98f-mowfuYPI"

    def fazer_login(self, email, senha):
        link = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.API_KEY}"
        info = {"email" : email,
                "password" : senha,
                "returnSecureToken" : True}

        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()
        #        print(requisicao_dic)
        if requisicao.ok:
            print("usuario logado")
            requisicao_dic['idToken']  # autenticação
        #            requisicao_dic['email']
            requisicao_dic['refreshToken']  # Token que mantem o susario logado, salvar para fazer login
            requisicao_dic['localId']  # id usuario no banco firebase
            refresh_token = requisicao_dic['refreshToken']
            local_id = requisicao_dic['localId']
            id_token = requisicao_dic['idToken']
            meu_aplicativo = App.get_running_app()
            meu_aplicativo_local_id = local_id
            meu_aplicativo_id_token = id_token

            with open("refreshtoken.txt", "w") as arquivo:
                arquivo.write(refresh_token)

            meu_aplicativo.carregar_infos_usuario()
            meu_aplicativo.chamar_tela("homepage")

        else:
            mensagem_erro = requisicao_dic["error"]["message"]
            # get_running_app lhe da a classe principal do seu aplicativo, para pegar o self.root da pagina
            meu_aplicativo = App.get_running_app()
            pagina_login = meu_aplicativo.root.ids['loginpage']
            pagina_login.ids["mensagem_login"].text = mensagem_erro
            pagina_login.ids["mensagem_login"].color = (1, 0, 0, 1)
    #   print(requisicao_dic)

    #    https: // identitytoolkit.googleapis.com / v1 / accounts: signUp?key = [API_KEY]
# criação do usuario no cloud = https: // identitytoolkit.googleapis.com / v1 / accounts: signUp?key = [API_KEY]
    def criar_conta(self, email, senha):
        link = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.API_KEY}"

        info = {"email" : email,
                "password" : senha,
                "returnSecureToken" : True}
        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()
#        print(requisicao_dic)
        if requisicao.ok:
            print("usuario criado")
            requisicao_dic['idToken'] #  autenticação
#            requisicao_dic['email']
            requisicao_dic['refreshToken'] # Token que mantem o susario logado, salvar para fazer login
            requisicao_dic['localId'] # id usuario no banco firebase
            refresh_token = requisicao_dic['refreshToken']
            local_id = requisicao_dic['localId']
            id_token = requisicao_dic['idToken']
            meu_aplicativo = App.get_running_app()
            meu_aplicativo_local_id = local_id
            meu_aplicativo_id_token = id_token

            with open("refreshtoken.txt", "w") as arquivo:
                arquivo.write(refresh_token)

            req_id = requests.get(f"https://aplicativovendashash-968fe-default-rtdb.firebaseio.com/proximo_id_vendedor.json?auth={id_token}")
            id_vendedor = req_id.json()

            #criar usuario com patch
            link = f"https://aplicativovendashash-968fe-default-rtdb.firebaseio.com/{local_id}.json?auth={id_token}"

            info_usuario = f'{{"avatar" : "foto2.png", "equipe" : "", "total_vendas" : "0", "vendas" : "", "id_vendedor" : "{id_vendedor}"}}'
            requisicao_usuario = requests.patch(link, data=info_usuario)

            #atualizar o valor do proximo vendedor
            id_vendedor = int(id_vendedor) + 1
            info_id_vendedor = f'{{"proximo_id_vendedor": "{id_vendedor}"}}'
            requests.patch("https://aplicativovendashash-968fe-default-rtdb.firebaseio.com/.json?auth={id_token}",data=info_id_vendedor)

            meu_aplicativo.carregar_infos_usuario()
            meu_aplicativo.chamar_tela("homepage")
        else:
            mensagem_erro = requisicao_dic["error"]["message"]
            # get_running_app lhe da a classe principal do seu aplicativo, para pegar o self.root da pagina
            meu_aplicativo = App.get_running_app()
            pagina_login = meu_aplicativo.root.ids['loginpage']
            pagina_login.ids["mensagem_login"].text = mensagem_erro
            pagina_login.ids["mensagem_login"].color = (1, 0, 0, 1)
    #    print(requisicao_dic)

    def trocar_token(self, refresh_token):
        link = f"https://securetoken.googleapis.com/v1/token?key={self.API_KEY}"
        info = {"grant_type" : "refresh_token", "refresh_token" : refresh_token}
        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()
        #print(requisicao_dic)
        local_id = requisicao_dic['user_id']
        id_token = requisicao_dic['id_token']
        return (local_id, id_token)
