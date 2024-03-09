from django.db import models


class Mebel(models.Model):
    link = models.TextField('Ссылка:')
    price = models.DecimalField(max_digits=10, decimal_places=4, verbose_name='Цена с kufar.by')
    description = models.TextField(verbose_name='Описание с kufar.by')
    parse_datetime = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Дата добавления')
    update_datetime = models.DateTimeField(blank=True, verbose_name='Дата обновления записи')

    def get_absolute_url(self):
        return self.link

    def get_str(self):
        return f"{self.price}"

    # def __bool__(self):
    #     if any((self.link, self.price, self.description, self.parse_datetime)):
    #         return True
    #     else:
    #         return False

    def __str__(self):
        return f"{self.price} | {self.description}"

    class Meta:
        verbose_name = "Мебель"
        verbose_name_plural = "Мебель"
        # ordering = ['price']
        ordering = ['-price']