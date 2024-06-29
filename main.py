import sys
from scripts.create_ontology import main as create_ontology
from scripts.process_ontology import main as process_ontology
from scripts.align_ontologies import main as align_ontologies
from scripts.match_ontologies import main as match_ontologies

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py [create|process|align|match]")
        sys.exit(1)
    
    command = sys.argv[1]
    if command == "create":
        create_ontology()
    elif command == "process":
        process_ontology()
    elif command == "align":
        align_ontologies()
    elif command == "match":
        match_ontologies()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
