import typing
from enum import Enum

import pandas as pd

from invest_tools import analysis


class Currency(Enum):
    USD = "usd"
    GBP = "gbp"


class InvalidCurrencyException(Exception):
    def __init__(self, message):
        super().__init__("Currency must be `gbp` or `usd`")


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
        currency: Currency,
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
        self.portfolio_definition = portfolio_definition
        self.backtest = pd.DataFrame()
        self.prices = pd.DataFrame()
        self.gbpusd = pd.DataFrame()
        self.usdgbp = pd.DataFrame()
        self.currency = currency
        self.clean_returns = pd.Series()
        self.percentage_returns = pd.Series()
        self.analysis = {}

    def ping(self):
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
                if opts["currency"] != Currency.GBP:
                    ret = self.calculate_returns(
                        self.prices, code, convert=True, cur=self.gbpusd
                    )
                elif opts["currency"] != Currency.USD:
                    ret = self.calculate_returns(
                        self.prices, code, convert=True, cur=self.usdgbp
                    )
                else:
                    # TODO add a test for this!
                    raise InvalidCurrencyException
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
        return port

    def _get_data(self) -> typing.List[pd.DataFrame]:
        """
        Automatically get the data necessary for the portfolio builder

        - FamaFrench Data
        - Currency Data
        - Benchmark

        This data can also just be stored in a `data` directory at the same
        level as the file that calls this package.
        """

        return []

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
        df = pd.read_csv(prices_csv)
        df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")
        self.prices = df
        return df

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

        cur = pd.read_csv(conversion_csv)
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
        ti = ti.sort_values(by="Date")
        ti = ti.set_index("Date")
        if convert:
            ti = ti.join(cur)
            ti.Close = ti.Close * ti.Convert
        ti["Close"] = ti.Close * ti.Adjustment
        ti["Returns"] = ti.Close.pct_change()
        ti["Returns"] = ti["Returns"].dropna()
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

        return analysis_results
