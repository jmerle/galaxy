import posixpath
import uuid

import google.cloud.storage as storage
from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models, transaction

import siarnaq.api.refs as refs
from siarnaq.api.teams.managers import TeamQuerySet


class Rating(models.Model):
    """
    An immutable database model for a Penalized Elo rating.

    While only intended for two-player games, this model computes rating changes for
    arbitrary N-player games. This is purely for the sake of potential future
    extensibility. The actual outputs here for games with more than 2 players may be
    nonsensical.
    """

    mean = models.FloatField(default=settings.TEAMS_ELO_INITIAL)
    """The Elo rating mean."""

    n = models.PositiveIntegerField(default=0)
    """The number of rated games played before this rating."""

    value = models.FloatField(default=0)
    """The penalized Elo value of this rating."""

    def save(self, *args, **kwargs):
        """Save a rating object, ensuring the penalized value is correct."""
        self.value = (
            self.mean
            - settings.TEAMS_ELO_INITIAL * settings.TEAMS_ELO_PENALTY**self.n
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.value:.0f}"

    def step(self, opponent_ratings, score):
        """Produce the new rating after a specific match is played."""
        e_self = self.expected_score(opponent_ratings)
        new_mean = self.mean + settings.TEAMS_ELO_K * (score - e_self)
        return Rating.objects.create(
            mean=new_mean,
            n=self.n + 1,
        )

    def expected_score(self, opponent_ratings):
        """Return the expected score against a given set of opponents."""
        total = 0
        for r in opponent_ratings:
            diff = self.mean - r.mean
            total += 1 / (1 + 10 ** (-diff / settings.TEAMS_ELO_SCALE))
        return total / len(opponent_ratings)


class TeamStatus(models.TextChoices):
    """
    An immutable type enumerating the possible varieties of teams.
    """

    REGULAR = "R"
    """A regular team consisting of regular members."""

    INACTIVE = "X"
    """
    A regular team with no remaining members.
    Inactive teams cannot be reactivated and are only kept as archival data.
    """

    STAFF = "S"
    """
    A team with staff privileges that can play matches requested by regular teams.
    Staff teams do not have ratings.
    """

    INVISIBLE = "O"
    """
    A team with staff privileges that is invisible to regular users.
    Invisible teams are useful for testing purposes.
    """


def make_team_join_key():
    return uuid.uuid4().hex[:16]


class Team(models.Model):
    """
    A database model for a team participating in an episode.
    """

    episode = models.ForeignKey(
        refs.EPISODE_MODEL,
        on_delete=models.PROTECT,
        related_name="teams",
    )
    """The episode to which this team belongs."""

    name = models.CharField(
        max_length=32,
        validators=[RegexValidator(r"^[ -~]*$", message="Use ASCII characters only.")],
    )
    """The name of the team."""

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="teams", blank=True
    )
    """The users who belong to this team."""

    join_key = models.SlugField(default=make_team_join_key, editable=False)
    """A passcode for users to join the team. Generated by a signal upon save."""

    status = models.CharField(
        max_length=1,
        choices=TeamStatus.choices,
        default=TeamStatus.REGULAR,
    )
    """The type of the team."""

    objects = TeamQuerySet.as_manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["episode", "name"],
                name="team-unique-episode-name",
            )
        ]

    def __init__(self, *args, profile=None, **kwargs):
        """Construct a team object, ensuring it has a profile."""
        super().__init__(*args, **kwargs)
        if not hasattr(self, "profile"):
            profile = profile or {}
            self.profile = TeamProfile(**profile)

    def __str__(self):
        return self.name

    @transaction.atomic
    def save(self, *args, **kwargs):
        """Save a team object, ensuring it has a profile recorded in the database."""
        super().save(*args, **kwargs)
        if self.profile._state.adding:
            self.profile.save()

    def is_staff(self):
        """Check whether this is a team with staff privileges."""
        return self.status in {TeamStatus.STAFF, TeamStatus.INVISIBLE}

    def can_participate_tournament(self):
        """Check whether this team status can participate in a tournament."""
        return self.status == TeamStatus.REGULAR

    def has_active_submission(self):
        """Return whether this team has an active submission."""
        return self.submissions.filter(accepted=True).exists()

    def get_active_submission(self):
        """Return the current active submission belonging to the team."""
        return self.submissions.filter(accepted=True).order_by("-created").first()

    def get_non_staff_count(self):
        return self.members.filter(is_staff=False).count()


class TeamProfile(models.Model):
    """
    A database model for the profile information augmenting a team of users.
    """

    team = models.OneToOneField(
        Team,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="profile",
    )
    """The team being augmented by this profile."""

    quote = models.CharField(
        max_length=80,
        blank=True,
        validators=[RegexValidator(r"^[ -~]*$", message="Use ASCII characters only.")],
    )
    """The short quote written by the team, if any."""

    biography = models.TextField(max_length=1024, blank=True)
    """The biography provided by the team, if any."""

    has_avatar = models.BooleanField(default=False)
    """Whether the team has an uploaded avatar."""

    avatar_uuid = models.UUIDField(default=uuid.uuid4)
    """A unique ID to identify each new avatar upload."""

    rating = models.OneToOneField(Rating, on_delete=models.PROTECT)
    """The current rating of the team."""

    auto_accept_ranked = models.BooleanField(default=False)
    """Whether the team automatically accepts ranked match requests."""

    auto_accept_unranked = models.BooleanField(default=True)
    """Whether the team automatically accepts unranked match requests."""

    eligible_for = models.ManyToManyField(
        refs.ELIGIBILITY_CRITERION_MODEL, related_name="teams", blank=True
    )
    """The eligibility criteria that this team satisfies."""

    def save(self, *args, **kwargs):
        """Save to database, ensuring the profile has a rating."""
        if self._state.adding and self.rating_id is None:
            self.rating = Rating.objects.create()
        super().save(*args, **kwargs)

    def get_avatar_path(self):
        """Return the path of the avatar on Google cloud storage."""
        if not self.has_avatar:
            return None
        return posixpath.join("team", str(self.pk), "avatar.png")

    def get_avatar_url(self):
        """Return a cache-safe URL to the avatar."""
        # To circumvent caching of old avatars, we append a UUID that changes on each
        # update.
        if not self.has_avatar:
            return None

        client = storage.Client.create_anonymous_client()
        public_url = (
            client.bucket(settings.GCLOUD_BUCKET_PUBLIC)
            .blob(self.get_avatar_path())
            .public_url
        )
        # Append UUID to public URL to prevent caching on avatar update
        return f"{public_url}?{self.avatar_uuid}"


class ReferencePlayer(models.Model):
    """
    A database model for the information regarding a reference player that forms a
    requirement for passing the Battlecode class. Each requirement is of the form, "the
    student must be part of a team who has played a scrimmage on a precise set of maps
    S, and won on at least W of those maps."
    """

    episode = models.ForeignKey(
        refs.EPISODE_MODEL,
        on_delete=models.CASCADE,
        related_name="reference_players",
    )
    """The episode this reference player is relevant to."""

    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    """The team of the reference player."""

    maps = models.ManyToManyField(refs.MAP_MODEL)
    """The maps involved in this requirement."""

    min_score = models.PositiveSmallIntegerField()
    """The minimum number of maps to be won."""
