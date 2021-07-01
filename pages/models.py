from django.db import models

class Pages(models.Model):
    """Таблица страницы"""
    page_name = models.CharField('Название страницы',max_length=100)
    slug = models.SlugField('URL страницы',help_text='Url можно изменить')
    main_title = models.CharField('Главный заголовок',max_length=200,blank=True,null=True,help_text='Необязательное поле')

    def __str__(self):
        return self.page_name

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'

class Section(models.Model):
    """Таблица информации на странице, fk к основой таблице страницы( Pages )"""
    pages = models.ForeignKey(Pages,related_name='section',on_delete=models.CASCADE)
    second_title = models.CharField('Второстепенный заголовок',null=True,blank=True,max_length=200,help_text='Необязательное поле')

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

class Body(models.Model):
    """Таблица текста, fk к заголовку(таблица section)"""
    section = models.ForeignKey(Section,related_name='body',on_delete=models.CASCADE)
    body = models.TextField('Текст',blank=True,null=True,help_text='Необязательное поле')

    class Meta:
        verbose_name = 'Текст'
        verbose_name_plural = 'Текст'

class List(models.Model):
    """Таблица для списков, fk к заголовку(таблица section)"""
    section = models.ForeignKey(Section,related_name='list',on_delete=models.CASCADE)
    list = models.CharField('Список', max_length=150,blank=True, null=True, help_text='Необязательное поле')

    class Meta:
        verbose_name = 'Список'
        verbose_name_plural = 'Список'

class Contact(models.Model):
    """Таблица контактов"""
    phone = models.CharField('Номер для связи',max_length=50)
    whats_app = models.CharField('Номер WhatsApp',max_length=50)
    telegram = models.CharField('Telegram',max_length=50)
    email = models.CharField('Email адрес',max_length=50)

    class Meta:
        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'
    