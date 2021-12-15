from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class MatchingEntry(models.Model):
    class Meta:
        verbose_name_plural = 'Matching Entries'
        permissions = [  # TODO: Move these permissions to matching object
            ('is_matcher', 'Can make matching suggestions'),
            ('is_moderator', 'Can moderate matching suggestions')
        ]

    def clean(self):
        # Sadly, if the list values aren't lists but are falsey, they pass validation, even if they shouldn't
        # We fix that below
        if not self.tags and self.album_adjectives != []:
            raise ValidationError({"tags": "Tags is not formatted correctly."})

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='matching_entry'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # SECTION 1 - MY ALBUM REQUIRED

    # Q1 - What album are you recommending?
    #    - Make the exchange interesting! Recommend something different.
    album_artist = models.CharField(
        max_length=256,
        help_text="What is the artist of the album?"
    )
    album_name = models.CharField(
        max_length=256,
        help_text="What is the name of the album?"
    )
    album_image_small_url = models.CharField(
        max_length=256,
        blank=True,
        validators=[URLValidator]
    )
    album_image_medium_url = models.CharField(
        max_length=256,
        blank=True,
        validators=[URLValidator]
    )
    album_image_large_url = models.CharField(
        max_length=256,
        blank=True,
        validators=[URLValidator]
    )
    album_image_xlarge_url = models.CharField(
        max_length=256,
        blank=True,
        validators=[URLValidator]
    )
    album_lastfm_url = models.CharField(
        max_length=256,
        blank=True,
        validators=[URLValidator]
    )
    album_lastfm_should_rerun = models.BooleanField()

    # Add LastFM tags to tag list as well

    # Q2 - What macro genre would you classify the album you're recommending in?
    #    - Don't worry too much about perfect categorisation - just write what best fits!

    # ++ Add to tags ++

    # Q3 - How would you describe your album?
    album_description = models.TextField(
        help_text="How would you describe your album?"
    )

    # Was previously going to limit it to just these choices but why have that pain
    # Can use front end stuff to ensure that the choices are limited
    # class MacroGenres(models.TextChoices):
    #     CFB = 'Country, Folk & Blues', 'Country, Folk & Blues'
    #     CLASSICAL = 'Classical', 'Classical'
    #     ED = 'Electronic and Dance', 'Electronic and Dance'
    #     HHRB = 'Hip Hop and R&B', 'Hip Hop and R&B'
    #     IIPEPP = 'Indie, Indie Pop, Emo and Pop Punk', 'Indie, Indie Pop, Emo and Pop Punk'
    #     JSNSF = 'Jazz, Soul, Neo-Soul and Funk', 'Jazz, Soul, Neo-Soul and Funk'
    #     POP = 'Pop', 'Pop'
    #     RMPNPPRI = 'Rock, Metal, Punk, Noise, Prog, Post-Rock, Industrial', 'Rock, Metal, Punk, Noise, Prog, Post-Rock, Industrial',
    #     OTHER = 'Other', 'Other'

    # ++ Add to tags ++

    # SECTION 2 - MY ALBUM OPTIONAL

    # Q1 - What microgenre(s) would you associate with your album?

    # ++ Add to tags ++

    # Q2 - What decade does your album most sound like?

    # ++ Add to tags ++

    # Was going to limit it to just the following
    # Can just do that on the front end
    # class MusicDecades(models.TextChoices):
    #     NO_CHOICE = '', 'No Choice'
    #     PRE50S = 'Pre-50s', 'Pre-50s'
    #     D50S = '50s', '50s'
    #     D60S = '60s', '60s'
    #     D70S = '70s', '70s'
    #     D80S = '80s', '80s'
    #     D90S = '90s', '90s'
    #     D00S = '00s', '2000s'
    #     D10S20S = '10s-20s', '2010s-20s'

    # ++ Add to tags ++

    # ADJECTIVE_CHOICES = (
    #     'All over the place',
    #     'Ambitious/epic',
    #     'Angry/passionate/intense',
    #     'Chill/slow-paced/ballads',
    #     'Classic/influential',
    #     'Concept album',
    #     'Danceable/festival',
    #     'Disturbing/disgusting',
    #     'Domestic/wholesome/sincere',
    #     'Dreamy/meditative',
    #     'Empowering/proud',
    #     'Experimental/strange',
    #     'Fast-paced/Upbeat',
    #     'Funny',
    #     'Happy/joyful',
    #     'Heartbreaking/break-up',
    #     'Instrumental (i.e. no lyrics)',
    #     'Loud',
    #     'LGBT',
    #     'Lyrical',
    #     'Musically complex',
    #     'Musically simple/acoustic',
    #     'Political',
    #     'Psychedelic',
    #     'Quiet',
    #     'Romantic',
    #     'Sad/melancholic/sombre',
    #     'Screaming/shouting',
    #     'Silly',
    #     'Summery',
    #     'Vibey',
    #     'Wintery'
    # )

    # Q3 - What adjectives would you use to describe your album?

    # ++ Add to tags ++

    # Q4 - What musical elements/instruments do you love the most about your album?
    # Vocals, Guitar, Drums, Bass/bassline, Piano/keyboard, Synths/beats, Brass, Crazy sounds!, Other (free choice)

    # ++ Add to tags ++

    # Q5 - What country does your album originate from?

    # SECTION 3 - ARTIST RECOMMENDATIONS

    # Q1 - What artists do you recommend?
    artist_1_name = models.CharField(
        max_length=256,
        help_text="What artists do you recommend?"
    )
    artist_2_name = models.CharField(
        max_length=256,
        help_text="What artists do you recommend?"
    )

    # SECTION 4 - What you want from your match (mandatory)

    # Q1 - What do you want to get out of the exchange?
    #    - If you select that you prefer someone to talk about music with or that you prefer to network with others
    #      then we expect that you would try to talk with your match at least one time!
    #    - Otherwise your poor match will be left abandoned :'(
    #    - Note: Even if you select recommendation only you will still be given the email of your match.
    class TalkativityPreference(models.TextChoices):
        PREFERS_TALKING = 'Talking', 'Talking and Recommendation'
        PREFERS_RECOMMENDATION_ONLY = 'Rec Only', 'Recommendation Only'
        PREFERS_NETWORKING = 'Networking', 'Networking'

    talkativity_preference = models.CharField(
        max_length=15,
        choices=TalkativityPreference.choices,
        help_text='What do you want to get out of the exchange?'
    )

    # Q2a - If you were matched with a non-musician person who wants to have a chat, how happy would you be on a scale of 0-5?
    #     - If you wouldn't talk with a non-musician who wants to have a chat, select NOT OKAY.
    #     - Please be honest in this question.
    #     - We use this to make sure that people who want to talk will DEFINITELY be matched
    #       with someone who would talk with them at least once.
    #     - We don't want any abandoned matches :'(
    # This question is for REC ONLY and NETWORKERS.
    # If a person is TALKING => TOTALLY OK
    minds_talking = models.IntegerField(
        help_text='If you were matched with a non-musician person who wants to have a chat, how happy would you be from 0 (very unhappy) to 5 (very happy and willing to chat)?',
        validators=[MinValueValidator(0, "Can't be less than 0"),
                    MaxValueValidator(5, "Can't be greater than 5")]
    )
    # Q2b - If you were matched with a non-musician person who didn't want to talk, would you mind?
    #     - Aka would you mind an album exchange and not talk
    # This question is for TALKING and NETWORKERS
    minds_not_talking = models.IntegerField(
        help_text="If you were matched with a non-musician person who doesn't want to have a chat, how happy would you be from 0 (very unhappy) to 5 (very happy and willing to just get a recommendation)?",
        validators=[MinValueValidator(0, "Can't be less than 0"),
                    MaxValueValidator(5, "Can't be greater than 5")]
    )
    # HOW TO DECIDE TALK TYPE COMPATIBILITY
    # If both people are the same
    #   SUGGEST "Ideal"
    # If one is a NETWORKER (and only one will be a networker)
    #   Look at how okay the networker is with the other person
    #   SUGGEST that
    # If neither is a NETWORKER
    #   Look at how okay each person would be with the other as a match
    #   SUGGEST the maximum of both of those

    # Q3 - To what extent do you agree with the statement "I'm adventurous and want to try something very new"
    adventurous = models.IntegerField(
        help_text='To what extent do you agree with the statement '
                  '"I\'m adventurous and want to try something very new" '
                  'from 0 (not adventurous) to 5 (very adventurous)',
        validators=[MinValueValidator(0, "Can't be less than 0"),
                    MaxValueValidator(5, "Can't be greater than 5")]
    )

    # Q4 - To what extent do you agree with the statement
    #      "I want to find another person who listens to my type of music, even if I already know the album"
    person_above_adventure = models.IntegerField(
        help_text='To what extent do you agree with the statement '
                  '"I want to find another person who listens to my type of music, even if I already know the album" '
                  "from 0 (please don't give me an album I know) to 5 (woop woop shared music buddies)",
        validators=[MinValueValidator(0, "Can't be less than 0"),
                    MaxValueValidator(5, "Can't be greater than 5")]
    )

    # Q6 - Which macrogenres would you be happy to receive recommendations from, in order of preference?
    #    - Select at least two

    # ++ add to tags ++

    # Q7 - What language preferences do you have for your match?
    # On the client side show English as the default.

    # ++ add to tags ++

    # Q8 - Are you happy to receive an instrumental (no vocals) album?

    # ++ add to tags ++

    # Q9 - What kind of album would you like to be matched with?
    match_description = models.TextField(
        help_text="What kind of album would you like to be matched with?"
    )

    # SECTION 5 - Match Optional

    # Q1 - Which microgenre(s) do you most want a match from?

    # ++ add to tags ++

    # Q2 - Select the adjectives you want your match to embody.

    # ++ add to tags ++

    # Q4 - What musical elements/instruments do you want your match to have
    # Vocals, Guitar, Drums, Bass/bassline, Piano/keyboard, Synths/beats, Brass, Crazy sounds!, Other (free choice)

    # ++ add to tags ++

    # Q5 - Are there any particular country(/ies) that you want your match to be from?

    # ++ add to tags ++

    # FINAL QUESTION
    # QF - What do you want to get out of this?
    what_get_out = models.TextField(
        help_text="What do you want to get out of this?",
        blank=True
    )


class MatchingTag(models.Model):
    matching_entry = models.ForeignKey(
        MatchingEntry, on_delete=models.CASCADE, related_name='all_tags')
    name = models.CharField(
        max_length=256
    )
    tagtype = models.CharField(
        max_length=256
    )
    describes_album = models.BooleanField(
        help_text='Does this tag describe the album (true) or what the matcher wants in their match (false)?'
    )
