# # ⚠ Warning
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
# NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# [🥭 Mango Markets](https://mango.markets/) support is available at:
#   [Docs](https://docs.mango.markets/)
#   [Discord](https://discord.gg/67jySBhxrg)
#   [Twitter](https://twitter.com/mangomarkets)
#   [Github](https://github.com/blockworks-foundation)
#   [Email](mailto:hello@blockworks.foundation)


import typing

from decimal import Decimal
from solana.publickey import PublicKey

from .account import Account
from .combinableinstructions import CombinableInstructions
from .constants import SYSTEM_PROGRAM_ADDRESS
from .context import Context
from .group import Group
from .instructions import build_cancel_perp_order_instructions, build_mango_consume_events_instructions, build_cancel_all_perp_orders_instructions, build_place_perp_order_instructions, build_redeem_accrued_mango_instructions
from .marketoperations import MarketInstructionBuilder, MarketOperations
from .orders import Order, OrderBook
from .perpmarket import PerpMarket
from .publickey import encode_public_key_for_sorting
from .tokenbank import TokenBank
from .wallet import Wallet


# # 🥭 PerpMarketInstructionBuilder
#
# This file deals with building instructions for Perp markets.
#
# As a matter of policy for all InstructionBuidlers, construction and build_* methods should all work with
# existing data, requiring no fetches from Solana or other sources. All necessary data should all be loaded
# on initial setup in the `load()` method.
#
class PerpMarketInstructionBuilder(MarketInstructionBuilder):
    def __init__(self, context: Context, wallet: Wallet, group: Group, account: Account,
                 perp_market: PerpMarket) -> None:
        super().__init__()
        self.context: Context = context
        self.wallet: Wallet = wallet
        self.group: Group = group
        self.account: Account = account
        self.perp_market: PerpMarket = perp_market
        self.mngo_token_bank: TokenBank = self.group.liquidity_incentive_token_bank

    @staticmethod
    def load(context: Context, wallet: Wallet, group: Group, account: Account, perp_market: PerpMarket) -> "PerpMarketInstructionBuilder":
        return PerpMarketInstructionBuilder(context, wallet, group, account, perp_market)

    def build_cancel_order_instructions(self, order: Order, ok_if_missing: bool = False) -> CombinableInstructions:
        if self.perp_market.underlying_perp_market is None:
            raise Exception(f"PerpMarket {self.perp_market.symbol} has not been loaded.")
        return build_cancel_perp_order_instructions(
            self.context, self.wallet, self.account, self.perp_market.underlying_perp_market, order, ok_if_missing)

    def build_place_order_instructions(self, order: Order) -> CombinableInstructions:
        if self.perp_market.underlying_perp_market is None:
            raise Exception(f"PerpMarket {self.perp_market.symbol} has not been loaded.")
        return build_place_perp_order_instructions(
            self.context, self.wallet, self.perp_market.underlying_perp_market.group, self.account, self.perp_market.underlying_perp_market, order.price, order.quantity, order.client_id, order.side, order.order_type)

    def build_settle_instructions(self) -> CombinableInstructions:
        return CombinableInstructions.empty()

    def build_crank_instructions(self, addresses: typing.Sequence[PublicKey], limit: Decimal = Decimal(32)) -> CombinableInstructions:
        if self.perp_market.underlying_perp_market is None:
            raise Exception(f"PerpMarket {self.perp_market.symbol} has not been loaded.")

        distinct_addresses: typing.List[PublicKey] = [self.account.address]
        for address in addresses:
            if address not in distinct_addresses:
                distinct_addresses += [address]

        limited_addresses = distinct_addresses[0:min(int(limit), len(distinct_addresses))]
        limited_addresses.sort(key=encode_public_key_for_sorting)
        self._logger.debug(f"About to crank {len(limited_addresses)} addresses: {limited_addresses}")

        return build_mango_consume_events_instructions(self.context, self.group, self.perp_market.underlying_perp_market, limited_addresses, limit)

    def build_redeem_instructions(self) -> CombinableInstructions:
        return build_redeem_accrued_mango_instructions(self.context, self.wallet, self.perp_market, self.group, self.account, self.mngo_token_bank)

    def build_cancel_all_orders_instructions(self, limit: Decimal = Decimal(32)) -> CombinableInstructions:
        if self.perp_market.underlying_perp_market is None:
            raise Exception(f"PerpMarket {self.perp_market.symbol} has not been loaded.")
        return build_cancel_all_perp_orders_instructions(
            self.context, self.wallet, self.account, self.perp_market.underlying_perp_market, limit)

    def __str__(self) -> str:
        return """« PerpMarketInstructionBuilder »"""


# # 🥭 PerpMarketOperations
#
# This file deals with placing orders for Perps.
#
class PerpMarketOperations(MarketOperations):
    def __init__(self, market_name: str, context: Context, wallet: Wallet,
                 market_instruction_builder: PerpMarketInstructionBuilder,
                 account: Account, perp_market: PerpMarket) -> None:
        super().__init__(perp_market)
        self.market_name: str = market_name
        self.context: Context = context
        self.wallet: Wallet = wallet
        self.market_instruction_builder: PerpMarketInstructionBuilder = market_instruction_builder
        self.account: Account = account
        self.perp_market: PerpMarket = perp_market

    def cancel_order(self, order: Order, ok_if_missing: bool = False) -> typing.Sequence[str]:
        self._logger.info(f"Cancelling {self.market_name} order {order}.")
        signers: CombinableInstructions = CombinableInstructions.from_wallet(self.wallet)
        cancel: CombinableInstructions = self.market_instruction_builder.build_cancel_order_instructions(
            order, ok_if_missing=ok_if_missing)
        accounts_to_crank = self.perp_market.accounts_to_crank(self.context, self.account.address)
        crank = self.market_instruction_builder.build_crank_instructions(accounts_to_crank)
        settle = self.market_instruction_builder.build_settle_instructions()
        return (signers + cancel + crank + settle).execute(self.context)

    def place_order(self, order: Order) -> Order:
        client_id: int = self.context.generate_client_id()
        signers: CombinableInstructions = CombinableInstructions.from_wallet(self.wallet)
        order_with_client_id: Order = order.with_client_id(client_id)
        self._logger.info(f"Placing {self.market_name} order {order_with_client_id}.")
        place: CombinableInstructions = self.market_instruction_builder.build_place_order_instructions(
            order_with_client_id)
        accounts_to_crank = self.perp_market.accounts_to_crank(self.context, self.account.address)
        crank = self.market_instruction_builder.build_crank_instructions(accounts_to_crank)
        settle = self.market_instruction_builder.build_settle_instructions()
        (signers + place + crank + settle).execute(self.context)
        return order_with_client_id

    def settle(self) -> typing.Sequence[str]:
        signers: CombinableInstructions = CombinableInstructions.from_wallet(self.wallet)
        settle = self.market_instruction_builder.build_settle_instructions()
        return (signers + settle).execute(self.context)

    def crank(self, limit: Decimal = Decimal(32)) -> typing.Sequence[str]:
        signers: CombinableInstructions = CombinableInstructions.from_wallet(self.wallet)
        accounts_to_crank = self.perp_market.accounts_to_crank(self.context, self.account.address)
        crank = self.market_instruction_builder.build_crank_instructions(accounts_to_crank, limit)
        return (signers + crank).execute(self.context)

    def create_openorders(self) -> PublicKey:
        return SYSTEM_PROGRAM_ADDRESS

    def ensure_openorders(self) -> PublicKey:
        return SYSTEM_PROGRAM_ADDRESS

    def load_orderbook(self) -> OrderBook:
        return self.perp_market.fetch_orderbook(self.context)

    def load_my_orders(self) -> typing.Sequence[Order]:
        orderbook: OrderBook = self.load_orderbook()
        return list([o for o in [*orderbook.bids, *orderbook.asks] if o.owner == self.account.address])

    def __str__(self) -> str:
        return f"""« PerpMarketOperations [{self.market_name}] »"""
