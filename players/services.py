from .models import Referral, User


def apply_referral_code(invited_user, referral_code):
    try:
        inviter = User.objects.get(referral_code=referral_code)

        # بررسی اینکه کاربر از قبل زیرمجموعه کسی نباشد
        if hasattr(invited_user, 'invited_by'):
            raise Exception("این کاربر قبلاً از طریق یک کد دعوت وارد شده است.")

        # ساختن رابطه ریفرال
        referral = Referral(inviter=inviter, invited_user=invited_user)
        referral.save()

        # پیام موفقیت‌آمیز بودن
        return f"کاربر {invited_user.name} با موفقیت از طریق {inviter.name} دعوت شد."

    except User.DoesNotExist:
        raise Exception("کد دعوت معتبر نیست.")
