import importlib
import json
import re
import struct
from collections import OrderedDict

from golosbase.account import PublicKey
from golosbase.operationids import operations
from golosbase.types import (
    Array,
    Bool,
    Bytes,
    Id,
    Int16,
    Int64,
    JsonObj,
    Map,
    OperationWrapper,
    Optional,
    PointInTime,
    StaticVariant,
    String,
    Uint16,
    Uint32,
    Uint64,
    variable_buffer,
    varint,
)

default_prefix = "GLS"

asset_precision = {
    "GOLOS": 3,
    "GESTS": 6,
    "GBG": 3,
}


class Operation:
    def __init__(self, op):
        if isinstance(op, list) and len(op) == 2:
            if isinstance(op[0], int):
                self.opId = op[0]
                name = self.get_operation_name_for_id(self.opId)
            else:
                self.opId = operations.get(op[0], None)
                name = op[0]
                if self.opId is None:
                    raise ValueError("Unknown operation")

            # convert method name like feed_publish to class name like FeedPublish
            self.name = self.to_class_name(name)
            try:
                klass = self.get_class(self.name)
            except:
                raise NotImplementedError("Unimplemented Operation %s" % self.name)
            else:
                self.op = klass(op[1])
        else:
            self.op = op
            # class name like FeedPublish
            self.name = type(self.op).__name__
            self.opId = operations[self.to_method_name(self.name)]

    @staticmethod
    def get_operation_name_for_id(_id: int):
        """Convert an operation id into the corresponding string."""
        for key, value in operations.items():
            if value == int(_id):
                return key

    @staticmethod
    def to_class_name(method_name: str):
        """Take a name of a method, like feed_publish and turn it into class name like FeedPublish."""
        return "".join(map(str.title, method_name.split("_")))

    @staticmethod
    def to_method_name(class_name: str):
        """Take a name of a class, like FeedPublish and turn it into method name like feed_publish."""
        words = re.findall("[A-Z][^A-Z]*", class_name)
        return "_".join(map(str.lower, words))

    @staticmethod
    def get_class(class_name: str):
        """Given name of a class from `operations`, return real class."""
        module = importlib.import_module("golosbase.operations")
        return getattr(module, class_name)

    def __bytes__(self):
        return bytes(Id(self.opId)) + bytes(self.op)

    def __str__(self):
        return json.dumps([self.get_operation_name_for_id(self.opId), self.op.json()])


class GrapheneObject(object):
    """
    Core abstraction class.

    This class is used for any JSON reflected object in Graphene.

    * ``instance.__json__()``: encodes data into json format
    * ``bytes(instance)``: encodes data into wire format
    * ``str(instances)``: dumps json object as string
    """

    def __init__(self, data=None):
        self.data = data

    def __bytes__(self):
        if self.data is None:
            return bytes()
        b = b""
        for name, value in self.data.items():
            if isinstance(value, str):
                b += bytes(value, "utf-8")
            else:
                b += bytes(value)
        return b

    def __json__(self):
        if self.data is None:
            return {}
        d = {}  # JSON output is *not* ordered
        for name, value in self.data.items():
            if isinstance(value, Optional) and value.isempty():
                continue

            if isinstance(value, String):
                d.update({name: str(value)})
            else:
                d.update({name: JsonObj(value)})
        return d

    def __str__(self):
        return json.dumps(self.__json__())

    def json(self):
        return self.__json__()


class Permission(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            prefix = kwargs.pop("prefix", default_prefix)

            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            # Sort keys (FIXME: ideally, the sorting is part of Public
            # Key and not located here)
            kwargs["key_auths"] = sorted(
                kwargs["key_auths"], key=lambda x: repr(PublicKey(x[0], prefix=prefix)), reverse=False,
            )
            kwargs["account_auths"] = sorted(kwargs["account_auths"], key=lambda x: x[0], reverse=False,)

            accountAuths = Map([[String(e[0]), Uint16(e[1])] for e in kwargs["account_auths"]])
            keyAuths = Map([[PublicKey(e[0], prefix=prefix), Uint16(e[1])] for e in kwargs["key_auths"]])
            super().__init__(
                OrderedDict(
                    [
                        ("weight_threshold", Uint32(int(kwargs["weight_threshold"]))),
                        ("account_auths", accountAuths),
                        ("key_auths", keyAuths),
                    ]
                )
            )


class Memo(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            prefix = kwargs.pop("prefix", default_prefix)

            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            super().__init__(
                OrderedDict(
                    [
                        ("from", PublicKey(kwargs["from"], prefix=prefix)),
                        ("to", PublicKey(kwargs["to"], prefix=prefix)),
                        ("nonce", Uint64(int(kwargs["nonce"]))),
                        ("check", Uint32(int(kwargs["check"]))),
                        ("encrypted", Bytes(kwargs["encrypted"])),
                    ]
                )
            )


class Vote(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("voter", String(kwargs["voter"])),
                        ("author", String(kwargs["author"])),
                        ("permlink", String(kwargs["permlink"])),
                        ("weight", Int16(kwargs["weight"])),
                    ]
                )
            )


class Comment(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            meta = ""
            if "json_metadata" in kwargs and kwargs["json_metadata"]:
                if isinstance(kwargs["json_metadata"], dict) or isinstance(kwargs["json_metadata"], list):
                    meta = json.dumps(kwargs["json_metadata"])
                else:
                    meta = kwargs["json_metadata"]

            super().__init__(
                OrderedDict(
                    [
                        ("parent_author", String(kwargs["parent_author"])),
                        ("parent_permlink", String(kwargs["parent_permlink"])),
                        ("author", String(kwargs["author"])),
                        ("permlink", String(kwargs["permlink"])),
                        ("title", String(kwargs["title"])),
                        ("body", String(kwargs["body"])),
                        ("json_metadata", String(meta)),
                    ]
                )
            )


class DeleteComment(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            super().__init__(
                OrderedDict([("author", String(kwargs["author"])), ("permlink", String(kwargs["permlink"])),])
            )


class Amount:
    def __init__(self, d):
        self.amount, self.asset = d.strip().split(" ")
        self.precision = len(self.amount.split('.')[-1])
        self.amount = float(self.amount)

        if self.asset in asset_precision:
            self.precision = asset_precision[self.asset]
            self.isUIA = False
        else:
            self.isUIA = True

    def __bytes__(self):
        # padding
        asset = self.asset + "\x00" * (7 - len(self.asset))
        amount = round(float(self.amount) * 10 ** self.precision)
        return struct.pack("<q", amount) + struct.pack("<b", self.precision) + bytes(asset, "ascii")

    def __str__(self):
        return "{:.{}f} {}".format(self.amount, self.precision, self.asset)


class ExchangeRate(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            super().__init__(OrderedDict([("base", Amount(kwargs["base"])), ("quote", Amount(kwargs["quote"])),]))


class ChainProperties(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            super().__init__(
                OrderedDict(
                    [
                        ("account_creation_fee", Amount(kwargs["account_creation_fee"])),
                        ("maximum_block_size", Uint32(kwargs["maximum_block_size"])),
                        ("sbd_interest_rate", Uint16(kwargs["sbd_interest_rate"])),
                    ]
                )
            )


class ChainProperties18(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            p = ChainProperties(kwargs).data
            p.update(
                OrderedDict(
                    [
                        ("create_account_min_golos_fee", Amount(kwargs["create_account_min_golos_fee"])),
                        ("create_account_min_delegation", Amount(kwargs["create_account_min_delegation"])),
                        ("create_account_delegation_time", Uint32(kwargs["create_account_delegation_time"])),
                        ("min_delegation", Amount(kwargs["min_delegation"])),
                    ]
                )
            )
            super().__init__(p)


class ChainProperties19(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            p = ChainProperties18(kwargs).data
            p.update(
                OrderedDict(
                    [
                        # Note that param order is critical to serialization
                        ("max_referral_interest_rate", Uint16(kwargs["max_referral_interest_rate"])),
                        ("max_referral_term_sec", Uint32(kwargs["max_referral_term_sec"])),
                        ("min_referral_break_fee", Amount(kwargs["min_referral_break_fee"])),
                        ("max_referral_break_fee", Amount(kwargs["max_referral_break_fee"])),
                        ("posts_window", Uint16(kwargs["posts_window"])),
                        ("posts_per_window", Uint16(kwargs["posts_per_window"])),
                        ("comments_window", Uint16(kwargs["comments_window"])),
                        ("comments_per_window", Uint16(kwargs["comments_per_window"])),
                        ("votes_window", Uint16(kwargs["votes_window"])),
                        ("votes_per_window", Uint16(kwargs["votes_per_window"])),
                        ("auction_window_size", Uint16(kwargs["auction_window_size"])),
                        ("max_delegated_vesting_interest_rate", Uint16(kwargs["max_delegated_vesting_interest_rate"])),
                        ("custom_ops_bandwidth_multiplier", Uint16(kwargs["custom_ops_bandwidth_multiplier"])),
                        ("min_curation_percent", Uint16(kwargs["min_curation_percent"])),
                        ("max_curation_percent", Uint16(kwargs["max_curation_percent"])),
                        ("curation_reward_curve", Uint64(kwargs["curation_reward_curve"])),
                        ("allow_distribute_auction_reward", Bool(bool(kwargs["allow_distribute_auction_reward"]))),
                        (
                            "allow_return_auction_reward_to_fund",
                            Bool(bool(kwargs["allow_return_auction_reward_to_fund"])),
                        ),
                    ]
                )
            )
            super().__init__(p)


class ChainProperties22(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            p = ChainProperties19(kwargs).data
            p.update(
                OrderedDict(
                    [
                        ("worker_reward_percent", Uint16(kwargs["worker_reward_percent"])),
                        ("witness_reward_percent", Uint16(kwargs["witness_reward_percent"])),
                        ("vesting_reward_percent", Uint16(kwargs["vesting_reward_percent"])),
                        ("worker_request_creation_fee", Amount(kwargs["worker_request_creation_fee"])),
                        ("worker_request_approve_min_percent", Uint16(kwargs["worker_request_approve_min_percent"])),
                        ("sbd_debt_convert_rate", Uint16(kwargs["sbd_debt_convert_rate"])),
                        ("vote_regeneration_per_day", Uint32(kwargs["vote_regeneration_per_day"])),
                        ("witness_skipping_reset_time", Uint32(kwargs["witness_skipping_reset_time"])),
                        ("witness_idleness_time", Uint32(kwargs["witness_idleness_time"])),
                        ("account_idleness_time", Uint32(kwargs["account_idleness_time"])),
                    ]
                )
            )
            super().__init__(p)


class ChainProperties23(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            p = ChainProperties22(kwargs).data
            p.update(
                OrderedDict(
                    [
                        ("claim_idleness_time", Uint32(kwargs["claim_idleness_time"])),
                        ("min_invite_balance", Amount(kwargs["min_invite_balance"])),
                    ]
                )
            )
            super().__init__(p)


class ChainProperties24(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            p = ChainProperties23(kwargs).data
            p.update(
                OrderedDict(
                    [
                        ("asset_creation_fee", Amount(kwargs["asset_creation_fee"])),
                        ("invite_transfer_interval_sec", Uint32(kwargs["invite_transfer_interval_sec"])),
                    ]
                )
            )
            super().__init__(p)


class ChainProperties26(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            p = ChainProperties24(kwargs).data
            p.update(
                OrderedDict(
                    [
                        ("convert_fee_percent", Uint16(kwargs["convert_fee_percent"])),
                        ("min_golos_power_to_curate", Amount(kwargs["min_golos_power_to_curate"])),
                        ("worker_emission_percent", Uint16(kwargs["worker_emission_percent"])),
                        ("vesting_of_remain_percent", Uint16(kwargs["vesting_of_remain_percent"])),
                        ("negrep_posting_window", Uint16(kwargs["negrep_posting_window"])),
                        ("negrep_posting_per_window", Uint16(kwargs["negrep_posting_per_window"])),
                    ]
                )
            )
            super().__init__(p)


class Props(StaticVariant):
    def __init__(self, o):
        type_id, data = o

        if type_id == 0:
            data = ChainProperties(data["props"])
        elif type_id == 1:
            data = ChainProperties18(data["props"])
        elif type_id == 2:
            data = ChainProperties19(data["props"])
        elif type_id == 3:
            data = ChainProperties22(data["props"])
        elif type_id == 4:
            data = ChainProperties23(data["props"])
        elif type_id == 5:
            data = ChainProperties24(data["props"])
        elif type_id == 6:
            data = ChainProperties26(data["props"])
        super().__init__(data, type_id)


class Beneficiary(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict([("account", String(kwargs["account"])), ("weight", Int16(kwargs["weight"])),])
            )


class Beneficiaries(GrapheneObject):
    def __init__(self, kwargs):
        super().__init__(OrderedDict([("beneficiaries", Array([Beneficiary(o) for o in kwargs["beneficiaries"]])),]))


class Destination(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([("destination", Uint64(kwargs["destination"])),]))


class Percent(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([("percent", Uint16(kwargs["percent"])),]))


class CommentOptionExtensions(StaticVariant):
    """
    Serialize Comment Payout Beneficiaries.

    Args:
        beneficiaries (list): A static_variant containing beneficiaries.

    Example:

        ::

            [0,
                {'beneficiaries': [
                    {'account': 'furion', 'weight': 10000}
                ]}
            ]
    """

    def __init__(self, o):
        type_id, data = o
        if type_id == 0:
            data = Beneficiaries(data)
        elif type_id == 1:
            data = Destination(data)
        elif type_id == 2:
            data = Percent(data)
        else:
            raise Exception("Unknown CommentOptionExtension")
        super().__init__(data, type_id)


class IsInviteReferral(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("is_invite_referral", Bool(kwargs["is_invite_referral"]))
                    ]
                )
            )


class InviteExtensions(StaticVariant):
    """
    Serialize Invite Operation Extensions.

    Args:
        is_invite_referral (bool): If someone will create account with that invite, should it be referral of invite creator or not.

    Example:

        ::

            [0,
                {'is_invite_referral': True}
            ]
    """

    def __init__(self, o):
        type_id, data = o
        if type_id == 0:
            data = IsInviteReferral(data)
        else:
            raise Exception("Unknown InviteExtension")
        super().__init__(data, type_id)


class PairToCancel(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("base", String(kwargs["base"])),
                        ("quote", String(kwargs["quote"])),
                        ("reverse", Bool(kwargs["reverse"]))
                    ]
                )
            )


class LimitOrderCancelExExtensions(StaticVariant):
    """
    Serialize LimitOrderCancelEx Operation Extensions.

    Args:
        base (string): Base asset in the pair.
        quote (string): Quote asset in the pair.
        reverse (bool): If True, also cancel orders with reversed pair (e.g. GBG/GOLOS when pair is GOLOS/GBG).

    Example:

        ::

            [0,
                {'base': 'GOLOS', 'quote': 'GBG', 'reverse': True}
            ]
    """

    def __init__(self, o):
        type_id, data = o
        if type_id == 0:
            data = PairToCancel(data)
        else:
            raise Exception("Unknown LimitOrderCancelExExtension")
        super().__init__(data, type_id)


########################################################
# Actual Operations
########################################################


class AccountCreate(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.pop("prefix", default_prefix)

            assert len(kwargs["new_account_name"]) <= 16, "Account name must be at most 16 chars long"

            meta = ""
            if "json_metadata" in kwargs and kwargs["json_metadata"]:
                if isinstance(kwargs["json_metadata"], dict):
                    meta = json.dumps(kwargs["json_metadata"])
                else:
                    meta = kwargs["json_metadata"]
            super().__init__(
                OrderedDict(
                    [
                        ("fee", Amount(kwargs["fee"])),
                        ("creator", String(kwargs["creator"])),
                        ("new_account_name", String(kwargs["new_account_name"])),
                        ("owner", Permission(kwargs["owner"], prefix=prefix)),
                        ("active", Permission(kwargs["active"], prefix=prefix)),
                        ("posting", Permission(kwargs["posting"], prefix=prefix)),
                        ("memo_key", PublicKey(kwargs["memo_key"], prefix=prefix)),
                        ("json_metadata", String(meta)),
                    ]
                )
            )


class AccountCreateWithDelegation(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.pop("prefix", default_prefix)

            assert len(kwargs["new_account_name"]) <= 16, "Account name must be at most 16 chars long"

            meta = ""
            if "json_metadata" in kwargs and kwargs["json_metadata"]:
                if isinstance(kwargs["json_metadata"], dict):
                    meta = json.dumps(kwargs["json_metadata"])
                else:
                    meta = kwargs["json_metadata"]
            super().__init__(
                OrderedDict(
                    [
                        ("fee", Amount(kwargs["fee"])),
                        ("delegation", Amount(kwargs["delegation"])),
                        ("creator", String(kwargs["creator"])),
                        ("new_account_name", String(kwargs["new_account_name"])),
                        ("owner", Permission(kwargs["owner"], prefix=prefix)),
                        ("active", Permission(kwargs["active"], prefix=prefix)),
                        ("posting", Permission(kwargs["posting"], prefix=prefix)),
                        ("memo_key", PublicKey(kwargs["memo_key"], prefix=prefix)),
                        ("json_metadata", String(meta)),
                        ("extensions", Array([])),
                    ]
                )
            )


class AccountUpdate(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.pop("prefix", default_prefix)

            meta = ""
            if "json_metadata" in kwargs and kwargs["json_metadata"]:
                if isinstance(kwargs["json_metadata"], dict):
                    meta = json.dumps(kwargs["json_metadata"])
                else:
                    meta = kwargs["json_metadata"]

            owner = Permission(kwargs["owner"], prefix=prefix) if "owner" in kwargs else None
            active = Permission(kwargs["active"], prefix=prefix) if "active" in kwargs else None
            posting = Permission(kwargs["posting"], prefix=prefix) if "posting" in kwargs else None

            super().__init__(
                OrderedDict(
                    [
                        ("account", String(kwargs["account"])),
                        ("owner", Optional(owner)),
                        ("active", Optional(active)),
                        ("posting", Optional(posting)),
                        ("memo_key", PublicKey(kwargs["memo_key"], prefix=prefix)),
                        ("json_metadata", String(meta)),
                    ]
                )
            )


class AccountMetadata(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            meta = ""
            if kwargs.get("json_metadata"):
                if isinstance(kwargs["json_metadata"], dict):
                    meta = json.dumps(kwargs["json_metadata"])
                else:
                    meta = kwargs["json_metadata"]

            super().__init__(OrderedDict([("account", String(kwargs["account"])), ("json_metadata", String(meta)),]))


class Transfer(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            if "memo" not in kwargs:
                kwargs["memo"] = ""
            super().__init__(
                OrderedDict(
                    [
                        ("from", String(kwargs["from"])),
                        ("to", String(kwargs["to"])),
                        ("amount", Amount(kwargs["amount"])),
                        ("memo", String(kwargs["memo"])),
                    ]
                )
            )


class TransferToVesting(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("from", String(kwargs["from"])),
                        ("to", String(kwargs["to"])),
                        ("amount", Amount(kwargs["amount"])),
                    ]
                )
            )


class WithdrawVesting(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [("account", String(kwargs["account"])), ("vesting_shares", Amount(kwargs["vesting_shares"])),]
                )
            )


class TransferToSavings(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            if "memo" not in kwargs:
                kwargs["memo"] = ""
            super().__init__(
                OrderedDict(
                    [
                        ("from", String(kwargs["from"])),
                        ("to", String(kwargs["to"])),
                        ("amount", Amount(kwargs["amount"])),
                        ("memo", String(kwargs["memo"])),
                    ]
                )
            )


class TransferFromSavings(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            if "memo" not in kwargs:
                kwargs["memo"] = ""

            super().__init__(
                OrderedDict(
                    [
                        ("from", String(kwargs["from"])),
                        ("request_id", Uint32(int(kwargs["request_id"]))),
                        ("to", String(kwargs["to"])),
                        ("amount", Amount(kwargs["amount"])),
                        ("memo", String(kwargs["memo"])),
                    ]
                )
            )


class CancelTransferFromSavings(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict([("from", String(kwargs["from"])), ("request_id", Uint32(int(kwargs["request_id"]))),])
            )


class ClaimRewardBalance(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("account", String(kwargs["account"])),
                        ("reward_steem", Amount(kwargs["reward_steem"])),
                        ("reward_sbd", Amount(kwargs["reward_sbd"])),
                        ("reward_vests", Amount(kwargs["reward_vests"])),
                    ]
                )
            )


class DelegateVestingShares(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("delegator", String(kwargs["delegator"])),
                        ("delegatee", String(kwargs["delegatee"])),
                        ("vesting_shares", Amount(kwargs["vesting_shares"])),
                    ]
                )
            )


class DelegateVestingSharesWithInterest(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("delegator", String(kwargs["delegator"])),
                        ("delegatee", String(kwargs["delegatee"])),
                        ("vesting_shares", Amount(kwargs["vesting_shares"])),
                        ("interest_rate", Uint16(kwargs["interest_rate"])),
                        ("extensions", Array(kwargs.get("extensions") or [])),
                    ]
                )
            )


class LimitOrderCreate(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("owner", String(kwargs["owner"])),
                        ("orderid", Uint32(int(kwargs["orderid"]))),
                        ("amount_to_sell", Amount(kwargs["amount_to_sell"])),
                        ("min_to_receive", Amount(kwargs["min_to_receive"])),
                        ("fill_or_kill", Bool(kwargs["fill_or_kill"])),
                        ("expiration", PointInTime(kwargs["expiration"])),
                    ]
                )
            )


class LimitOrderCancel(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("owner", String(kwargs["owner"])),
                        ("orderid", Uint32(int(kwargs["orderid"]))),
                    ]
                )
            )


class LimitOrderCancelEx(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            new_extensions = []

            if "pair_to_cancel" in kwargs and kwargs["pair_to_cancel"]:
                new_extensions.append([0, kwargs["pair_to_cancel"]])

            if new_extensions:
                kwargs["extensions"] = new_extensions

            extensions = Array([])
            if "extensions" in kwargs and kwargs["extensions"]:
                extensions = Array([LimitOrderCancelExExtensions(o) for o in kwargs["extensions"]])

            if "orderid" not in kwargs:
                kwargs["orderid"] = 0

            super().__init__(
                OrderedDict(
                    [
                        ("owner", String(kwargs["owner"])),
                        ("orderid", Uint32(int(kwargs["orderid"]))),
                        ("extensions", extensions),
                    ]
                )
            )


class SetWithdrawVestingRoute(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("from_account", String(kwargs["from_account"])),
                        ("to_account", String(kwargs["to_account"])),
                        ("percent", Uint16((kwargs["percent"]))),
                        ("auto_vest", Bool(kwargs["auto_vest"])),
                    ]
                )
            )


class Convert(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("owner", String(kwargs["owner"])),
                        ("requestid", Uint32(kwargs["requestid"])),
                        ("amount", Amount(kwargs["amount"])),
                    ]
                )
            )


class FeedPublish(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("publisher", String(kwargs["publisher"])),
                        ("exchange_rate", ExchangeRate(kwargs["exchange_rate"])),
                    ]
                )
            )


class WitnessUpdate(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.pop("prefix", default_prefix)

            if not kwargs["block_signing_key"]:
                kwargs["block_signing_key"] = "GLS1111111111111111111111111111111114T1Anm"
            super().__init__(
                OrderedDict(
                    [
                        ("owner", String(kwargs["owner"])),
                        ("url", String(kwargs["url"])),
                        ("block_signing_key", PublicKey(kwargs["block_signing_key"], prefix=prefix)),
                        ("props", ChainProperties(kwargs["props"])),
                        ("fee", Amount(kwargs["fee"])),
                    ]
                )
            )


class ChainPropertiesUpdate(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            props = kwargs.get("props")

            # A hack to extract properties at the second op processing in transactionbuilder
            if props and type(props) == list:
                props = props[1]

            if props and type(props) == dict:
                type_id = 0
                if "min_delegation" in props:
                    type_id = 1
                if "auction_window_size" in props:
                    type_id = 2
                if "worker_reward_percent" in props:
                    type_id = 3
                if "claim_idleness_time" in props:
                    type_id = 4
                if "asset_creation_fee" in props:
                    type_id = 5
                if "convert_fee_percent" in props:
                    type_id = 6

                obj = [type_id, {"props": props}]
                props = Props(obj)

            super().__init__(OrderedDict([("owner", String(kwargs["owner"])), ("props", props),]))


class AccountWitnessVote(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("account", String(kwargs["account"])),
                        ("witness", String(kwargs["witness"])),
                        ("approve", Bool(bool(kwargs["approve"]))),
                    ]
                )
            )


class CustomJson(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            if "json" in kwargs and kwargs["json"]:
                if isinstance(kwargs["json"], dict) or isinstance(kwargs["json"], list):
                    js = json.dumps(kwargs["json"])
                else:
                    js = kwargs["json"]

            if len(kwargs["id"]) > 32:
                raise Exception("'id' too long")

            super().__init__(
                OrderedDict(
                    [
                        ("required_auths", Array([String(o) for o in kwargs["required_auths"]])),
                        ("required_posting_auths", Array([String(o) for o in kwargs["required_posting_auths"]])),
                        ("id", String(kwargs["id"])),
                        ("json", String(js)),
                    ]
                )
            )


class CommentOptions(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            new_extensions = []

            # handle beneficiaries
            if "beneficiaries" in kwargs and kwargs["beneficiaries"]:
                new_extensions.append([0, {"beneficiaries": kwargs["beneficiaries"]}])

            if "auction_window_reward_destination" in kwargs and kwargs["auction_window_reward_destination"]:
                new_extensions.append([1, {"destination": kwargs["auction_window_reward_destination"]}])

            if "curation_rewards_percent" in kwargs and kwargs["curation_rewards_percent"]:
                new_extensions.append([2, {"percent": kwargs["curation_rewards_percent"]}])

            if new_extensions:
                kwargs["extensions"] = new_extensions

            extensions = Array([])
            if "extensions" in kwargs and kwargs["extensions"]:
                extensions = Array([CommentOptionExtensions(o) for o in kwargs["extensions"]])

            super().__init__(
                OrderedDict(
                    [
                        ("author", String(kwargs["author"])),
                        ("permlink", String(kwargs["permlink"])),
                        ("max_accepted_payout", Amount(kwargs["max_accepted_payout"])),
                        ("percent_steem_dollars", Uint16(int(kwargs["percent_steem_dollars"]))),
                        ("allow_votes", Bool(bool(kwargs["allow_votes"]))),
                        ("allow_curation_rewards", Bool(bool(kwargs["allow_curation_rewards"]))),
                        ("extensions", extensions),
                    ]
                )
            )


class ProposalCreate(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            assert kwargs["proposed_operations"], "proposed_operations cannot be empty!"

            if isinstance(kwargs["proposed_operations"][0], GrapheneObject):
                proposed_operations = [OperationWrapper(Operation(op)) for op in kwargs["proposed_operations"]]
            else:
                proposed_operations = [OperationWrapper(Operation(op["op"])) for op in kwargs["proposed_operations"]]

            review_period_time = PointInTime(kwargs["review_period_time"]) if kwargs.get("review_period_time") else None

            super().__init__(
                OrderedDict(
                    [
                        ("author", String(kwargs["author"])),
                        ("title", String(kwargs["title"])),
                        ("memo", String(kwargs.get("memo", ""))),
                        ("expiration_time", PointInTime(kwargs["expiration_time"])),
                        ("proposed_operations", Array(proposed_operations)),
                        ("review_period_time", Optional(review_period_time)),
                        ("extensions", Array(kwargs.get("extensions") or [])),
                    ]
                )
            )


class ProposalUpdate(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            active_approvals_to_add = [String(str(x)) for x in kwargs.get("active_approvals_to_add") or []]
            active_approvals_to_remove = [String(str(x)) for x in kwargs.get("active_approvals_to_remove") or []]
            owner_approvals_to_add = [String(str(x)) for x in kwargs.get("owner_approvals_to_add") or []]
            owner_approvals_to_remove = [String(str(x)) for x in kwargs.get("owner_approvals_to_remove") or []]
            posting_approvals_to_add = [String(str(x)) for x in kwargs.get("posting_approvals_to_add") or []]
            posting_approvals_to_remove = [String(str(x)) for x in kwargs.get("posting_approvals_to_remove") or []]
            key_approvals_to_add = [String(str(x)) for x in kwargs.get("key_approvals_to_add") or []]
            key_approvals_to_remove = [String(str(x)) for x in kwargs.get("key_approvals_to_remove") or []]

            super().__init__(
                OrderedDict(
                    [
                        ("author", String(kwargs["author"])),
                        ("title", String(kwargs["title"])),
                        ("active_approvals_to_add", Array(active_approvals_to_add)),
                        ("active_approvals_to_remove", Array(active_approvals_to_remove)),
                        ("owner_approvals_to_add", Array(owner_approvals_to_add)),
                        ("owner_approvals_to_remove", Array(owner_approvals_to_remove)),
                        ("posting_approvals_to_add", Array(posting_approvals_to_add)),
                        ("posting_approvals_to_remove", Array(posting_approvals_to_remove)),
                        ("key_approvals_to_add", Array(key_approvals_to_add)),
                        ("key_approvals_to_remove", Array(key_approvals_to_remove)),
                        ("extensions", Array(kwargs.get("extensions") or [])),
                    ]
                )
            )


class ProposalDelete(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("author", String(kwargs["author"])),
                        ("title", String(kwargs["title"])),
                        ("requester", String(kwargs["requester"])),
                        ("extensions", Array(kwargs.get("extensions") or [])),
                    ]
                )
            )


class Claim(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("from", String(kwargs["from"])),
                        ("to", String(kwargs["to"])),
                        ("amount", Amount(kwargs["amount"])),
                        ("to_vesting", Bool(bool(kwargs["to_vesting"]))),
                        ("extensions", Array([])),
                    ]
                )
            )


class VariantObject(GrapheneObject):
    """
    Represents fc::variant_object.

    variant_object is a dict-like structure with keys and values, where keys are always strings, and values could be
    anything. We provide here only limited set of values recognition.
    """

    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            self.data = OrderedDict()
            for key, value in kwargs.items():
                if isinstance(value, str):
                    _value = String(value)
                elif isinstance(value, int):
                    if value > 0:
                        _value = Uint64(value)
                    else:
                        _value = Int64(value)

                self.data[key] = _value

    def __bytes__(self):
        if self.data is None:
            return bytes()

        # Encode number of elements
        b = varint(len(self.data))
        for name, value in self.data.items():
            # All keys are strings
            b += bytes(String(name))

            if isinstance(value, String):
                b += b"\x05"  # delimiter
            elif isinstance(value, Int64):
                b += b"\x01"
            else:
                b += b"\x02"
            b += bytes(value)
        return b


class DonateMemo(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            comment = String(kwargs["comment"]) if kwargs.get("comment") else None

            super().__init__(
                OrderedDict(
                    [
                        ("app", String(kwargs["app"])),
                        ("version", Uint16(int(kwargs["version"]))),
                        ("target", kwargs["target"]),
                        ("comment", Optional(comment)),
                    ]
                )
            )


class Donate(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            super().__init__(
                OrderedDict(
                    [
                        ("from", String(kwargs["from"])),
                        ("to", String(kwargs["to"])),
                        ("amount", Amount(kwargs["amount"])),
                        ("memo", kwargs["memo"]),
                        ("extensions", Array([])),
                    ]
                )
            )


class TransferToTip(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            if "memo" not in kwargs:
                kwargs["memo"] = ""
            super().__init__(
                OrderedDict(
                    [
                        ("from", String(kwargs["from"])),
                        ("to", String(kwargs["to"])),
                        ("amount", Amount(kwargs["amount"])),
                        ("memo", String(kwargs["memo"])),
                        ("extensions", Array(kwargs.get("extensions") or [])),
                    ]
                )
            )


class TransferFromTip(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            if "memo" not in kwargs:
                kwargs["memo"] = ""
            super().__init__(
                OrderedDict(
                    [
                        ("from", String(kwargs["from"])),
                        ("to", String(kwargs["to"])),
                        ("amount", Amount(kwargs["amount"])),
                        ("memo", String(kwargs["memo"])),
                        ("extensions", Array(kwargs.get("extensions") or [])),
                    ]
                )
            )


class Invite(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.pop("prefix", default_prefix)

            new_extensions = []

            if "is_invite_referral" in kwargs and kwargs["is_invite_referral"]:
                new_extensions.append([0, {"is_invite_referral": kwargs["is_invite_referral"]}])

            if new_extensions:
                kwargs["extensions"] = new_extensions

            extensions = Array([])
            if "extensions" in kwargs and kwargs["extensions"]:
                extensions = Array([InviteExtensions(o) for o in kwargs["extensions"]])

            super().__init__(
                OrderedDict(
                    [
                        ("creator", String(kwargs["creator"])),
                        ("balance", Amount(kwargs["balance"])),
                        ("invite_key", PublicKey(kwargs["invite_key"], prefix=prefix)),
                        ("extensions", extensions),
                    ]
                )
            )


class InviteClaim(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("initiator", String(kwargs["initiator"])),
                        ("receiver", String(kwargs["receiver"])),
                        ("invite_secret", String(kwargs["invite_secret"])),
                        ("extensions", Array(kwargs.get("extensions") or [])),
                    ]
                )
            )


class AssetCreate(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("creator", String(kwargs["creator"])),
                        ("max_supply", Amount(kwargs["max_supply"])),
                        ("allow_fee", Bool(kwargs["allow_fee"])),
                        ("allow_override_transfer", Bool(kwargs["allow_override_transfer"])),
                        ("json_metadata", String(kwargs["json_metadata"])),
                        ("extensions", Array(kwargs.get("extensions") or [])),
                    ]
                )
            )


class AssetUpdate(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("creator", String(kwargs["creator"])),
                        ("symbol", String(kwargs["symbol"])),
                        ("symbols_whitelist", Array([String(o) for o in kwargs["symbols_whitelist"]])),
                        ("fee_percent", Uint16(kwargs["fee_percent"])),
                        ("json_metadata", String(kwargs["json_metadata"])),
                        ("extensions", Array(kwargs.get("extensions") or [])),
                    ]
                )
            )


class AssetIssue(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("creator", String(kwargs["creator"])),
                        ("amount", Amount(kwargs["amount"])),
                        ("to", String(kwargs["to"])),
                        ("extensions", Array(kwargs.get("extensions") or [])),
                    ]
                )
            )


class AssetTransfer(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("creator", String(kwargs["creator"])),
                        ("symbol", String(kwargs["symbol"])),
                        ("new_owner", String(kwargs["new_owner"])),
                        ("extensions", Array(kwargs.get("extensions") or [])),
                    ]
                )
            )


class OverrideTransfer(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            if "memo" not in kwargs:
                kwargs["memo"] = ""
            super().__init__(
                OrderedDict(
                    [
                        ("creator", String(kwargs["creator"])),
                        ("from", String(kwargs["from"])),
                        ("to", String(kwargs["to"])),
                        ("amount", Amount(kwargs["amount"])),
                        ("memo", String(kwargs["memo"])),
                        ("extensions", Array(kwargs.get("extensions") or [])),
                    ]
                )
            )


class InviteDonate(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            if "memo" not in kwargs:
                kwargs["memo"] = ""
            super().__init__(
                OrderedDict(
                    [
                        ("from", String(kwargs["from"])),
                        ("invite_key", PublicKey(kwargs["invite_key"])),
                        ("amount", Amount(kwargs["amount"])),
                        ("memo", String(kwargs["memo"])),
                        ("extensions", Array(kwargs.get("extensions") or [])),
                    ]
                )
            )


class InviteTransfer(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            if "memo" not in kwargs:
                kwargs["memo"] = ""
            super().__init__(
                OrderedDict(
                    [
                        ("from", PublicKey(kwargs["from"])),
                        ("to", PublicKey(kwargs["to"])),
                        ("amount", Amount(kwargs["amount"])),
                        ("memo", String(kwargs["memo"])),
                        ("extensions", Array(kwargs.get("extensions") or [])),
                    ]
                )
            )


class WorkerRequestDelete(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("author", String(kwargs["author"])),
                        ("permlink", String(kwargs["permlink"])),
                        ("extensions", Array(kwargs.get("extensions") or [])),
                    ]
                )
            )


class WorkerRequestVote(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("voter", String(kwargs["voter"])),
                        ("author", String(kwargs["author"])),
                        ("permlink", String(kwargs["permlink"])),
                        ("vote_percent", Uint16(kwargs["vote_percent"])),
                        ("extensions", Array(kwargs.get("extensions") or [])),
                    ]
                )
            )


def isArgsThisClass(self, args):
    return len(args) == 1 and type(args[0]).__name__ == type(self).__name__
