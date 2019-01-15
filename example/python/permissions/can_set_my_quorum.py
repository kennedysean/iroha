#
# Copyright Soramitsu Co., Ltd. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
#

import irohalib
import commons
import primitive_pb2

admin = commons.new_user('admin@test')
alice = commons.new_user('alice@test')
bob = commons.new_user('bob@test')
iroha = irohalib.Iroha(admin['id'])


@commons.hex
def genesis_tx():
    test_permissions = [
        primitive_pb2.can_grant_can_set_my_quorum,
        primitive_pb2.can_add_signatory
    ]
    genesis_commands = commons.genesis_block(admin, alice, test_permissions)
    genesis_commands.append(
        iroha.command('CreateAccount', account_name='bob', domain_id='test',
                      public_key=commons.public_key_bytes(bob['key']))
    )
    tx = iroha.transaction(genesis_commands)
    irohalib.IrohaCrypto.sign_transaction(tx, admin['key'])
    return tx


@commons.hex
def grant_can_set_my_quorum_tx():
    extra_key = irohalib.IrohaCrypto.private_key()
    tx = iroha.transaction([
        iroha.command('GrantPermission', account_id=bob['id'], permission=primitive_pb2.can_set_my_quorum),
        iroha.command('AddSignatory', account_id=alice['id'], public_key=commons.public_key_bytes(extra_key))
    ], creator_account=alice['id'])
    irohalib.IrohaCrypto.sign_transaction(tx, alice['key'])
    return tx


@commons.hex
def set_quorum_tx():
    tx = iroha.transaction([
        iroha.command('SetAccountQuorum', account_id=alice['id'], quorum=2)
    ], creator_account=bob['id'])
    irohalib.IrohaCrypto.sign_transaction(tx, bob['key'])
    return tx
