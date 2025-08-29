# Projeto de Automação Web: Verificação de Conexão de Internet via Speed Test
 - Objetivo: aplicar automação web de maneira prática, sendo este um código onde pode auxiliar no cotidiano de todos os usuários de internet para manter um histórico registrado de informações básicas da qualidade do sinal de internet, caso por ventura precise realizar alguma reclamação com a empresa provedora do serviço, ou queira comparar qualidade e simplesmente trocar a empresa que utiliza em sua residência, trabalho, ou qualquer outro ambiuente de convívio;
 - automacao_pura.ipynb -> Código da automação pura (arquivo notebook) ;
 - main.py -> Código com interface gráfica (utilizando flet).

# Dicas Iniciais:
 - Passo 1: Crie um ambiente virtual (trazendo um Python puro para sua pasta) -> py -m venv venv
 - Passo 2: Ativação do ambiente virtual criado -> \venv\Scripts\activate [ Na prática escreva: ve(aperta tab)sc(aperta tab)ac(aperta tab) ]
 
 - OBS-1: Caso dê errado e não dê nenhum aviso, tente: .\venv\Scripts\Activate.ps1 [ Na prática escreva: ve(aperta tab)sc(aperta tab)ac(aperta tab) e complete escrevendo .ps1 ]
 
 - Passo 3: Execute o seguinte comando para instalar todas as bibliotecas de uma única vez -> pip install -r \requirements.txt [ Na prática escreva: pip install -r req(aperta tab) ]

 # Ajustando Política de Privacidade:
 - OBS-2: Caso não esteja autorizando, é necessário executar o powershell como adm e verificar :
 
 - Get-ExecutionPolicy
 - Se estiver dando como restrito, utilizar este comando e autorizar -> Set-ExecutionPolicy Unrestricted
 - Depois se quiser reotrnar para política restrita utilizando -> Set-ExecutionPolicy Restricted

# Convertendo Para Executável Windows:
 - Para converter o código com flet para um executável windows, basta abrir o terminal do seu editor de código (vscode ou cursor) pressionando crtl+j e executando -> pyinstaller --onefile --windowed main.py
