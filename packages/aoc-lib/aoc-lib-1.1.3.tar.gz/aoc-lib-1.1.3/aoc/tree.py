class TreeNode:
    PREORDER = 1
    INORDER = 2
    POSTORDER = 3

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    @classmethod
    def from_list(cls, arr):
        if arr is None or len(arr) == 0:
            return None
        tree = [[TreeNode(arr[0])]]
        i = 1
        while i < len(arr):
            new_level = []
            for node in tree[-1]:
                if i >= len(arr):
                    break
                v = arr[i]
                if v is not None:
                    node.left = TreeNode(v)
                    new_level.append(node.left)
                v = arr[i + 1]
                if v is not None:
                    node.right = TreeNode(v)
                    new_level.append(node.right)
                i += 2
            tree.append(new_level)
        return tree[0][0]

    def __iter__(self):
        yield from self.nodes()

    def nodes(self, style=INORDER):
        if style == TreeNode.PREORDER:
            yield self.val
        if self.left is not None:
            yield from self.left.nodes(style)
        if style == TreeNode.INORDER:
            yield self.val
        if self.right is not None:
            yield from self.right.nodes(style)
        if style == TreeNode.POSTORDER:
            yield self.val
