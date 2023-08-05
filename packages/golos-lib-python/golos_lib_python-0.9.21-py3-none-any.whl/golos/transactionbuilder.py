import logging

from golos.account import Account
from golos.instance import shared_steemd_instance
from golos.wallet import Wallet
from golosbase import operations
from golosbase.account import PrivateKey
from golosbase.exceptions import InsufficientAuthorityError, InvalidKeyFormat, MissingKeyError
from golosbase.operations import Operation
from golosbase.transactions import SignedTransaction, fmt_time_from_now, get_block_params

log = logging.getLogger(__name__)


class TransactionBuilder(dict):
    """This class simplifies the creation of transactions by adding operations and signers."""

    def __init__(self, tx=None, steemd_instance=None, wallet_instance=None, no_broadcast=False, expiration=60):
        self.steemd = steemd_instance or shared_steemd_instance()
        self.no_broadcast = no_broadcast
        self.expiration = expiration
        self.wallet = wallet_instance or Wallet(self.steemd)

        self.op = []
        self.wifs = []
        self.tx = tx

    def appendOps(self, ops):
        if isinstance(ops, list):
            for op in ops:
                self.op.append(op)
        else:
            self.op.append(ops)
        self.constructTx()

    def appendSigner(self, account, permission):
        assert permission in ["active", "owner", "posting"], "Invalid permission"
        account = Account(account, steemd_instance=self.steemd)

        required_treshold = account[permission]["weight_threshold"]

        def fetchkeys(account, level=0):
            if level > 2:
                return []
            r = []
            for authority in account[permission]["key_auths"]:
                wif = self.wallet.getPrivateKeyForPublicKey(authority[0])
                if wif:
                    r.append([wif, authority[1]])

            if sum([x[1] for x in r]) < required_treshold:
                # go one level deeper
                for authority in account[permission]["account_auths"]:
                    auth_account = Account(authority[0], steemd_instance=self.steemd)
                    r.extend(fetchkeys(auth_account, level + 1))

            return r

        keys = fetchkeys(account)
        self.wifs.extend([x[0] for x in keys])

    def appendWif(self, wif):
        if wif:
            try:
                PrivateKey(wif)
                self.wifs.append(wif)
            except:
                raise InvalidKeyFormat

    def constructTx(self):
        if isinstance(self.op, list):
            ops = [Operation(o) for o in self.op]
        else:
            ops = [Operation(self.op)]
        expiration = fmt_time_from_now(self.expiration)
        ref_block_num, ref_block_prefix = get_block_params(self.steemd)
        tx = SignedTransaction(
            ref_block_num=ref_block_num, ref_block_prefix=ref_block_prefix, expiration=expiration, operations=ops
        )
        self.tx = tx

    def sign(self):
        """
        Sign a provided transaction with the provided key(s)

        :param dict tx: The transaction to be signed and returned
        :param string wifs: One or many wif keys to use for signing
            a transaction. If not present, the keys will be loaded
            from the wallet as defined in "missing_signatures" key
            of the transactions.
        """

        # We need to set the default prefix, otherwise pubkeys are
        # presented wrongly!
        if self.steemd:
            operations.default_prefix = self.steemd.chain_params["prefix"]
        elif "blockchain" in self:
            operations.default_prefix = self["blockchain"]["prefix"]

        if not any(self.wifs):
            raise MissingKeyError

        self.tx.sign(self.wifs, chain=self.steemd.chain_params)

    def verify_authority(self):
        """Verify the authority of the signed transaction."""
        try:
            if not self.steemd.verify_authority(self.json()):
                raise InsufficientAuthorityError
        except Exception as e:
            raise e

    def broadcast(self):
        """
        Broadcast a transaction to the Steem network.

        :param tx tx: Signed transaction to broadcast
        """
        if self.no_broadcast:
            log.warning("Not broadcasting anything!")
            log.debug(self.json())
            return self.tx

        try:
            if not self.steemd.verify_authority(self.json()):
                raise InsufficientAuthorityError
        except Exception as e:
            # There is an issue with some appbase builds which makes
            # `verify_authority` unusable. TODO: remove this case #212
            if "Bad Cast:Invalid cast from string_type to Array" in str(e):
                log.error("Ignoring verify_authority failure. See #212.")
            else:
                print("failing on {}".format(e))
                raise e

        try:
            self.steemd.broadcast_transaction(self.json())
        except Exception as e:
            raise e

        return self.tx

    def addSigningInformation(self, account, permission):
        """This is a private method that adds side information to a unsigned/partial transaction in order to simplify
        later signing (e.g. for multisig or coldstorage)"""
        account_obj = Account(account, steemd_instance=self.steemd)
        authority = account_obj[permission]
        # We add a required_authorities to be able to identify
        # how to sign later. This is an array, because we
        # may later want to allow multiple operations per tx
        self.update({"required_authorities": {account: authority}})
        for account_auth in authority["account_auths"]:
            account_auth_account = Account(account_auth[0], steemd_instance=self.steemd)
            self["required_authorities"].update({account_auth[0]: account_auth_account.get(permission)})

        # Try to resolve required signatures for offline signing
        self["missing_signatures"] = [x[0] for x in authority["key_auths"]]
        # Add one recursion of keys from account_auths:
        for account_auth in authority["account_auths"]:
            account_auth_account = Account(account_auth[0], steemd_instance=self.steemd)
            self["missing_signatures"].extend([x[0] for x in account_auth_account[permission]["key_auths"]])
        self["blockchain"] = self.steemd.chain_params

    def json(self):
        return self.tx.json()

    def appendMissingSignatures(self, wifs):
        missing_signatures = self.get("missing_signatures", [])
        for pub in missing_signatures:
            wif = self.wallet.getPrivateKeyForPublicKey(pub)
            if wif:
                self.appendWif(wif)
