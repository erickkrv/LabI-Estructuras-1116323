import json
from tkinter import filedialog
from tkinter import Tk


class Libro:
    # Constructor de la clase Libro
    def __init__(self, ISBN, titulo, autor, categoria, precio, stock):
        self.ISBN = ISBN
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria
        self.precio = precio
        self.stock = stock

    # Métodos get y set de la clase Libro
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

    # Método para imprimir el objeto Libro
    def __str__(self):
        return f'{{"isbn":"{self.ISBN}","name":"{self.titulo}","author":"{self.autor}","category":"{self.categoria}","price":"{self.precio}","quantity":"{self.stock}"}}'


class NodoArbolB:
    # Constructor de la clase NodoArbolB
    def __init__(self, t, leaf):
        self.t = t  # Grado mínimo
        self.leaf = leaf  # Si es hoja
        self.keys = [None] * (2 * t - 1)  # Array de libros
        self.C = [None] * (2 * t)  # Array de punteros a hijos
        self.n = 0  # Número actual de libros

    # Método para recorrer el árbol y encontrar un isbn
    def find_key(self, isbn):
        idx = 0
        while idx < self.n and self.keys[idx].ISBN < isbn:
            idx += 1
        return idx

    # Método para eliminar un libro
    def remove(self, isbn):
        # Encontrar el índice del libro
        idx = self.find_key(isbn)

        # Si el índice es menor que el número de libros y el isbn es igual al isbn del libro
        if idx < self.n and self.keys[idx].ISBN == isbn:
            # Si es hoja
            if self.leaf:
                self.remove_from_leaf(idx)
            else:
                self.remove_from_non_leaf(idx)
        else:
            # Si es hoja
            if self.leaf:
                # print(f"El libro con ISBN {isbn} no existe en el árbol")
                return
            # Flag para saber si el índice es igual al número de libros
            flag = idx == self.n
            # Si el número de libros en el nodo es menor que el grado mínimo
            if idx < self.n and self.C[idx].n < self.t:
                # Llenar el nodo
                self.fill(idx)

            # Si el índice es mayor que el número de libros y el flag es verdadero
            if flag and idx > self.n:
                # Eliminar el libro del nodo hijo anterior
                self.C[idx - 1].remove(isbn)
            else:
                self.C[idx].remove(isbn)

    # Método para eliminar un libro de un nodo hoja
    def remove_from_leaf(self, idx):
        # Mover todos los libros después del índice
        for i in range(idx + 1, self.n):
            self.keys[i - 1] = self.keys[i]
        # Reducir el número de libros
        self.n -= 1

    # Método para eliminar un libro de un nodo no hoja
    def remove_from_non_leaf(self, idx):
        # Libro actual
        libro = self.keys[idx]

        # Si el hijo tiene al menos t libros
        if self.C[idx].n >= self.t:
            pred = self.get_pred(idx)  # Obtiene el predecesor
            self.keys[idx] = pred
            self.C[idx].remove(pred.ISBN)  # Elimina el predecesor
        elif self.C[idx + 1].n >= self.t:
            succ = self.get_succ(idx)  # Obtiene el sucesor
            self.keys[idx] = succ
            self.C[idx + 1].remove(succ.ISBN)  # Elimina el sucesor
        else:
            self.merge(idx)  # Si no hay predecesor ni sucesor, se hace merge
            self.C[idx].remove(libro.ISBN)

    # Método para obtener el predecesor
    def get_pred(self, idx):
        cur = self.C[idx]
        while not cur.leaf:  # Mientras no sea hoja
            cur = cur.C[cur.n]
        return cur.keys[cur.n - 1]  # Retorna el último libro

    # Método para obtener el sucesor
    def get_succ(self, idx):
        cur = self.C[idx + 1]
        while not cur.leaf:  # Mientras no sea hoja
            cur = cur.C[0]
        return cur.keys[0]  # Retorna el primer libro

    # Método para llenar un nodo
    def fill(self, idx):
        if idx != 0 and self.C[idx - 1].n >= self.t:
            self.borrow_from_prev(idx)  # Prestar del nodo anterior
        elif idx != self.n and self.C[idx + 1].n >= self.t:
            self.borrow_from_next(idx)  # Prestar del nodo siguiente
        else:
            if idx != self.n:
                self.merge(idx)  # Si no se puede prestar, hacer merge con el siguiente
            else:
                self.merge(idx - 1)

    # Método para prestar del nodo anterior
    def borrow_from_prev(self, idx):
        child, sibling = self.C[idx], self.C[idx - 1]

        for i in range(child.n - 1, -1, -1):  # Mover todos los libros del nodo hijo
            child.keys[i + 1] = child.keys[i]

        if not child.leaf:  # Si no es hoja, mover todos los hijos
            for i in range(child.n, -1, -1):
                child.C[i + 1] = child.C[i]

        child.keys[0] = self.keys[idx - 1]  # Mueve el libro del nodo padre al nodo hijo

        if not child.leaf:
            child.C[0] = sibling.C[sibling.n]  # Mueve el ultimo hijo del nodo hermano al primer hijo del nodo hijo

        self.keys[idx - 1] = sibling.keys[sibling.n - 1]  # Mueve el último libro del nodo hermano al nodo padre

        child.n += 1  # Aumenta el número de libros del nodo hijo
        sibling.n -= 1  # Disminuye el número de libros del nodo hermano

    # Método para prestar del nodo siguiente
    def borrow_from_next(self, idx):
        child, sibling = self.C[idx], self.C[idx + 1]

        child.keys[child.n] = self.keys[idx]  # Mueve el libro del nodo padre al nodo hijo

        if not child.leaf:
            child.C[child.n + 1] = sibling.C[0]  # Mueve el primer hijo del nodo hermano al último hijo del nodo hijo

        self.keys[idx] = sibling.keys[0]  # Mueve el primer libro del nodo hermano al nodo padre

        for i in range(1, sibling.n):
            sibling.keys[i - 1] = sibling.keys[i]  # Mueve todos los libros del nodo hermano

        if not sibling.leaf:  # Si no es hoja, mover todos los hijos
            for i in range(1, sibling.n + 1):
                sibling.C[i - 1] = sibling.C[i]

        child.n += 1  # Aumenta el número de libros del nodo hijo
        sibling.n -= 1  # Disminuye el número de libros del nodo hermano

    # Método para hacer merge
    def merge(self, idx):
        child, sibling = self.C[idx], self.C[idx + 1]

        child.keys[self.t - 1] = self.keys[idx]  # Mueve el libro del nodo padre al nodo hijo

        for i in range(sibling.n):
            child.keys[i + self.t] = sibling.keys[i]  # Mueve todos los libros del nodo hermano al nodo hijo

        if not child.leaf:
            for i in range(sibling.n + 1):
                child.C[i + self.t] = sibling.C[i]  # Mueve todos los hijos del nodo hermano al nodo hijo

        for i in range(idx + 1, self.n):
            self.keys[i - 1] = self.keys[i]  # Mueve todos los libros del nodo padre

        for i in range(idx + 2, self.n + 1):
            self.C[i - 1] = self.C[i]  # Mueve todos los hijos del nodo padre

        child.n += sibling.n + 1  # Aumenta el número de libros del nodo hijo
        self.n -= 1  # Disminuye el número de libros del nodo padre

    # Método para insertar un libro en un nodo no lleno
    def insert_non_full(self, libro):
        i = self.n - 1

        if self.leaf:
            while i >= 0 and self.keys[i].ISBN > libro.ISBN:
                self.keys[i + 1] = self.keys[i]  # Mueve los libros
                i -= 1

            self.keys[i + 1] = libro  # Inserta el libro
            self.n += 1  # Aumenta el número de libros
        else:
            while i >= 0 and self.keys[i].ISBN > libro.ISBN:  # Encuentra el hijo
                i -= 1

            i += 1
            if self.C[i].n == (2 * self.t - 1):
                self.split_child(i, self.C[i])  # Divide el nodo si está lleno

                if self.keys[i].ISBN < libro.ISBN:
                    i += 1

            self.C[i].insert_non_full(libro)  # Inserta el libro en el hijo adecuado

    # Método para dividir un nodo
    def split_child(self, i, y):
        z = NodoArbolB(y.t, y.leaf)
        z.n = self.t - 1

        for j in range(self.t - 1):
            z.keys[j] = y.keys[j + self.t]  # Copia la mitad de los libros al nuevo nodo

        if not y.leaf:
            for j in range(self.t):
                z.C[j] = y.C[j + self.t]  # Mueve los hijos si no es hoja

        y.n = self.t - 1  # Actualiza el número de libros en el nodo original

        for j in range(self.n, i, -1):
            self.C[j + 1] = self.C[j]  # Mueve los hijos

        self.C[i + 1] = z  # Inserta el nuevo nodo en el nodo padre

        for j in range(self.n - 1, i - 1, -1):
            self.keys[j + 1] = self.keys[j]  # Mueve los libros

        self.keys[i] = y.keys[self.t - 1]  # Inserta el libro en el nodo padre
        self.n += 1  # Aumenta el número de libros

    def traverse(self):
        i = 0
        while i < self.n:
            if not self.leaf:
                self.C[i].traverse()
            print(self.keys[i].ISBN, self.keys[i].titulo, end=" | ")
            i += 1

        if not self.leaf:
            self.C[i].traverse()

    # Método para buscar un libro por isbn
    def search(self, isbn):
        i = 0
        # Buscar el índice del libro
        while i < self.n and isbn > self.keys[i].ISBN:
            i += 1

        # Si el índice es menor que el número de libros y el isbn es igual al isbn del libro
        if i < self.n and self.keys[i].ISBN == isbn:
            return self.keys[i]  # Retorna el libro

        if self.leaf:
            return None

        # Si no es hoja, buscar en el nodo hijo
        return self.C[i].search(isbn)


class ArbolB:
    # Constructor de la clase ArbolB
    def __init__(self, t):
        self.root = None  # Puntero a la raíz
        self.t = t  # Grado mínimo
        self.name_to_isbn = {}  # Diccionario para buscar por nombre

    def traverse(self):
        if self.root:
            self.root.traverse()
            print()

    # Método para buscar un libro por isbn en el árbol
    def search(self, isbn):
        if self.root is not None:
            return self.root.search(isbn)
        return None

    # Método para insertar un libro en el árbol
    def insert(self, libro):
        # Si el árbol está vacío
        if not self.root:
            self.root = NodoArbolB(self.t, True)  # Crear un nuevo nodo
            self.root.keys[0] = libro  # Insertar el libro
            self.root.n = 1  # Aumentar el número de libros
        else:
            # Si la raíz está llena
            if self.root.n == (2 * self.t - 1):
                s = NodoArbolB(self.t, False)  # Crear un nuevo nodo
                s.C[0] = self.root  # Hacer que la raíz sea el hijo del nuevo nodo
                s.split_child(0, self.root)  # Dividir la raíz

                i = 0  # Inicializar el índice
                if s.keys[0].ISBN < libro.ISBN:  # Si el primer libro del nuevo nodo es menor que el libro a insertar
                    i += 1

                s.C[i].insert_non_full(libro)  # Insertar el libro en el hijo adecuado
                self.root = s
            else:
                self.root.insert_non_full(libro)
        self.name_to_isbn[libro.titulo] = libro.ISBN  # Insertar el libro en el diccionario

    # Método para eliminar un libro del árbol
    def remove(self, isbn):
        if not self.root:
            # print("El árbol está vacío")
            return

        # Eliminar del diccionario
        libro = self.search(isbn)
        if libro is not None:
            self.name_to_isbn.pop(libro.titulo)

        # Eliminar el libro
        self.root.remove(isbn)
        # Eliminar el libro del diccionario
        # Si la raíz está vacía
        if self.root.n == 0:
            tmp = self.root  # Guardar la raíz
            if self.root.leaf:
                self.root = None
            else:
                self.root = self.root.C[0]  # Hacer que el hijo sea la raíz

            del tmp  # Eliminar la raíz


    # Método para actualizar un libro
    def update(self, datos):
        ISBN = datos["isbn"]  # Obtener el isbn
        libro = self.search(ISBN)  # Buscar el libro
        if libro is None:  # Si el libro no existe
            return  # Retornar
        # Editar solamente lo que encuentre en el json de PATCH
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

    # Método para buscar un libro por nombre
    def searchByName(self, name):
        isbn = self.name_to_isbn.get(name)
        if isbn is not None:
            return self.search(isbn)
        return None


def main():
    arbol = ArbolB(5)
    while True:
        # Menú
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
    # Seleccionar el archivo CSV
    archivo_seleccionado = filedialog.askopenfilename(filetypes=[("Archivo CSV", "*.csv"), ("Todos los archivos", "*")])

    if archivo_seleccionado:
        try:
            # Abrir el archivo CSV y el archivo de salida
            with open(archivo_seleccionado, 'r') as f, open('libros_encontrados.txt', 'w') as writer:
                # procesados = 0
                # insertados = 0
                busquedas_hechas = 0
                operacion_actual = ""

                # Recorrer el archivo CSV
                for linea in f:
                    ultima_linea = linea

                    if linea.startswith("INSERT;"):
                        # operacion_actual = "INSERT"
                        datos = json.loads(linea[7:].strip())
                        libro = Libro(datos["isbn"], datos["name"], datos["author"], datos["category"], datos["price"],
                                      datos["quantity"])
                        arbol.insert(libro)

                    elif linea.startswith("DELETE;"):
                        # operacion_actual = "DELETE"
                        datos = json.loads(linea[7:].strip())
                        arbol.remove(datos["isbn"])

                    elif linea.startswith("PATCH;"):
                        # operacion_actual = "PATCH"
                        datos = json.loads(linea[6:].strip())
                        arbol.update(datos)

                    elif linea.startswith("SEARCH;"):
                        # operacion_actual = "SEARCH"
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
