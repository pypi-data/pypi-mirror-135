from formsg.util.crypto import decrypt_content
from typing import Optional
from typing_extensions import TypedDict


DecryptParams = TypedDict(
    "DecryptParams",
    {"encrypted_content": str, "version": str, "verified_content": Optional[str]},
)


class Crypto(object):
    def __init__(self, signing_public_key: str):
        self.signing_public_key = signing_public_key

    """
    /**
    * Decrypts an encrypted submission and returns it.
    * @param formSecretKey The base-64 secret key of the form to decrypt with.
    * @param decryptParams The params containing encrypted content and information.
    * @param decryptParams.encryptedContent The encrypted content encoded with base-64.
    * @param decryptParams.version The version of the payload. Used to determine the decryption process to decrypt the content with.
    * @param decryptParams.verifiedContent Optional. The encrypted and signed verified content. If given, the signingPublicKey will be used to attempt to open the signed message.
    * @returns The decrypted content if successful. Else, null will be returned.
    * @throws {MissingPublicKeyError} if a public key is not provided when instantiating this class and is needed for verifying signed content.
    */
    """

    def decrypt(self, form_secret_key: str, decrypt_params: DecryptParams):
        decrypted_content = decrypt_content(form_secret_key, decrypt_params["encrypted_content"])
        # nacl.exceptions.CryptoError?
        return decrypted_content
