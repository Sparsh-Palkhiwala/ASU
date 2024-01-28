class Node:
    def __init__(self,value):
        self.left = None
        self.data = value
        self.right = None
    
class Tree:
    def createNode(self,data):
        return Node(data)

    def insertNode(self,node,data):
        if node is None:
            return self.createNode(data)
        if data < node.data:
            node.left = self.insertNode(node.left,data)
        else:
            node.right = self.insertNode(node.right,data)
        return node

    def Traverse_Inorder(self,root):
        if root is not None:
            self.Traverse_Inorder(root.left)
            print(root.data)
            self.Traverse_Inorder(root.right)

    def Traverse_Preorder(self,root):
        if root is not None:
            print(root.data)
            self.Traverse_Preorder(root.left)
            self.Traverse_Preorder(root.right)

    def Traverse_Postorder(self,root):
        if root is not None:
            self.Traverse_Postorder(root.left)
            self.Traverse_Postorder(root.right)
            print(root.data)

    def insertIntoBST(self,root,data):
        if root is None:
            root = self.createNode(data)
        while 1:
            if data < root.data:
                if root.left is not None:
                    root = root.left
                else:
                    root.left = self.createNode(data)
                    break
            elif data >= root.data:
                if root.right is not None:
                    root = root.right
                else:
                    root.right = self.createNode(data)
                    break
        return root

tree = Tree()
root = tree.createNode(5)
print(root.data)
tree.insertNode(root,2)
tree.insertNode(root,9)
tree.insertNode(root,6)
tree.insertNode(root,10)
tree.insertIntoBST(root,8)
print("Print Inorder--> ")
tree.Traverse_Inorder(root)
print("Print PreOrder--> ")
tree.Traverse_Preorder(root)
print("Print PostOrder--> ")
tree.Traverse_Postorder(root)

