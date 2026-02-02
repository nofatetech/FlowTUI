import json
from services.code_scanner import CodeScannerService


def main():
    """
    Main entry point for the FlowTUI application.
    """
    scanner = CodeScannerService()
    app_graph = scanner.scan_apps()
    print(json.dumps(app_graph, indent=2))


if __name__ == "__main__":
    main()
