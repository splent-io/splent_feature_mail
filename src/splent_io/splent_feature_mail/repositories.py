from splent_io.splent_feature_mail.models import Mail
from splent_framework.repositories.BaseRepository import BaseRepository


class MailRepository(BaseRepository):
    def __init__(self):
        super().__init__(Mail)
