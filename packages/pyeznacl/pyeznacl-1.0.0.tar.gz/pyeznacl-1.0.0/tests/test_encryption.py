'''This module tests the various classes and functions in the encryption module'''
import json
import os
import shutil
import time

import nacl.signing
from pyeznacl import CryptoString
from pyeznacl import encryption

def setup_test(name):
	'''Creates a test folder hierarchy'''
	test_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)),'testfiles')
	if not os.path.exists(test_folder):
		os.mkdir(test_folder)

	test_folder = os.path.join(test_folder, name)
	while os.path.exists(test_folder):
		try:
			shutil.rmtree(test_folder)
		except:
			print("Waiting a second for test folder to unlock")
			time.sleep(1.0)
	os.mkdir(test_folder)
	return test_folder


def test_encryptionpair_save():
	'''Tests the save code of the EncryptionPair class'''
	test_folder = setup_test('encryption_encryptionpair_save')

	public_key = CryptoString("CURVE25519:(B2XX5|<+lOSR>_0mQ=KX4o<aOvXe6M`Z5ldINd`")
	private_key = CryptoString("CURVE25519:(Rj5)mmd1|YqlLCUP0vE;YZ#o;tJxtlAIzmPD7b&")
	kp = encryption.EncryptionPair(public_key, private_key)
	keypair_path = os.path.join(test_folder, 'testpair.jk')
	status = encryption.save_encryptionpair(kp, keypair_path)

	assert not status.error(), f"Failed to create saved encryption pair file: {status.info()}"

	with open(keypair_path, encoding='utf8') as fhandle:
		filedata = json.load(fhandle)

	assert filedata['EncryptionKey'] == public_key.as_string(), "Saved data does not match input data"
	assert filedata['DecryptionKey'] == private_key.as_string(), "Saved data does not match input data"


def test_encryptionpair_load():
	'''Tests the load code of the EncryptionPair class'''
	test_folder = setup_test('encryption_encryptionpair_load')

	public_key = CryptoString("CURVE25519:(B2XX5|<+lOSR>_0mQ=KX4o<aOvXe6M`Z5ldINd`")
	private_key = CryptoString("CURVE25519:(Rj5)mmd1|YqlLCUP0vE;YZ#o;tJxtlAIzmPD7b&")
	kp = encryption.EncryptionPair(public_key, private_key)

	keypair_path = os.path.join(test_folder, 'testpair.jk')
	status = encryption.save_encryptionpair(kp, keypair_path)
	assert not status.error(), f"Failed to create saved encryption pair file: {status.info()}"

	status = encryption.load_encryptionpair(keypair_path)
	assert not status.error(), f"Failed to load saved pair file: {status.info()}"

	testpair = status['keypair']

	assert testpair.enctype == kp.enctype, "Loaded data does not match input data"
	assert testpair.public == public_key, "Loaded data does not match input data"
	assert testpair.private == private_key, "Loaded data does not match input data"


def test_encryptionpair_encrypt_decrypt():
	'''Test the encryption and decryption code for the EncryptionPair class'''

	public_key = CryptoString(r"CURVE25519:(B2XX5|<+lOSR>_0mQ=KX4o<aOvXe6M`Z5ldINd`")
	private_key = CryptoString(r"CURVE25519:(Rj5)mmd1|YqlLCUP0vE;YZ#o;tJxtlAIzmPD7b&")
	kp = encryption.EncryptionPair(public_key, private_key)

	test_data = 'This is some encryption test data'
	estatus = kp.encrypt(test_data.encode())
	assert not estatus.error(), 'test_encryptionpair_encrypt_decrypt: error encrypting test data'

	dstatus = kp.decrypt(estatus['data'])
	assert not dstatus.error(), 'test_encryptionpair_encrypt_decrypt: error decrypting test data'
	assert dstatus['data'] == test_data, 'decoded data mismatch'


def test_signpair_save():
	'''Tests the save code of the SigningPair class'''
	test_folder = setup_test('encryption_signpair_save')

	public_key = CryptoString(r"ED25519:PnY~pK2|;AYO#1Z;B%T$2}E$^kIpL=>>VzfMKsDx")
	private_key = CryptoString(r"ED25519:{^A@`5N*T%5ybCU%be892x6%*Rb2rnYd=SGeO4jF")
	sp = encryption.SigningPair(public_key, private_key)

	keypair_path = os.path.join(test_folder, 'testpair.jk')
	status = encryption.save_signingpair(sp, keypair_path)
	assert not status.error(), f"Failed to create saved signing pair file: {status.info()}"

	with open(keypair_path, encoding='utf8') as fhandle:
		filedata = json.load(fhandle)

	assert filedata['VerificationKey'] == public_key.as_string(), \
		"Saved data does not match input data"
	assert filedata['SigningKey'] == private_key.as_string(), "Saved data does not match input data"


def test_signpair_load():
	'''Tests the load code of the SigningPair class'''
	test_folder = setup_test('encryption_signpair_load')

	public_key = CryptoString(r"ED25519:PnY~pK2|;AYO#1Z;B%T$2}E$^kIpL=>>VzfMKsDx")
	private_key = CryptoString(r"ED25519:{^A@`5N*T%5ybCU%be892x6%*Rb2rnYd=SGeO4jF")
	kp = encryption.SigningPair(public_key, private_key)

	keypair_path = os.path.join(test_folder, 'testpair.jk')
	status = encryption.save_signingpair(kp, keypair_path)
	assert not status.error(), f"Failed to create saved signing pair file: {status.info()}"

	status = encryption.load_signingpair(keypair_path)
	assert not status.error(), f"Failed to load saved signing pair file: {status.info()}"

	testpair = status['keypair']

	assert testpair.enctype == kp.enctype, "Loaded data does not match input data"
	assert testpair.public == public_key, "Loaded data does not match input data"
	assert testpair.private == private_key, "Loaded data does not match input data"


def test_signpair_sign_verify():
	'''Tests SigningPair's sign() and verify() methods'''

	public_key = CryptoString(r"ED25519:PnY~pK2|;AYO#1Z;B%T$2}E$^kIpL=>>VzfMKsDx")
	private_key = CryptoString(r"ED25519:{^A@`5N*T%5ybCU%be892x6%*Rb2rnYd=SGeO4jF")
	sp = encryption.SigningPair(public_key, private_key)

	key = nacl.signing.SigningKey(private_key.as_raw())
	signed = key.sign(b'1234567890', encryption.Base85Encoder)
	
	sstatus = sp.sign(b'1234567890')
	assert not sstatus.error(), f"test_signpair_sign_verify: signing failed: {sstatus.info()}"
	assert sstatus['signature'] == 'ED25519:' + signed.signature.decode(), \
		"test_signpair_sign_verify: signature data mismatch"
	
	vstatus = sp.verify(b'1234567890', CryptoString(sstatus['signature']))
	assert not vstatus.error(), f"test_signpair_sign_verify: verification failed: {vstatus.info()}"


def test_secretkey_save_load():
	'''Tests the load code of the SecretKey class'''
	test_folder = setup_test('encryption_secretkey_load')

	sk = encryption.SecretKey(r"XSALSA20:J~T^ko3HCFb$1Z7NudpcJA-dzDpF52IF1Oysh+CY")
	key_path = os.path.join(test_folder, 'testkey.jk')
	status = encryption.save_secretkey(sk, key_path)
	assert not status.error(), f"Failed to create saved secret key file: {status.info()}"

	status = encryption.load_secretkey(key_path)
	assert not status.error(), f"Failed to load saved secret key file: {status.info()}"

	testpair = status['key']

	assert testpair.type == sk.type, "Loaded data does not match input data"
	assert testpair.enctype == sk.enctype, "Loaded data does not match input data"
	assert testpair.key == sk.key, "Loaded data does not match input data"


def test_secretkey_encrypt_decrypt():
	'''Tests SecretKey encryption/decryption'''

	testdata = b'1234567890'

	sk = encryption.SecretKey()
	encstatus = sk.encrypt(testdata)

	decstatus = sk.decrypt(encstatus['data'])
	assert testdata == decstatus['data'], "Decrypted data didn't match"


if __name__ == '__main__':
	test_encryptionpair_save()
	test_encryptionpair_load()
	test_encryptionpair_encrypt_decrypt()
	test_signpair_save()
	test_signpair_load()
	test_signpair_sign_verify()
	test_secretkey_save_load()
	test_secretkey_encrypt_decrypt()
