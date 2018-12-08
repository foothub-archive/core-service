import uuid
from typing import Optional, List

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import IntegrityError
from faker import Faker

from profiles.models import Profile
from friendships.models import FriendshipInvitation


class SomethingWentWrongException(Exception):
    pass


class Command(BaseCommand):
    help = 'Generates fake data for development purposes\n' \
           'Usage example:\n' \
           './manage.py generate_fake_data -v 3 --profiles 100 --heroes 2 --invited_f 5\n' \
           'This would create 100 new Profile items, ' \
           'find the Profile with id=2 (hero),' \
           'create 5 FriendshipInvitation with hero as invited'

    def add_arguments(self, parser):
        parser.add_argument(
            '--heroes',
            dest='heroes',
            nargs='+',
            help="Tag profiles as heroes using their id. "
                 "Heroes are the target special operations and are never deleted"
        )

        parser.add_argument(
            '--profiles',
            dest='profiles',
            type=int,
            help="number of profiles to generate",
        )

        parser.add_argument(
            '--inviting_f',
            dest='inviting_f',
            type=int,
            help="number of friendship invitations to generate for each hero as the inviting Profile",
        )

        parser.add_argument(
            '--invited_f',
            dest='invited_f',
            type=int,
            help="number of friendship invitations to generate for each hero as the invited Profile",
        )

        parser.add_argument(
            '--force',
            dest='force',
            action='store_true',
            help="Ignores environment (dev / production). Use with care as you can wipe out the db!",
        )

    def print_error(self, msg: str) -> None:
        self.stdout.write(self.style.ERROR(msg))

    def print_warning(self, msg: str) -> None:
        self.stdout.write(self.style.WARNING(msg))

    def print_success(self, msg: str) -> None:
        self.stdout.write(self.style.SUCCESS(msg))

    def get_heroes(self, hero_ids: Optional[List[int]]) -> List[Profile]:
        """
        Finds our heroes among all those profiles
        """
        heroes: list = []
        if isinstance(hero_ids, list):
            self.print_success(f"Finding heroes with ids {hero_ids}")
            heroes = list(Profile.objects.filter(id__in=hero_ids))
            if len(heroes) != len(hero_ids):
                self.print_error("Failed to find at least one hero. Aborting")
                raise SomethingWentWrongException
            else:
                self.print_success(f"Heroes found!")
        return heroes

    def generate_profiles(self, n: Optional[int]) -> None:
        """
        Generates new Profiles with random uuid and name
        """
        if isinstance(n, int):
            self.print_success(f"Generating {n} new Profiles")
            faker = Faker()
            Profile.objects.bulk_create(
                [Profile(external_uuid=uuid.uuid4().hex, name=faker.name()) for _ in range(n)]
            )
            self.print_success(f"New Profiles generated!")

    def _generate_one_f_invitation(self, hero: Profile, invited: bool, retries=15) -> None:
        """
        Recursively tries to create new FriendshipInvitations for a given hero (Profile)
        tries 15 times before concluding that such FriendshipInvitations is not possible to create
        """
        random_profile = Profile.objects.order_by('?').first()
        try:
            if invited:
                FriendshipInvitation.objects.create(inviting=random_profile, invited=hero)
            else:
                FriendshipInvitation.objects.create(inviting=hero, invited=random_profile)
        except IntegrityError:
            if retries == 0:
                # we can be asking for something that is not possible
                # which will lead us here
                # (or we were just very unlucky)  ¯\_(ツ)_/¯
                self.print_error("Unable to create FriendshipInvitations."
                                 " Is it impossible or were you just unlucky?")
                raise SomethingWentWrongException
            self._generate_one_f_invitation(hero, invited, retries - 1)

    def generate_invited_f(self, n: Optional[int], heroes: List[Profile]) -> None:
        """
        Generates new FriendshipInvitations with (hero as invited)
        """
        if isinstance(n, int):
            self.print_success(f"Generating {n} new Friendship Invitations (hero as invited)")
            for hero in heroes:
                for _ in range(n):
                    self._generate_one_f_invitation(hero, True)
            self.print_success(f"New Friendship Invitations generated (hero as invited)")

    def generate_inviting_f(self, n: Optional[int], heroes: List[Profile]) -> None:
        """
        Generates new FriendshipInvitations with (hero as inviting)
        """
        if isinstance(n, int):
            self.print_success(f"Generating {n} new Friendship Invitations (hero as inviting)")
            for hero in heroes:
                for _ in range(n):
                    self._generate_one_f_invitation(hero, False)
            self.print_success(f"New Friendship Invitations generated (hero as inviting)")

    def generate_fake_data(self, *args, **kwargs):
        """
        Manages item creation
        """
        heroes = self.get_heroes(kwargs['heroes'])
        self.generate_profiles(kwargs['profiles'])
        self.generate_invited_f(kwargs['invited_f'], heroes)
        self.generate_inviting_f(kwargs['inviting_f'], heroes)

    def print_input(self, **kwargs):
        """
        Prints input (useful for debug)
        """
        if kwargs['verbosity'] > 2:
            self.print_warning('Command Args')
            for k, v in kwargs.items():
                self.print_warning(f'{k}: {v}')

    def handle(self, *args, **kwargs):
        """
        Command entry point
        """
        self.print_input(**kwargs)
        self.print_success(kwargs['force'])
        if not settings.DEBUG:
            self.print_error("This command is for development only. Use --force if you want to run it anyway")
        else:
            try:
                self.print_success('Starting...')
                self.generate_fake_data(**kwargs)
                self.print_success('Finished successfully.')
            # we will be raising generic exceptions for now, this is a dev command
            except SomethingWentWrongException:
                self.print_error('Aborted.')
