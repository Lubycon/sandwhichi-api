from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, username, has_terms, has_privacy_policy, password=None):
        """
        주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            has_terms=has_terms,
            has_privacy_policy=has_privacy_policy
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password):

        user = self.create_user(
            email,
            password=password,
            username=username,
            has_terms=True,
            has_privacy_policy=True
        )
        user.is_admin = True
        user.save(using=self._db)

        return user