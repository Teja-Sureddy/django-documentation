from .account.signup import CustomSignupForm
from .account.login import CustomLoginForm
from .account.password_reset import CustomPasswordResetForm
from .account.password_reset_key import CustomPasswordResetKeyForm
from .account.reauthenticate import CustomReauthenticateForm
from .mfa.activate_totp import CustomActivateTOTPForm
from .mfa.authentication import CustomAuthenticateForm
from .profile import ProfilePicForm, ProofForm, DescriptionForm
