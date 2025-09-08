import argparse
from agents.orchestrator import StockOrchestrator

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--query", default=None)
    args = parser.parse_args()

    orchestrator = StockOrchestrator()
    recommendation = orchestrator.run(args.ticker, args.query)
    print("Recommendation:\n", recommendation)

if __name__ == "__main__":
    main()
