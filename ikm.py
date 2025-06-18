class TreeNode:
    def __init__(self, key=None, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right
        self.visited = False


class BinaryTree:
    def __init__(self):
        self.root = TreeNode(0)
        self.all_paths = set()
        self.errors = []
        self.missing_nodes = set()

    def bubbleSortByLength(self, items):
        """Сортировка пузырьком по длине строки"""
        n = len(items)
        for i in range(n):
            for j in range(0, n - i - 1):
                if len(items[j]) > len(items[j + 1]):
                    items[j], items[j + 1] = items[j + 1], items[j]
        return items

    def findNodes(self):
        """Поиск пропущенных узлов"""
        self.missing_nodes = set()
        paths_list = list(self.all_paths)
        sorted_paths = self.bubbleSortByLength(paths_list)

        for path in sorted_paths:
            for i in range(1, len(path)):
                prefix = path[:i]
                node = self.getNode(prefix)
                if node is None or node.key is None:
                    self.missing_nodes.add(prefix)

    def insertValue(self, key, path):
        """Вставка значения с обработкой ошибок"""
        try:
            current = self.root
            self.all_paths.add(path)

            # Добавляем все префиксы пути
            for i in range(1, len(path) + 1):
                self.all_paths.add(path[:i])

            index = 0
            while index < len(path):
                bit = path[index]
                if bit == '0':
                    if index == len(path) - 1:
                        if current.left is None:
                            current.left = TreeNode(key)
                        else:
                            if current.left.key is not None and current.left.key != key:
                                raise ValueError(f"Конфликт в узле {path}: {key} ≠ {current.left.key}")
                            current.left.key = key
                        current.left.visited = True
                    else:
                        if current.left is None:
                            current.left = TreeNode()
                        current = current.left
                elif bit == '1':
                    if index == len(path) - 1:
                        if current.right is None:
                            current.right = TreeNode(key)
                        else:
                            if current.right.key is not None and current.right.key != key:
                                raise ValueError(f"Конфликт в узле {path}: {key} ≠ {current.right.key}")
                            current.right.key = key
                        current.right.visited = True
                    else:
                        if current.right is None:
                            current.right = TreeNode()
                        current = current.right
                index += 1
            return True
        except ValueError as e:
            self.errors.append(str(e))
            return False

    def validateTree(self):
        """Проверка целостности дерева"""
        errors = []

        if self.root.key != 0:
            errors.append("Корень ≠ 0")

        paths_list = list(self.all_paths)
        sorted_paths = self.bubbleSortByLength(paths_list)

        for path in sorted_paths:
            node = self.getNode(path)
            if node is None or node.key is None:
                errors.append(f"Узел '{path}' без значения")

        self.findNodes()
        missing_list = list(self.missing_nodes)
        sorted_missing = self.bubbleSortByLength(missing_list)

        for path in sorted_missing:
            errors.append(f"Пропущен промежуточный узел '{path}'")

        return errors

    def getNode(self, path):
        """Получение узла по пути"""
        current = self.root
        for bit in path:
            if bit == '0':
                if current.left is None:
                    return None
                current = current.left
            elif bit == '1':
                if current.right is None:
                    return None
                current = current.right
        return current

    def printTree(self):
        """Печать структуры дерева"""

        def printHelper(node, prefix="", is_left=True):
            if node:
                if node.right:
                    printHelper(node.right, prefix + ("│   " if is_left else "    "), False)
                print(prefix + ("└── " if is_left else "┌── ") + str(node.key if node.key is not None else "None"))
                if node.left:
                    printHelper(node.left, prefix + ("    " if is_left else "│   "), True)

        print("\nГоризонтальное представление дерева:")
        printHelper(self.root)


class TreeManager:
    def __init__(self):
        self.tree = BinaryTree()
        self.line_num = 1

    def validatePath(self, path):
        """Проверка корректности пути"""
        if not path:
            return False
        for char in path:
            if char not in ('0', '1'):
                return False
        return True

    def processInputLine(self, line):
        """Обработка строки ввода"""
        line = line.strip()
        if not line:
            return False

        parts = line.split()
        if len(parts) != 2:
            print(f"Ошибка формата в строке {self.line_num}")
            self.line_num += 1
            return False

        value, path = parts
        if not self.validatePath(path):
            print(f"Неверный путь в строке {self.line_num}")
            self.line_num += 1
            return False

        try:
            value = int(value)
        except ValueError:
            print(f"Нечисловое значение в строке {self.line_num}")
            self.line_num += 1
            return False

        if not self.tree.insertValue(value, path):
            print(f"Ошибка в строке {self.line_num}: {self.tree.errors[-1]}")

        self.line_num += 1
        return True

    def fillNodes(self):
        """Заполнение пропущенных узлов"""
        self.tree.findNodes()
        if self.tree.missing_nodes:
            print("\nНеобходимо заполнить промежуточные узлы:")
            missing_list = list(self.tree.missing_nodes)
            sorted_missing = self.tree.bubbleSortByLength(missing_list)

            for path in sorted_missing:
                while True:
                    try:
                        value = input(f"Введите значение для узла '{path}': ").strip()
                        if not value:
                            print("Значение не может быть пустым!")
                            continue
                        value = int(value)
                        self.tree.insertValue(value, path)
                        break
                    except ValueError:
                        print("Ошибка: введите целое число!")

    def interactiveInput(self):
        """Интерактивный ввод данных"""
        print("\nВвод данных (формат: <значение> <путь>):")
        print("Пример: 15 101")
        print("Для завершения введите 'end'")

        while True:
            line = input(f"[{self.line_num}]> ").strip()

            if line.lower() == 'end':
                if not self.tree.all_paths:
                    print("Нет данных. Введите хотя бы одно значение.")
                    continue
                self.fillNodes()
                break

            self.processInputLine(line)

    def processFileLine(self, line):
        """Обработка строки файла"""
        line = line.strip()
        if not line:
            return False

        parts = line.split()
        if len(parts) != 2:
            print(f"Пропуск строки {self.line_num}: неверный формат")
            self.line_num += 1
            return False

        value, path = parts
        if not self.validatePath(path):
            print(f"Пропуск строки {self.line_num}: неверный путь")
            self.line_num += 1
            return False

        try:
            value = int(value)
        except ValueError:
            print(f"Пропуск строки {self.line_num}: нечисловое значение")
            self.line_num += 1
            return False

        if not self.tree.insertValue(value, path):
            print(f"Ошибка в строке {self.line_num}: {self.tree.errors[-1]}")

        self.line_num += 1
        return True

    def fileInput(self, filename):
        """Чтение данных из файла"""
        try:
            with open(filename, 'r') as f:
                for line in f:
                    self.processFileLine(line)

            if not self.tree.all_paths:
                print("Файл не содержит корректных данных!")
                return False

            # Проверяем и заполняем пропущенные узлы сразу после чтения файла
            self.tree.findNodes()
            if self.tree.missing_nodes:
                print("\nОбнаружены пропущенные узлы при чтении файла:")
                missing_list = list(self.tree.missing_nodes)
                sorted_missing = self.tree.bubbleSortByLength(missing_list)

                for path in sorted_missing:
                    while True:
                        try:
                            value = input(f"Введите значение для узла '{path}': ").strip()
                            if not value:
                                print("Значение не может быть пустым!")
                                continue
                            value = int(value)
                            self.tree.insertValue(value, path)
                            break
                        except ValueError:
                            print("Ошибка: введите целое число!")

            return True

        except FileNotFoundError:
            print("Файл не найден")
            return False
        except Exception as e:
            print(f"Ошибка чтения: {e}")
            return False

    def showResults(self):
        """Вывод результатов"""
        errors = self.tree.validateTree()
        print("\n" + "=" * 40)
        if errors:
            print("Обнаружены проблемы:")
            for error in errors:
                print(f"• {error}")
        else:
            print("Дерево построено успешно!")
        self.tree.printTree()

    def run(self):
        """Основной цикл программы"""
        print("Построение бинарного дерева")
        print("--------------------------")
        print("1. Ручной ввод")
        print("2. Загрузка из файла")
        print("3. Выход")

        while True:
            choice = input("\nВыберите действие (1-3): ").strip()
            if choice == '1':
                self.interactiveInput()
                break
            elif choice == '2':
                filename = input("Введите имя файла: ").strip()
                if self.fileInput(filename):
                    break
                self.line_num = 1
            elif choice == '3':
                print("Завершение работы")
                return
            else:
                print("Некорректный выбор")

        self.showResults()


if __name__ == "__main__":
    manager = TreeManager()
    manager.run()