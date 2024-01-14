import asyncio
from datetime import datetime, timedelta

from girok.core.authentication.token_manager import TokenManager
from girok.core.email.email_manager import EmailManager
from girok.core.exceptions.emitter import raise_custom_exception
from girok.core.utils.auth import generate_email_verification_code
from girok.domain.auth.entity import EmailVerification
from girok.domain.auth.repository.email_verification_repository import (
    EmailVerificationRepository,
)
from girok.domain.exceptions import DomainExceptions


class AuthService:
    def __init__(
        self,
        email_verification_repository: EmailVerificationRepository,
        token_manager: TokenManager,
        email_manager: EmailManager,
    ):
        self.email_verification_repository = email_verification_repository
        self.token_manager = token_manager
        self.email_manager = email_manager

    async def send_email_verification_code(self, email: str) -> None:
        verification_code = generate_email_verification_code()
        content = self.email_manager.read_and_format_html(replacements={"__VERIFICATION_CODE__": verification_code})
        asyncio.create_task(
            self.email_manager.send_email(recipient=email, subject="Please verify your email address.", content=content)
        )

        # Refresh email verification entry (email, verification_code, expiration_time, is_verified=False)
        email_verification = EmailVerification(
            email=email,
            verification_code=verification_code,
            is_verified=False,
            expiration_time=datetime.now() + timedelta(minutes=30),
        )
        await self.email_verification_repository.upsert_email_verification(email_verification=email_verification)

    async def verify_email_verification_code(self, email: str, code: str) -> None:
        email_verification: EmailVerification = (
            await self.email_verification_repository.get_email_verification_or_none_by_email(email=email)
        )

        # Check if verification code was sent
        if not email_verification:
            raise_custom_exception(DomainExceptions.EMAIL_VERIFICATION_NOT_FOUND)

        # Check if email is already verified
        if email_verification.check_verified():
            raise_custom_exception(DomainExceptions.EMAIL_ALREADY_VERIFIED)

        # Check valid verification code
        if email_verification.verification_code != code:
            raise_custom_exception(DomainExceptions.INVALID_VERIFICATION_CODE)

        # Check if verification code is expired
        if email_verification.is_expired():
            raise_custom_exception(DomainExceptions.VERIFICATION_CODE_EXPIRED)

        # Verification successful. Update email verification entry.
        email_verification.verify()
        await self.email_verification_repository.upsert_email_verification(email_verification=email_verification)

    async def check_email_verified(self, email: str, verification_code: str) -> None:
        email_verification = await self.email_verification_repository.get_email_verification_or_none_by_email(
            email=email
        )

        if not email_verification:
            raise_custom_exception(DomainExceptions.EMAIL_NOT_VERIFIED)

        if email_verification.verification_code != verification_code:
            raise_custom_exception(DomainExceptions.INVALID_VERIFICATION_CODE)

        if not email_verification.check_verified():
            raise_custom_exception(DomainExceptions.EMAIL_NOT_VERIFIED)

    async def login(self, email: str, password: str) -> dict:
        pass
