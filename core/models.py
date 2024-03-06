import email
import secrets
from .paystack import PayStack
# from base.models import Wallet
from django.db import models
from django.contrib.auth.models import User
# from .paystack import Paystack

from django.db import models

# Create your models here.

class Payment(models.Model):
    amount = models.PositiveIntegerField()
    ref = models.CharField(max_length=200)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    email = models.EmailField(null=True)
    description = models.CharField(max_length=200, null=True, default=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self) -> str:
        return f"Payment: {self.amount}"



    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)

    def amount_value(self):
        return int(self.amount) * 100
    

    def walletsave(self, *args, **kwargs):
        from base.models import Wallet
        if self.user:
            self.save()
            user_wallet, created = Wallet.objects.get_or_create(user=self.user)
            user_wallet.update_balance()

    # def verify_payment(self):
    #     paystack = Paystack()
    #     try:
    #         status, result = paystack.verify_payment(self.ref, self.amount)
    #         if status:
    #             if 'amount' in result and result['amount'] / 100 == self.amount:
    #                 self.verified = True
    #                 self.save()
    #                 return True
    #     except Exception as e:
    #         print(f"Error during payment verification: {str(e)}")
    #     return False

    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount'] / 100 == self.amount:
                self.verified = True
            self.save()
        if self.verified:
            return True
        return False


    @staticmethod
    def total_payments():
        return Payment.objects.aggregate(models.Sum('amount'))['amount__sum'] or 0
