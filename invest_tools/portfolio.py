import typing

import pandas as pd

from invest_tools import analysis, currency, plot, validation
from invest_tools.log import logger

PRICES_DATATYPES = {
    "TIDM": "string",
    "Date": "string",
    "Open": float,
    "High": float,
    "Low": float,
    "Close": float,
    "Volume": float,
    "Adjustment": float,
}

BENCHMARK_DATATYPES = {
    "Date": "string",
    "Open": float,
    "High": float,
    "Low": float,
    "Close": float,
    "Volume": float,
    "Adjustment": float,
}

CURRENCY_DATATYPES = {
    "Date": "string",
    "Open": float,
    "High": float,
    "Low": float,
    "Close": float,
    "Adj Close": float,
    "Volume": float,
}


class Portfolio:
    """
    An investment portfolio is a collection of securities with weights and
    currencies. Using historical prices these portfolios can be analysed for
    historical performance and benchmarked by different values.

    Analysis can be done using a variety of techniques.

    The main function of building the portfolio is to standardise the portfolio
    to a single currency using a conversion rate (the Close price of the
    relevant currency on the day of the returns).
    """

    def __init__(
        self,
        portfolio_definition: typing.Dict[str, typing.Dict[str, str]],
        currency: currency.Currency,
    ):
        """
        The portfolio definition must be a python dictionary with the form of:

        ```
            {
                "code": {
                    "weight": Float,
                    "currency": "gbp" | "usd"
                },
                ...
            }
        ```

        The sum of the weights must be 1.

        The currency is defined in the `Currency` enum.

        Other values are simply empty initialised for future use.
        """
        validation.validate_portfolio_definition(portfolio_definition)
        logger.info("validated portfolio definition")
        self.portfolio_definition = portfolio_definition
        self.backtest = pd.DataFrame()
        self.prices = pd.DataFrame()
        self.gbpusd = pd.DataFrame()
        self.usdgbp = pd.DataFrame()
        self.benchmark = pd.DataFrame()
        self.currency = currency
        self.clean_returns = pd.Series(dtype=float)
        self.percentage_returns = pd.Series(dtype=float)
        self.analysis = {}

    def ping(self):
        logger.info("PING")
        return "pong"

    def build(self) -> pd.DataFrame:
        """
        Use the portfolio definition to build the portfolio

        :returns: Pandas dataframe of the portfolio returns
        :rtype: pd.DataFrame
        """
        dfs = []
        weights = []
        for code, opts in self.portfolio_definition.items():
            weights.append(opts["weight"])
            if opts["currency"] != self.currency:
                if opts["currency"] != currency.Currency.GBP:
                    ret = self.calculate_returns(
                        self.prices, code, convert=True, cur=self.gbpusd
                    )
                elif opts["currency"] != currency.Currency.USD:
                    ret = self.calculate_returns(
                        self.prices, code, convert=True, cur=self.usdgbp
                    )
            else:
                ret = self.calculate_returns(
                    self.prices, code, convert=False, cur=self.gbpusd
                )
            ret = ret.rename({"Returns": code}, axis=1)
            dfs.append(ret[code].to_frame())
        port = dfs[0].join(dfs[1:])
        port_ret = port.mul(weights, axis=1).sum(axis=1)
        port["portfolio_returns"] = port_ret
        self.backtest = port
        self.clean_returns = port_ret.dropna()
        logger.info("Portfolio built")
        return port

    def get_prices(self, prices_csv: str) -> pd.DataFrame:
        """
        Take in a string pointing to a csv file containing the prices

        The CSV should be in the following format:

        | TIDM | Date | Open | High | Low | Close | Volume | Adjustment |
        |------|------|------|------|-----|-------|--------|------------|

        The Date column should be in the format of "%d/%m/%Y".

        :returns: Pandas dataframe of the portfolio prices
        :rtype: pd.DataFrame
        """
        logger.info(f"Loading data from {prices_csv}")
        df = pd.read_csv(prices_csv)
        valid = validation.validate_columns(df, PRICES_DATATYPES.keys())
        valid = validation.validate_datatypes(df, PRICES_DATATYPES)
        logger.debug(f"passed validation: {valid}")
        df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")
        self.prices = df
        return df

    def get_benchmark(self, benchmark_csv: str) -> pd.Series:
        """
        Take in a string pointing to a csv file containing an appropriate benchmark

        The CSV should be in the following format:

        | Date | Open | High | Low | Close | Volume | Adjustment |
        |------|------|------|-----|-------|--------|------------|

        The Date column should be in the format of "%d/%m/%Y".

        :returns: Pandas dataframe of the portfolio benchmark
        :rtype: pd.DataFrame
        """
        logger.info(f"Loading data from {benchmark_csv}")
        df = pd.read_csv(benchmark_csv)
        valid = validation.validate_columns(df, BENCHMARK_DATATYPES.keys())
        valid = validation.validate_datatypes(df, BENCHMARK_DATATYPES)
        logger.debug(f"passed validation: {valid}")
        df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")
        df["returns"] = (df.Close / 100).pct_change()
        df["benchmark_returns"] = df.returns.dropna()
        df = df.set_index("Date")
        df = df[["benchmark_returns"]]
        self.backtest = self.backtest.join(df)
        return df

    # TODO make this generic for currency
    def get_usd_converter(self, conversion_csv: str) -> pd.DataFrame:
        """
        Get a dataframe of USD to GBP to convert the prices between currencies.
        All portfolio prices and returns should be in GBP.

        The CSV should be in the following format:

        | Date | Open | High | Low | Close | Adj Close | Volume |
        |------|------|------|-----|-------|-----------|--------|

        :returns: Pandas dataframe of currency prices.
        :rtype: pd.DataFrame
        """
        logger.info(f"Loading data from {conversion_csv}")
        cur = pd.read_csv(conversion_csv)
        valid = validation.validate_columns(cur, CURRENCY_DATATYPES.keys())
        valid = validation.validate_datatypes(cur, CURRENCY_DATATYPES)
        logger.debug(f"passed validation: {valid}")
        cur["Date"] = pd.to_datetime(cur["Date"])
        cur = cur.set_index("Date")
        cur = cur.rename({"Close": "Convert"}, axis=1)
        cur = cur[["Convert"]]
        self.gbpusd = cur
        return cur

    def calculate_returns(
        self, prices: pd.DataFrame, code: str, convert: bool, cur: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Take in a dataframe of prices of all codes and calculate the returns
        shown by each security and then record those returns into a single
        dataframe.

        The dataframe will be in the format as follows:

        | TIDM | Date | Open | High | Low | Close | Volume | Adjustment |
        |------|------|------|------|-----|-------|--------|------------|

        The function will work by filtering the input frame by each TIDM and
        calculating the adjusted and converted returns and appending them to
        a new dataframe.

        :returns: A dataframe of a single TIDM with returns adjusted by
        adjustment and converted to currency
        """
        ti = prices.loc[prices.TIDM == code]
        if len(ti) < 1:
            raise validation.InvalidDataFrame(f"{code} not in prices df")
        ti = ti.sort_values(by="Date")
        ti = ti.set_index("Date")
        if convert:
            ti = ti.join(cur)
            ti.Close = ti.Close * ti.Convert
        ti["Close"] = ti.Close * ti.Adjustment
        ti["Returns"] = ti.Close.pct_change()
        ti["Returns"] = ti["Returns"].dropna()
        logger.info(f"Calculation for {code} finished")
        return ti

    def analyse(self) -> typing.Dict[str, float]:
        analysis_results = {}

        daily_returns = analysis.calculate_mean_daily_returns(self.clean_returns)
        annual_returns = analysis.calculate_mean_annual_return(self.clean_returns)
        daily_std = analysis.calculate_std_daily(self.clean_returns)
        daily_var = analysis.calculate_variance_daily(self.clean_returns)
        skew = analysis.calculate_skewness(self.clean_returns)
        kurtosis = analysis.calculate_kurtosis(self.clean_returns)
        percentage_returns = analysis.calculate_percentage_returns(self.clean_returns)

        analysis_results["daily_returns"] = daily_returns
        analysis_results["annual_returns"] = annual_returns
        analysis_results["daily_std"] = daily_std
        analysis_results["daily_var"] = daily_var
        analysis_results["skew"] = skew
        analysis_results["kurtosis"] = kurtosis

        self.analysis = analysis_results
        self.percentage_returns = percentage_returns

        logger.info("Analysis loaded")
        return analysis_results

    def benchmark_analysis(self) -> pd.DataFrame:
        cumulative_returns = self.backtest[["portfolio_returns", "benchmark_returns"]]
        cumulative_returns = cumulative_returns.assign(
            excess_returns=cumulative_returns.portfolio_returns
            - cumulative_returns.benchmark_returns
        )
        cumulative_returns = (
            1 + cumulative_returns[["portfolio_returns", "excess_returns"]]
        ).cumprod() - 1
        self.benchmark = cumulative_returns
        return cumulative_returns

    def plot_correlation_heatmap(self, save=False) -> None:
        if len(self.backtest) < 1:
            logger.warn("please run `.build()` before plotting")
        stock_returns = self.backtest.drop(
            columns=["portfolio_returns", "benchmark_returns"]
        )
        correlation_matrix = stock_returns.corr()
        logger.info("calculating portfolio correlation")
        plot.plot_heatmap(correlation_matrix, "Portfolio Correlation", save)

    def plot_returns_data(self, save=False) -> None:
        if len(self.backtest) < 1:
            logger.warn("please run `.build()` before plotting")
        plot.plot_histogram(
            self.clean_returns, self.percentage_returns, "Returns data", save
        )

    def plot_benchmark(self, save=False) -> None:
        if len(self.benchmark) < 1:
            logger.warn("please run `.benchmark_analysis()` before plotting")
        plot.plot_excess_returns(self.benchmark, "Portfolio Returns", save)
