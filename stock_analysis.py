import sys

try:
    import yfinance as yf
except ImportError:
    sys.stderr.write('yfinance is required. Install with "pip install yfinance"\n')
    sys.exit(1)


def analyze_stock(symbol: str) -> None:
    symbol = symbol.strip().upper()
    if not symbol:
        print('Ticker symbol cannot be empty')
        return
    ticker = yf.Ticker(symbol)

    try:
        info = ticker.info
    except Exception as e:
        print(f'Error retrieving info for {symbol}: {e}')
        return

    long_name = info.get('longName') or info.get('shortName') or symbol
    sector = info.get('sector', 'N/A')
    industry = info.get('industry', 'N/A')
    market_cap = info.get('marketCap', 'N/A')
    trailing_pe = info.get('trailingPE', 'N/A')
    forward_pe = info.get('forwardPE', 'N/A')
    price_to_book = info.get('priceToBook', 'N/A')
    dividend_yield = info.get('dividendYield', 'N/A')
    beta = info.get('beta', 'N/A')

    print(f'\n=== {long_name} ({symbol}) ===')
    print(f'Sector: {sector}')
    print(f'Industry: {industry}')
    print(f'Market Cap: {market_cap}')
    print(f'Trailing P/E: {trailing_pe}')
    print(f'Forward P/E: {forward_pe}')
    print(f'Price-to-Book: {price_to_book}')
    print(f'Dividend Yield: {dividend_yield}')
    print(f'Beta: {beta}')

    try:
        hist = ticker.history(period='1y')
    except Exception as e:
        print(f'Error retrieving historical data: {e}')
        return

    if not hist.empty:
        latest_close = hist['Close'].iloc[-1]
        hist['50d_ma'] = hist['Close'].rolling(window=50).mean()
        hist['200d_ma'] = hist['Close'].rolling(window=200).mean()
        ma50 = hist['50d_ma'].iloc[-1]
        ma200 = hist['200d_ma'].iloc[-1]
        print(f'Latest Close Price: {latest_close:.2f}')
        print(f'50-Day Moving Average: {ma50:.2f}')
        print(f'200-Day Moving Average: {ma200:.2f}')
    else:
        print('No historical data available')


def main() -> None:
    if len(sys.argv) > 1:
        symbol = sys.argv[1]
    else:
        symbol = input('Enter stock ticker symbol (e.g. AAPL): ')
    analyze_stock(symbol)


if __name__ == '__main__':
    main()
