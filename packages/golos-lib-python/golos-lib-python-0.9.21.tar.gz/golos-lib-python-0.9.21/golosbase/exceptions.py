def decodeRPCErrorMsg(e):
    """
    Helper function to decode the raised Exception and give it a python Exception class.

    Error codes can be obtained from libraries/protocol/include/golos/protocol/exceptions.hpp
    """
    lines = str(e).strip("\n").split("\n")
    return lines[-1]


class RPCError(Exception):
    pass


class RPCErrorRecoverable(RPCError):
    pass


class NumRetriesReached(Exception):
    pass


class InvalidNodeSchemes(Exception):
    pass


class NoAccessApi(RPCError):
    pass


class AlreadyTransactedThisBlock(RPCError):
    pass


class VoteWeightTooSmall(RPCError):
    pass


class OnlyVoteOnceEvery3Seconds(RPCError):
    pass


class AlreadyVotedSimilarily(RPCError):
    pass


class NoMethodWithName(RPCError):
    pass


class PostOnlyEvery5Min(RPCError):
    pass


class DuplicateTransaction(RPCError):
    pass


class MissingRequiredPostingAuthority(RPCError):
    pass


class UnhandledRPCError(RPCError):
    pass


class ExceededAllowedBandwidth(RPCError):
    pass


class AccountExistsException(Exception):
    pass


class AccountDoesNotExistsException(Exception):
    pass


class InsufficientAuthorityError(Exception):
    pass


class MissingKeyError(Exception):
    pass


class BlockDoesNotExistsException(Exception):
    pass


class WitnessDoesNotExistsException(Exception):
    pass


class InvalidKeyFormat(Exception):
    pass


class NoWallet(Exception):
    pass


class InvalidWifError(Exception):
    pass


class WalletExists(Exception):
    pass


class PostDoesNotExist(Exception):
    pass


class VotingInvalidOnArchivedPost(Exception):
    pass


class ReadLockFail(Exception):
    pass
