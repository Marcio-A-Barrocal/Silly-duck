# 🦆 Silly Duck
Bem-vindo ao Silly Duck! Um patinho digital amigável e um pouco bobo que passeia pela sua área de trabalho, trazendo um pouco de diversão e caos para o seu dia.

![Silly_Duck](https://github.com/user-attachments/assets/4d8c8dfa-f364-4440-b947-45447761cbed)

## Descrição
Silly Duck é um "desktop pet" (mascote de área de trabalho) desenvolvido em Python. Ele é um pato animado que anda de um lado para o outro na tela, interage com o cursor do mouse e até **reage a cliques**. É um projeto simples e divertido, perfeito para quem quer um companheiro virtual enquanto estuda ou trabalha.

## Funcionalidades Principais
* **Animação de caminhada:** O pato passeia pela sua tela de forma autônoma.
* **Interação com o mouse:** Fique de olho no seu cursor! O pato pode decidir segui-lo ou fugir dele.
* **Pato Assustado:** Experimente clicar no pato e veja ele sair correndo pela tela!
* **Comportamentos aleatórios:** Para tornar a experiência mais dinâmica, o pato tem momentos de descanso e ações inesperadas.
* **Leve e fácil de executar:** Não consome muitos recursos do sistema.

## Tecnologias Utilizadas
Este projeto foi construído utilizando Python e as seguintes bibliotecas principais:
* **Pillow:** Para manipulação de imagens e animações.
* **PyAutoGUI:** Para controlar o mouse e obter informações da tela, permitindo a interação do pato com o ambiente de trabalho.
* **PyGetWindow:** Para gerenciar e encontrar a janela do pato na tela.

## Como Executar o Projeto
Para ter o patinho andando na sua tela, siga os passos abaixo.

**Pré-requisitos:**
* Ter o [Python 3](https://www.python.org/downloads/) instalado.
* Ter o [Git](https://git-scm.com/downloads) instalado para clonar o repositório.

**Passos:**
1.  **Clone este repositório:**
    ```bash
    git clone https://github.com/Marcio-A-Barrocal/Silly-duck.git
    cd Silly-duck
    ```
2.  **(Recomendado) Crie e ative um ambiente virtual:**
    Isso isola as dependências do projeto e evita conflitos.
    ```bash
    # No Windows
    python -m venv venv
    .\venv\Scripts\activate
    # No macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Instale as dependências:**
    O arquivo `requirements.txt` já contém todas as bibliotecas necessárias. Execute o comando abaixo:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Execute o Silly Duck!**
    ```bash
    python main.py
    ```
    E pronto! O patinho deve aparecer na sua tela. Tente clicar nele!

## Como Contribuir
Ficou com alguma ideia para deixar o pato ainda mais divertido? Contribuições são super bem-vindas!
1.  Faça um **Fork** deste repositório.
2.  Crie uma nova **Branch** (`git checkout -b feature/PatoDancante`).
3.  Faça o **Commit** das suas alterações (`git commit -m 'Adiciona uma dança maneira para o pato'`).
4.  Envie para a sua Branch (`git push origin feature/PatoDancante`).
5.  Abra um **Pull Request**.
