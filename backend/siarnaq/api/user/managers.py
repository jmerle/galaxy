from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db.models import Count, Exists, OuterRef, Q


class UserManager(DjangoUserManager):
    def with_passed(self, reference):
        from siarnaq.api.compete.models import Match, MatchParticipant

        return self.annotate(
            passed=Exists(
                Match.objects.annotate(
                    total_maps=Count("maps"),
                    reference_maps=Count(
                        "maps",
                        filter=Q(maps__pk__in=reference.maps.all()),
                    ),
                    has_reference_player=Exists(
                        MatchParticipant.objects.filter(
                            match=OuterRef("pk"),
                            team=reference.team,
                        )
                    ),
                ).filter(
                    reference_maps=reference.maps.count(),
                    total_maps=reference.maps.count(),
                    has_reference_player=True,
                    participants__team__members=OuterRef("pk"),
                    participants__score__gte=reference.min_score,
                )
            )
        )
