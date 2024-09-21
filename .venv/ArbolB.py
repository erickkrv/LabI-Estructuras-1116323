import json
from tkinter import filedialog
from tkinter import Tk

class Libro:
    def __init__(self, ISBN, titulo, autor, categoria, precio, stock):
        self.ISBN = ISBN
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria
        self.precio = precio
        self.stock = stock

    def get_ISBN(self):
        return self.ISBN

    def set_ISBN(self, ISBN):
        self.ISBN = ISBN

    def get_titulo(self):
        return self.titulo

    def set_titulo(self, titulo):
        self.titulo = titulo

    def get_categoria(self):
        return self.categoria

    def set_categoria(self, categoria):
        self.categoria = categoria

    def get_autor(self):
        return self.autor

    def set_autor(self, autor):
        self.autor = autor

    def get_precio(self):
        return self.precio

    def set_precio(self, precio):
        self.precio = precio

    def get_stock(self):
        return self.stock

    def set_stock(self, stock):
        self.stock = stock

    def __str__(self):
        return f'{{"isbn":"{self.ISBN}","name":"{self.titulo}","author":"{self.autor}","category":"{self.categoria}","price":"{self.precio}","quantity":"{self.stock}"}}'


class NodoArbolB:
    def __init__(self, t, leaf):
        self.t = t  # Grado mínimo
        self.leaf = leaf  # Si es hoja
        self.keys = [None] * (2 * t - 1)  # Array de libros
        self.C = [None] * (2 * t)  # Array de punteros a hijos
        self.n = 0  # Número actual de libros

    def find_key(self, isbn):
        idx = 0
        while idx < self.n and self.keys[idx].ISBN < isbn:
            idx += 1
        return idx

    def remove(self, isbn):
        idx = self.find_key(isbn)

        if idx < self.n and self.keys[idx].ISBN == isbn:
            if self.leaf:
                self.remove_from_leaf(idx)
            else:
                self.remove_from_non_leaf(idx)
        else:
            if self.leaf:
                # print(f"El libro con ISBN {isbn} no existe en el árbol")
                return

            flag = idx == self.n
            if idx < self.n and self.C[idx].n < self.t:
                self.fill(idx)

            if flag and idx > self.n:
                self.C[idx - 1].remove(isbn)
            else:
                self.C[idx].remove(isbn)

    def remove_from_leaf(self, idx):
        for i in range(idx + 1, self.n):
            self.keys[i - 1] = self.keys[i]
        self.n -= 1

    def remove_from_non_leaf(self, idx):
        libro = self.keys[idx]

        if self.C[idx].n >= self.t:
            pred = self.get_pred(idx)
            self.keys[idx] = pred
            self.C[idx].remove(pred.ISBN)
        elif self.C[idx + 1].n >= self.t:
            succ = self.get_succ(idx)
            self.keys[idx] = succ
            self.C[idx + 1].remove(succ.ISBN)
        else:
            self.merge(idx)
            self.C[idx].remove(libro.ISBN)

    def get_pred(self, idx):
        cur = self.C[idx]
        while not cur.leaf:
            cur = cur.C[cur.n]
        return cur.keys[cur.n - 1]

    def get_succ(self, idx):
        cur = self.C[idx + 1]
        while not cur.leaf:
            cur = cur.C[0]
        return cur.keys[0]

    def fill(self, idx):
        if idx != 0 and self.C[idx - 1].n >= self.t:
            self.borrow_from_prev(idx)
        elif idx != self.n and self.C[idx + 1].n >= self.t:
            self.borrow_from_next(idx)
        else:
            if idx != self.n:
                self.merge(idx)
            else:
                self.merge(idx - 1)

    def borrow_from_prev(self, idx):
        child, sibling = self.C[idx], self.C[idx - 1]

        for i in range(child.n - 1, -1, -1):
            child.keys[i + 1] = child.keys[i]

        if not child.leaf:
            for i in range(child.n, -1, -1):
                child.C[i + 1] = child.C[i]

        child.keys[0] = self.keys[idx - 1]

        if not child.leaf:
            child.C[0] = sibling.C[sibling.n]

        self.keys[idx - 1] = sibling.keys[sibling.n - 1]

        child.n += 1
        sibling.n -= 1

    def borrow_from_next(self, idx):
        child, sibling = self.C[idx], self.C[idx + 1]

        child.keys[child.n] = self.keys[idx]

        if not child.leaf:
            child.C[child.n + 1] = sibling.C[0]

        self.keys[idx] = sibling.keys[0]

        for i in range(1, sibling.n):
            sibling.keys[i - 1] = sibling.keys[i]

        if not sibling.leaf:
            for i in range(1, sibling.n + 1):
                sibling.C[i - 1] = sibling.C[i]

        child.n += 1
        sibling.n -= 1

    def merge(self, idx):
        child, sibling = self.C[idx], self.C[idx + 1]

        child.keys[self.t - 1] = self.keys[idx]

        for i in range(sibling.n):
            child.keys[i + self.t] = sibling.keys[i]

        if not child.leaf:
            for i in range(sibling.n + 1):
                child.C[i + self.t] = sibling.C[i]

        for i in range(idx + 1, self.n):
            self.keys[i - 1] = self.keys[i]

        for i in range(idx + 2, self.n + 1):
            self.C[i - 1] = self.C[i]

        child.n += sibling.n + 1
        self.n -= 1

    def insert_non_full(self, libro):
        i = self.n - 1

        if self.leaf:
            while i >= 0 and self.keys[i].ISBN > libro.ISBN:
                self.keys[i + 1] = self.keys[i]
                i -= 1

            self.keys[i + 1] = libro
            self.n += 1
        else:
            while i >= 0 and self.keys[i].ISBN > libro.ISBN:
                i -= 1

            i += 1
            if self.C[i].n == (2 * self.t - 1):
                self.split_child(i, self.C[i])

                if self.keys[i].ISBN < libro.ISBN:
                    i += 1

            self.C[i].insert_non_full(libro)

    def split_child(self, i, y):
        z = NodoArbolB(y.t, y.leaf)
        z.n = self.t - 1

        for j in range(self.t - 1):
            z.keys[j] = y.keys[j + self.t]

        if not y.leaf:
            for j in range(self.t):
                z.C[j] = y.C[j + self.t]

        y.n = self.t - 1

        for j in range(self.n, i, -1):
            self.C[j + 1] = self.C[j]

        self.C[i + 1] = z

        for j in range(self.n - 1, i - 1, -1):
            self.keys[j + 1] = self.keys[j]

        self.keys[i] = y.keys[self.t - 1]
        self.n += 1

    def traverse(self):
        i = 0
        while i < self.n:
            if not self.leaf:
                self.C[i].traverse()
            print(self.keys[i].ISBN, self.keys[i].titulo, end=" | ")
            i += 1

        if not self.leaf:
            self.C[i].traverse()

    def search(self, isbn):
        i = 0
        while i < self.n and isbn > self.keys[i].ISBN:
            i += 1

        if i < self.n and self.keys[i].ISBN == isbn:
            return self.keys[i]

        if self.leaf:
            return None

        return self.C[i].search(isbn)

class ArbolB:
    def __init__(self, t):
        self.root = None  # Puntero a la raíz
        self.t = t  # Grado mínimo
        self.name_to_isbn = {} # Diccionario para buscar por nombre

    def traverse(self):
        if self.root:
            self.root.traverse()
            print()


    def search(self, isbn):
        if self.root is not None:
            return self.root.search(isbn)
        return None

    def insert(self, libro):
        if not self.root:
            self.root = NodoArbolB(self.t, True)
            self.root.keys[0] = libro
            self.root.n = 1
        else:
            if self.root.n == (2 * self.t - 1):
                s = NodoArbolB(self.t, False)
                s.C[0] = self.root
                s.split_child(0, self.root)

                i = 0
                if s.keys[0].ISBN < libro.ISBN:
                    i += 1

                s.C[i].insert_non_full(libro)
                self.root = s
            else:
                self.root.insert_non_full(libro)
        self.name_to_isbn[libro.titulo] = libro.ISBN

    def remove(self, isbn):
        if not self.root:
            #print("El árbol está vacío")
            return

        self.root.remove(isbn)

        if self.root.n == 0:
            tmp = self.root
            if self.root.leaf:
                self.root = None
            else:
                self.root = self.root.C[0]

            del tmp

    def update(self, datos):
        ISBN = datos["isbn"]
        libro = self.search(ISBN)
        if libro is None:
            return
        if "name" in datos:
            self.name_to_isbn.pop(libro.titulo)
            libro.titulo = datos["name"]
            self.name_to_isbn[libro.titulo] = ISBN
        if "author" in datos:
            libro.autor = datos["author"]
        if "category" in datos:
            libro.categoria = datos["category"]
        if "price" in datos:
            libro.precio = datos["price"]
        if "quantity" in datos:
            libro.stock = datos["quantity"]

    def searchByName(self, name):
        isbn = self.name_to_isbn.get(name)
        if isbn is not None:
            return self.search(isbn)
        return None


def main():
    arbol = ArbolB(5)
    while True:
        print("Laboratorio 1 Erick Rivas")
        print("1. Importar CSV")
        print("2. Salir")
        opcion = input("Ingrese una opción: ")
        if opcion == '1':
            importar_libros(arbol)
        elif opcion == '2':
            print("Saliendo...")
            exit(0)
        else:
            print("Opción inválida")

def importar_libros(arbol):
    ultima_linea = ""
    root = Tk()
    root.withdraw()
    archivo_seleccionado = filedialog.askopenfilename(filetypes=[("Archivo CSV", "*.csv"), ("Todos los archivos", "*")])

    if archivo_seleccionado:
        try:
            with open(archivo_seleccionado, 'r') as f, open('libros_encontrados.txt', 'w') as writer:
                procesados = 0
                insertados = 0
                busquedas_hechas = 0
                operacion_actual = ""

                for linea in f:
                    ultima_linea = linea
                    procesados += 1

                    if linea.startswith("INSERT;"):
                        operacion_actual = "INSERT"
                        insertados += 1
                        datos = json.loads(linea[7:].strip())
                        libro = Libro(datos["isbn"], datos["name"], datos["author"], datos["category"], datos["price"], datos["quantity"])
                        arbol.insert(libro)

                    elif linea.startswith("DELETE;"):
                        operacion_actual = "DELETE"
                        datos = json.loads(linea[7:].strip())
                        arbol.remove(datos["isbn"])

                    elif linea.startswith("PATCH;"):
                        operacion_actual = "PATCH"
                        datos = json.loads(linea[6:].strip())
                        arbol.update(datos)

                    elif linea.startswith("SEARCH;"):
                        operacion_actual = "SEARCH"
                        datos = json.loads(linea[7:].strip())
                        libro = arbol.searchByName(datos["name"])

                        if libro is not None:
                            busquedas_hechas += 1
                            writer.write(str(libro) + "\n")
                            print("Busquedas encontradas: " + str(busquedas_hechas))

            print("CSV importado correctamente")

        except Exception as e:
            print(f"Error al importar los libros: {str(e)} en la línea: {ultima_linea}")

if __name__ == "__main__":
    main()