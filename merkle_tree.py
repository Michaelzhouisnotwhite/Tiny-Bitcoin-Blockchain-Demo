from typing import Any, List
from colorprt import colorstr, Fore
import hashlib
import pickle


class Transaction:
    def __init__(self, from_pk, to_pk, amount) -> None:
        self.from_pk = from_pk
        self.to_pk = to_pk
        self.amount = amount

    def __str__(self) -> str:
        return f"{self.from_pk} -> {self.to_pk}: {self.amount}"


class Node:
    def __init__(self, left, right, value: str, content: Any, is_copied=False) -> None:
        self.left: Node = left
        self.right: Node = right
        self.value = value
        self.content = content
        self.is_copied = is_copied

    @staticmethod
    def hashstr(val: str) -> str:
        return hashlib.sha256(val.encode('utf-8')).hexdigest()

    @staticmethod
    def hashbyte(val: bytes) -> str:
        return hashlib.sha256(val).hexdigest()

    def __str__(self):
        return str(self.value)

    def copy(self):
        """
        copy function

        Returns:
            Node: 自己的节点
        """
        return Node(self.left, self.right, self.value, self.content, True)


class MerkleTree:
    def __init__(self, values: list) -> None:
        self.root: Node
        self.__buildTree(values)

    def __buildTree(self, values: list) -> None:

        leaves = [
            Node(
                None,
                None,
                Node.hashstr(e) if isinstance(e, str) else Node.hashbyte(pickle.dumps(e)), e
            ) for e in values
        ]
        if len(leaves) % 2 == 1:
            leaves.append(leaves[-1].copy())  # duplicate last elem if odd number of elements
        self.root: Node = self.__buildTreeRec(leaves)

    def __buildTreeRec(self, nodes: List[Node]) -> Node:
        if len(nodes) % 2 == 1:
            nodes.append(nodes[-1].copy())  # duplicate last elem if odd number of elements

        half: int = len(nodes) // 2

        if len(nodes) == 2:
            return Node(nodes[0], nodes[1], Node.hashstr(
                nodes[0].value + nodes[1].value),
                [nodes[0].content, nodes[1].content]
            )

        left: Node = self.__buildTreeRec(nodes[:half])
        right: Node = self.__buildTreeRec(nodes[half:])
        value: str = Node.hashstr(left.value + right.value)

        content = left.content + right.content
        return Node(left, right, value, content)

    def printTree(self) -> None:
        self.__printTreeRec(self.root)

    # def __printTreeRec(self, node) -> None:
    #     if node is not None:
    #         if node.left is not None and node.right is not None:
    #             # print("Left: " + str(node.left))
    #             # print("Right: " + str(node.right))
    #             pass
    #         else:
    #             print("Leaf Node")
    #             print("Value: " + str(node.value))
    #             if node.is_copied:
    #                 print(f"Content: {str(node.content)}{colorstr('(Copy)', Fore.YELLOW)}")
    #             else:
    #                 print("Content: " + str(node.content))
    #             print("")

    #         self.__printTreeRec(node.left)
    #         self.__printTreeRec(node.right)

    def __printTreeRec(self, node, level=0):
        if node is not None:
            self.__printTreeRec(node.left, level + 1)
            font_str = f"{' ' * 6 * level}-> "
            print(f"{font_str}{node.value[:8]}{'(Copy)' if node.is_copied else ''}")
            if not isinstance(node.content, list):
                print(f"{' ' * len(font_str)}{node.content}")
            self.__printTreeRec(node.right, level + 1)

    def getRootHash(self) -> str:
        return self.root.value

    def get_format_tree(self):
        res = []
        self.__format_tree(self.root, res)
        return res

    def __format_tree(self, node, buf: list):
        if node is not None:
            if node.left is not None and node.right is not None:
                sub_buf = [node.left, node.right]
                buf.append(sub_buf)

            self.__format_tree(node.left, buf)
            self.__format_tree(node.right, buf)

    def __str__(self) -> str:
        return self.getRootHash()


def main() -> None:
    # elems = ["Mix", "Merkle", "Tree", "From", "Onur Atakan ULUSOY", "https://github.com/onuratakan/mixmerkletree",
    # "GO"]
    transactions = [Transaction('A', 'B', 10.0), Transaction('A', 'A', 5.0), Transaction('B', 'C', 7.1)]
    print("Inputs: ")
    print("transaction: ", end="")
    print(*transactions, sep="\ntransaction: ")
    print("")
    mtree = MerkleTree(transactions)
    print(f"Root Hash: {mtree.getRootHash()} \n")
    mtree.printTree()


if __name__ == "__main__":
    main()
