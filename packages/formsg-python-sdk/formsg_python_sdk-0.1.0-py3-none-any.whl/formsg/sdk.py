from formsg.constants import PUBLIC_KEY_STAGING, PUBLIC_KEY_PRODUCTION

class FormSdk(object):
    def __init__(self, mode: str):
        self.mode = mode
        self.public_key: str
        if self.mode == 'STAGING':
            self.public_key = PUBLIC_KEY_STAGING
        elif self.mode == 'PRODUCTION':
            self.public_key = PUBLIC_KEY_PRODUCTION
        else: # default to prod
            self.public_key = PUBLIC_KEY_PRODUCTION


    def verify(self):
        pass

    def decrypt(self):
        pass

    def decrypt_attachments(self):
        pass