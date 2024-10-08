# users/management/commands/assign_permissions.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Назначает разрешения группам пользователей'

    def handle(self, *args, **options):
        # Получаем группы
        admins = Group.objects.get(name='Administrators')
        moderators = Group.objects.get(name='Moderators')
        authors = Group.objects.get(name='Authors')
        users = Group.objects.get(name='Users')

        # Получаем разрешения
        permissions = Permission.objects.all()

        # Администраторы получают все разрешения
        admins.permissions.set(permissions)

        # Разрешения для модераторов
        mod_perms = permissions.filter(
            codename__in=[
                'view_article', 'view_news', 'view_comment',
                'approve_comment', 'change_comment', 'delete_comment',
                'publish_article', 'publish_news',
            ]
        )
        moderators.permissions.set(mod_perms)

        # Разрешения для авторов
        author_perms = permissions.filter(
            codename__in=[
                'add_article', 'change_article', 'add_news', 'change_news',
                'view_article', 'view_news', 'view_comment', 'add_comment',
            ]
        )
        authors.permissions.set(author_perms)

        # Разрешения для пользователей
        user_perms = permissions.filter(
            codename__in=[
                'view_article', 'view_news', 'view_comment', 'add_comment',
            ]
        )
        users.permissions.set(user_perms)

        self.stdout.write(self.style.SUCCESS('Разрешения успешно назначены группам.'))
