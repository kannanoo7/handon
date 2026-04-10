

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.frequency = 0   # for future ranking


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.frequency += 1

    def _dfs(self, node, prefix, results):
        if node.is_end:
            results.append((prefix, node.frequency))

        for char, child in node.children.items():
            self._dfs(child, prefix + char, results)

    def autocomplete(self, prefix):
        node = self.root

        # Step 1: Traverse to prefix node
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        # Step 2: DFS from that node
        results = []
        self._dfs(node, prefix, results)

        # Step 3: Sort by frequency (future-ready)
        results.sort(key=lambda x: -x[1])

        return [word for word, _ in results]