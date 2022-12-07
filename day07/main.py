from collections import defaultdict
from typing import List

RAW_INPUT = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""


class TreeNode:
    def __init__(self,
        size: int = 0,
        parent: 'TreeNode' = None):
        """
        input:
            size: size of the current node, for directories we assume it is 0
            parent: pointer to parent node  
        it creates two more attributes
            children: pointers to the node's children.
            _total_size: stores the total size of the subtree rooted at the this node,
            initially -1
        """
        self.size = size
        self.parent = parent
        self.children = list()
        self._total_size = -1

    def total_size(self) -> int:
        if self._total_size < 0:
            self._total_size = self.size
            for child in self.children: 
                self._total_size += child.total_size()
        return self._total_size
    
    def list_directories_sizes(self) -> List[int]:
        self.total_size()
        directories_sizes = []
        def dfs(root: TreeNode):
            if root.size == 0:
                directories_sizes.append(root.total_size())
            for child in root.children:
                dfs(child)
        dfs(self)
        return directories_sizes


    @staticmethod
    def parse(terminal_output: str) -> 'TreeNode':
        lines = terminal_output.strip().splitlines()
        dir_to_node_mapper = defaultdict(TreeNode)
        i = 0
        while i < len(lines):
            command_pieces = lines[i].split(' ')
            command = command_pieces[1]
            if command == 'cd':
                subdir = command_pieces[2]
                if subdir == '..':
                    # set the current parent = grandparent
                    curr_parent = curr_parent.parent
                else:
                    # set the current parent to the current folder {subdir}
                    curr_parent = dir_to_node_mapper[subdir]
                i += 1
            else:
                # the commmand is ls, we need to read the lines below
                i += 1
                while i < len(lines) and not lines[i].startswith('$'):
                    str_size, name = lines[i].split(' ')
                    size = int(str_size) if str_size.isnumeric() else 0
                    # create a new node
                    node = TreeNode(size, parent=curr_parent)
                    # add the current node to the parent.children array
                    curr_parent.children.append(node)
                    # if it is a directory, then save to use later as parent
                    if str_size == 'dir':
                        dir_to_node_mapper[name] = node
                    i += 1
        return dir_to_node_mapper['/']


def compute_total_space_under(terminal_output: str, under: int = 100_000) -> int: 
    root = TreeNode.parse(terminal_output)
    sizes = root.list_directories_sizes()
    answer = sum([dsize for dsize in sizes if dsize <= under])
    return answer


def choose_directory_to_delete(
    terminal_output: str,
    total_space: int = 70000000,
    space_needit: int = 30000000) -> int:
    # parse the input
    root = TreeNode.parse(terminal_output)
    # get directories sizes
    sizes = root.list_directories_sizes()


    answer = float('inf')
    free_space = total_space - root.total_size()
    # no need to delete anything
    if free_space >= space_needit:
        return 0

    for dsize in sizes:
        # if deleting this dir creates enough space
        if free_space + dsize >= space_needit:
            # take the minimum between the current size
            # and the best answer so far
            answer = min(dsize, answer)
    return answer


if __name__ == '__main__':
    test_total_space_under_100k = compute_total_space_under(RAW_INPUT, 100_000)
    assert test_total_space_under_100k == 95437

    test_space_dir_to_delete = choose_directory_to_delete(RAW_INPUT)
    assert test_space_dir_to_delete == 24933642

    with open('data/input.txt') as f:
        terminal_output = f.read()
    
    total_space_under_100k = compute_total_space_under(terminal_output, 100_000)
    print(f'total_space_under_100k: {total_space_under_100k}')

    space_dir_to_delete = choose_directory_to_delete(terminal_output)
    print(f'space_dir_to_delete: {space_dir_to_delete}')

    