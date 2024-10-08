# users/management/commands/create_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.apps import apps

class Command(BaseCommand):
    help = 'Создает группы пользователей и назначает разрешения'

    def handle(self, *args, **kwargs):
        # Создаем группы
        groups = ['Administrators', 'Moderators', 'Authors', 'Users']
        for group_name in groups:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(f'Группа "{group_name}" создана.')

        # Назначаем разрешения группам
        # Получаем все разрешения
        all_permissions = Permission.objects.all()

        # Administrators получают все разрешения
        admin_group = Group.objects.get(name='Administrators')
        admin_group.permissions.set(all_permissions)

        # Moderators получают разрешения на изменение и удаление контента
        moderator_group = Group.objects.get(name='Moderators')
        mod_permissions = Permission.objects.filter(codename__in=['add_comment', 'change_comment', 'delete_comment'])
        moderator_group.permissions.set(mod_permissions)

        # Authors получают разрешения на добавление и изменение своих статей
        author_group = Group.objects.get(name='Authors')
        author_permissions = Permission.objects.filter(codename__in=['add_article', 'change_article'])
        author_group.permissions.set(author_permissions)

        # Users получают разрешения на добавление комментариев
        user_group = Group.objects.get(name='Users')
        user_permissions = Permission.objects.filter(codename='add_comment')
        user_group.permissions.set(user_permissions)

        self.stdout.write('Группы и разрешения успешно созданы и настроены.')
