import argparse
import sys


class Cifra():
    CLI_VERSION = "0.0.1"

    def __init__(self):
        self.__run()

    def __run(self):

        self.parser = argparse.ArgumentParser(
            prog='Cifra de Playfair',
            description='Criptografia usando a cifra de Playfair',
            epilog='Desenvolvido por: @meiazero',
            usage='%(prog)s [options] [path] [key]')

        self.parser.version = self.CLI_VERSION

        self.parser.add_argument("-v", "--version", action="version")

        self.parser.add_argument(
            "-d", "--dir", type=str, help="Diretório do arquivo de texto", required=True)

        self.parser.add_argument(
            "-k", "--key", type=str, help="Chave de criptografia", required=True)

        args_parser = self.__args()

        if args_parser:
            try:
                tokens = self.__textToToken(args_parser.dir)
                print(f"Tokens: {tokens}")

                key = self.__clearKey(args_parser.key)
                print(f"Chave: {key}")

                matrix = self.__matrixKey(key)
                print(f"Matriz: {matrix}")

                # encriptar a mensagem
                cifra = self.__encrypt(tokens, matrix)
                print(f"cifra: {cifra}")

            except Exception as e:
                print(e)

    def __args(self):
        return self.parser.parse_args()

    def __textToToken(self, path) -> list:
        self.path = path
        # transform the text in tokens
        tokens = []
        file = open(self.path, 'r')
        text = file.read()

        # transforma o texto em maiúsculo
        text = text.upper()

        # remove os caracteres especiais
        text = ''.join(e for e in text if e.isalnum())

        # remove os espaços e substitui por x
        text = text.replace(" ", "X")

        # verifica se há a letra I ou J e substitui por I/J
        text = text.replace("I", "IJ")

        # verifica se há caracteres repetidos e adiciona um X entre eles
        for i in range(0, len(text)-1, 2):
            if text[i] == text[i+1]:
                text = text[:i+1] + "X" + text[i+1:]

        # verifica se o texto possui um número ímpar de caracteres e adiciona um X no final
        if len(text) % 2 != 0:
            text += "X"

        # remove os números do texto
        text = ''.join(e for e in text if not e.isdigit())

        file.close()

        # transforma o texto em tokens
        tokens = self.__ifIsIorJ(tokens, text)

        # transforma a lista em uma lista de duplas
        # tokens = [tokens[i:i+2] for i in range(0, len(tokens), 2)]

        # separa as letras em pares caso haja a letra I/J faz um trio
        tokens = [tokens[i:i+3] if tokens[i] == "IJ" else tokens[i:i+2]
                  for i in range(0, len(tokens), 2)]

        return tokens

    def __ifIsIorJ(self, tokens, text):
        self.tokens = tokens
        self.text = text

        if self.text == "I" or self.text == "J":
            self.tokens.append("IJ")
        else:
            for letter in self.text:
                self.tokens.append(letter)

        return self.tokens

    def __clearKey(self, key) -> str:
        self.key = key

        # rejeita a chave se ela conter algum caractere especial ou número ou conter espaços
        if self.key != ''.join(e for e in self.key if e.isalnum()) or self.key.find(" ") != -1:
            raise Exception("A chave não pode ser usada!")

        # transforma a chave em maiúscula
        self.key = self.key.upper()

        # remove as duplicatas da chave
        self.key = ''.join(dict.fromkeys(self.key))

        return self.key

    def __matrixKey(self, key) -> list:
        self.key = key

        # cria a matriz de cifragem
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

        matrix = []
        # remove os caracteres repetidos do alfabeto com a chave
        for i in self.key:
            alphabet = alphabet.replace(i, "")

        # adiciona a chave na matriz
        for i in self.key:
            matrix.append(i)

        # adiciona o alfabeto na matriz
        for i in alphabet:
            matrix.append(i)

        # transforma a matriz em uma matriz 5x5
        matrix = [matrix[i:i+5] for i in range(0, len(matrix), 5)]

        return matrix

    def __encrypt(self, tokens, matrix) -> str:
        # encrypt the tokens with the key using the Playfair algorithm
        self.tokens = tokens
        self.matrix = matrix
        coordenadas = []

        #  busca a linha da primeira letra do par se encontra com a coluna da segunda letra
        for linha in range(0, 5):
            for coluna in range(0, 5):
                if self.tokens[0][1] == self.matrix[linha][coluna]:
                    coordenadas.append(linha+1)
                    coordenadas.append(coluna+1)

        return coordenadas

        # TODO: O código acima deve buscar por linha e coluna do par de letras.
