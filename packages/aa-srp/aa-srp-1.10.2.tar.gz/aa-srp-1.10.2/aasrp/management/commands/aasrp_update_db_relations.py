"""
Update DB relations
"""

# Django
from django.core.management.base import BaseCommand

# Alliance Auth (External Libs)
from eveuniverse.models import EveType

# AA SRP
from aasrp.managers import AaSrpManager
from aasrp.models import AaSrpRequest


def get_input(text):
    """
    wrapped input to update DB relations
    """

    return input(text)


class Command(BaseCommand):
    help = "Update DB Relations"

    def _update_relations(self) -> None:
        """
        updating relations in database
        :return:
        """

        srp_requests = AaSrpRequest.objects.filter(ship=None)
        requests_count = srp_requests.count()

        self.stdout.write(
            self.style.WARNING(f"{requests_count} SRP requests need to be updated")
        )

        for srp_request in srp_requests:
            request_code = srp_request.request_code
            self.stdout.write(f"Updating SRP request {request_code}")

            try:
                srp_request__ship = EveType.objects.get(name=srp_request.ship_name)
            except EveType.DoesNotExist:
                srp_kill_link = AaSrpManager.get_kill_id(srp_request.killboard_link)

                (ship_type_id, ship_value, victim_id) = AaSrpManager.get_kill_data(
                    srp_kill_link
                )

                (
                    srp_request__ship,
                    created_from_esi,
                ) = EveType.objects.get_or_create_esi(id=ship_type_id)

            srp_request.ship = srp_request__ship
            srp_request.save()

    def handle(self, *args, **options):
        """
        ask before running ...
        :param args:
        :param options:
        """

        self.stdout.write(
            "This will update the relations between various tables in the database."
        )

        user_input = get_input("Are you sure you want to proceed? (yes/no)?")

        if user_input == "yes":
            self.stdout.write("Starting migration. Please stand by.")
            self._update_relations()
            self.stdout.write(self.style.SUCCESS("Update complete!"))
        else:
            self.stdout.write(self.style.WARNING("Aborted."))
