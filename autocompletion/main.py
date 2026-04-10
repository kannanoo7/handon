

from trie import Trie

def load_words(filename, trie):
    with open(filename, "r") as f:
        for line in f:
            trie.insert(line.strip())

from engine import AutoCompleteEngine

def main():

    print("Enter your Python code (type END to finish):")

    lines = []
    while True:
        line = input()
        if line == "END":
            break
        lines.append(line)

    source_code = "\n".join(lines)
    engine = AutoCompleteEngine(source_code)

    while True:
        query = input("\nAutocomplete > ")

        if query == "exit":
            break

        suggestions = engine.suggest(query)

        if suggestions:
            for s in suggestions[:10]:
                print("-", s)
        else:
            print("No suggestions")

if __name__ == "__main__":
    main()
