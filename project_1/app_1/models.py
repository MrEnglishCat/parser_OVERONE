from django.db import models


class Mebel(models.Model):
    link = models.TextField('Ссылка:')
    price = models.DecimalField('Цена:', max_digits=10, decimal_places=4)
    description = models.TextField('Описание:')
    parse_datetime = models.DateTimeField(auto_now_add=True, blank=True)
    def get_absolute_url(self):
        return self.link

    def get_str(self):
        return f"{self.price}"

    def __str__(self):
        return f"{self.price} | {self.description}"

    class Meta:
        verbose_name = "Мебель"
        verbose_name_plural = "Мебель"
        # ordering = ['price']
        ordering = ['-price']