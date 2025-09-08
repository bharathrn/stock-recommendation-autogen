import argparse
import json
from agents.orchestrator import run_pipeline

def main():
    parser = argparse.ArgumentParser(description='Stock Market Assistant')
    parser.add_argument('--ticker', required=True, help='Ticker symbol e.g. AAPL or TCS.NS')
    parser.add_argument('--query', required=False, help='News query (defaults to ticker/company)')
    args = parser.parse_args()

    out = run_pipeline(ticker=args.ticker, company_query=args.query or args.ticker)

    print('\n=== STRATEGY NOTE ===')
    print(out.get('strategy'))
    print('\n=== FEATURES ===')
    print(json.dumps(out.get('features', {}), indent=2))
    print('\n=== SENTIMENT ===')
    print(json.dumps(out.get('sentiment', {}), indent=2))
    print('\n=== TOP HEADLINES ===')
    for h in out.get('headlines', []):
        print(f"- {h.get('title')} — {h.get('source')} ({h.get('date')})")
        if h.get('url'):
            print(f"  {h.get('url')}")
    print()

if __name__ == '__main__':
    main()
