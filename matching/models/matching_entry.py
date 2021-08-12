from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from matching.validators import ListOfStringsValidator


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
        errors = {}
        if not self.album_adjectives and self.album_adjectives != []:
            errors['album_adjectives'] = ValidationError('The album adjectives are not in a valid list.')
        if not self.album_musical_elements and self.album_musical_elements != []:
            errors['album_musical_elements'] = ValidationError('The album musical elements are not in a valid list.')
        if not self.match_adjectives and self.match_adjectives != []:
            errors['match_adjectives'] = ValidationError('The match adjectives are not in a valid list.')
        if not self.match_musical_elements and self.match_musical_elements != []:
            errors['match_musical_elements'] =  ValidationError('The match musical elements are not in a valid list.')
        if errors:
            raise ValidationError(errors)

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='matching_entry'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # SECTION 1 - MY ALBUM REQUIRED

    SPOTIFY_ID_REGEX_VALIDATOR = RegexValidator('^[a-zA-Z0-9]{22}$', "Your Spotify ID was invalid.")

    # Q1 - What album are you recommending?
    #    - Make the exchange interesting! Recommend something different.
    album_spotify_id = models.CharField(
        max_length=22,
        validators=[SPOTIFY_ID_REGEX_VALIDATOR],
        help_text="What album are you recommending?"
    )

    # TODO: Foreign key to a spotify album object (that can be null)

    # Q2 - What macro genre would you classify the album you're recommending in?
    #    - Don't worry too much about perfect categorisation - just write what best fits!
    class MacroGenres(models.TextChoices):
        CFB = 'Country, Folk & Blues', 'Country, Folk & Blues'
        CLASSICAL = 'Classical', 'Classical'
        ED = 'Electronic and Dance', 'Electronic and Dance'
        HHRB = 'Hip Hop and R&B', 'Hip Hop and R&B'
        IIPEPP = 'Indie, Indie Pop, Emo and Pop Punk', 'Indie, Indie Pop, Emo and Pop Punk'
        JSNSF = 'Jazz, Soul, Neo-Soul and Funk', 'Jazz, Soul, Neo-Soul and Funk'
        POP = 'Pop', 'Pop'
        RMPNPPRI = 'Rock, Metal, Punk, Noise, Prog, Post-Rock, Industrial', 'Rock, Metal, Punk, Noise, Prog, Post-Rock, Industrial',
        OTHER = 'Other', 'Other'
    album_macrogenre = models.CharField(
        max_length=60,
        choices=MacroGenres.choices,
        help_text="What macro genre would you classify the album you're recommending in?"
    )
    # Q3 - How would you describe your album?
    album_description = models.TextField(
        help_text="How would you describe your album?"
    )

    # SECTION 2 - MY ALBUM OPTIONAL

    # Q1 - What microgenre(s) would you associate with your album?
    album_microgenre = models.CharField(
        max_length=200,
        blank=True,
        help_text="What microgenre(s) would you associate with your album?"
    )

    # Q2 - What decade does your album most sound like?
    class MusicDecades(models.TextChoices):
        NO_CHOICE = '', 'No Choice'
        PRE50S = 'Pre-50s', 'Pre-50s'
        D50S = '50s', '50s'
        D60S = '60s', '60s'
        D70S = '70s', '70s'
        D80S = '80s', '80s'
        D90S = '90s', '90s'
        D00S = '00s', '2000s'
        D10S20S = '10s-20s', '2010s-20s'
    album_decade = models.CharField(
        max_length=10,
        choices=MusicDecades.choices,
        blank=True,
        help_text="What decade does your album most sound like?"
    )

    ADJECTIVE_CHOICES = (
        'All over the place',
        'Ambitious/epic',
        'Angry/passionate/intense',
        'Chill/slow-paced/ballads',
        'Classic/influential',
        'Concept album',
        'Danceable/festival',
        'Disturbing/disgusting',
        'Domestic/wholesome/sincere',
        'Dreamy/meditative',
        'Empowering/proud',
        'Experimental/strange',
        'Fast-paced/Upbeat',
        'Funny',
        'Happy/joyful',
        'Heartbreaking/break-up',
        'Instrumental (i.e. no lyrics)',
        'Loud',
        'LGBT',
        'Lyrical',
        'Musically complex',
        'Musically simple/acoustic',
        'Political',
        'Psychedelic',
        'Quiet',
        'Romantic',
        'Sad/melancholic/sombre',
        'Screaming/shouting',
        'Silly',
        'Summery',
        'Vibey',
        'Wintery'
    )
    # Q3 - What adjectives would you use to describe your album?
    # This is a multiselect but we'll let the client choose the options available
    # Since we don't need them to take a fixed set of values
    album_adjectives = models.JSONField(
        validators=[ListOfStringsValidator(
            'Your album adjectives were invalid.',
            'album adjectives',
            choices=ADJECTIVE_CHOICES
        )],
        default=list,
        blank=True,
        help_text="What adjectives would you use to describe your album? "
                  f"Valid choices are <select><option>{'</option><option>'.join(ADJECTIVE_CHOICES)}</option></select>"
    )

    # Q4 - What musical elements/instruments do you love the most about your album?
    # Vocals, Guitar, Drums, Bass/bassline, Piano/keyboard, Synths/beats, Brass, Crazy sounds!, Other (free choice)
    album_musical_elements = models.JSONField(
        validators=[ListOfStringsValidator('Your album musical elements are invalid.')],
        default=list,
        blank=True,
        help_text="What musical elements/instruments do you love the most about your album?"
    )

    # Q5 - What country does your album originate from?
    album_country = models.CharField(
        max_length=70,  # The United Kingdom of Great Britain and Northern Ireland <-- 56 chars
        blank=True,
        help_text="What country does your album originate from?"
    )

    # SECTION 3 - ARTIST RECOMMENDATIONS

    # Q1 - What artists do you recommend?
    artist_1_spotify_id = models.CharField(
        max_length=22,
        validators=[SPOTIFY_ID_REGEX_VALIDATOR],
        help_text="What artists do you recommend?"
    )
    # TODO: Foreign key it
    artist_2_spotify_id = models.CharField(
        max_length=22,
        validators=[SPOTIFY_ID_REGEX_VALIDATOR],
        help_text="What artists do you recommend?"
    )
    # TODO: Foreign key it

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

    class OKLevel(models.TextChoices):
        TOTALLY_OK = 'Totally OK', 'Totally OK'
        OK_BUT_PREFERABLY_NOT = 'Medium OK', 'OK but preferably not'
        NOT_OK = 'Not OK', 'Not OK'

    # Q2a - If you were matched with a non-musician person who wants to have a chat, would you mind?
    #     - If you wouldn't talk with a non-musician who wants to have a chat, select NOT OKAY.
    #     - Please be honest in this question.
    #     - We use this to make sure that people who want to talk will DEFINITELY be matched
    #       with someone who would talk with them at least once.
    #     - We don't want any abandoned matches :'(
    # This question is for REC ONLY and NETWORKERS.
    # If a person is TALKING => TOTALLY OK
    minds_talking = models.CharField(
        max_length=20,
        choices=OKLevel.choices,
        help_text='If you were matched with a non-musician person who wants to have a chat, would you mind?'
    )
    # Q2b - If you were matched with a non-musician person who didn't want to talk, would you mind?
    #     - Aka would you mind an album exchange and not talk
    # This question is for TALKING and NETWORKERS
    minds_not_talking = models.CharField(
        max_length=20,
        choices=OKLevel.choices,
        help_text="If you were matched with a non-musician person who didn't want to talk, would you mind?"
    )
    # HOW TO DECIDE TALK TYPE COMPATIBILITY
    # If both people are the same
    #   SUGGEST "Ideal"
    # If neither is a NETWORKER
    #   Look at how okay each person would be with the other as a match
    #   SUGGEST the maximum of both of those
    # If one and one only is a NETWORKER
    #   Look at how okay the networker is with the other person
    #   SUGGEST that

    class AgreementLevel(models.IntegerChoices):
        STRONGLY_AGREE = 2, 'Strongly Agree'
        SOMEWHAT_AGREE = 1, 'Somewhat Agree'
        NEITHER = 0, 'Neither'
        SOMEWHAT_DISAGREE = -1, 'Somewhat Disagree'
        STRONGLY_DISAGREE = -2, 'Strongly Disagree'
    # Q3 - To what extent do you agree with the statement "I'm adventurous and want to try something very new"
    adventurous = models.IntegerField(
        choices=AgreementLevel.choices,
        help_text='To what extent do you agree with the statement '
                  '"I\'m adventurous and want to try something very new".'
    )

    # Q4 - To what extent do you agree with the statement
    #      "I want to find another person who listens to my type of music, even if I already know the album"
    person_above_adventure = models.IntegerField(
        choices=AgreementLevel.choices,
        help_text='To what extent do you agree with the statement '
                  '"I want to find another person who listens to my type of music, even if I already know the album".'
    )

    # Q5 - Would you be okay with being matched in a triplet?
    #    - Note: We cannot guarantee that you will be put in a pair
    triplet = models.BooleanField(
        help_text="Would you be okay with being matched in a triplet?"
    )

    # Q6 - Which macrogenres would you be happy to receive recommendations from, in order of preference?
    #    - Select at least two
    match_macrogenre = models.JSONField(
        validators=[ListOfStringsValidator(
            'Your match macrogenre was invalid, you might not have selected enough genres.',
            'match macrogenre',
            choices=MacroGenres.choices,
            min_items=2
        )],
        help_text="Which macrogenres would you be happy to receive recommendations from, in order of preference? "
                  "Select at least 2. Valid choices are "
                  f"<select><option>{'</option><option>'.join(x[0] + ' (' + x[1] + ')' for x in MacroGenres.choices)}</option></select>"
    )

    # Q7 - What language preferences do you have for your match?
    # On the client side show English as the default.
    match_language = models.CharField(
        max_length=80,
        default='English',
        help_text="What language preferences do you have for your match?"
    )

    # Q8 - Are you happy to receive an instrumental (no vocals) album?
    match_instrumental = models.BooleanField(
        help_text="Are you happy to receive an instrumental (no vocals) album?"
    )

    # Q9 - What kind of album would you like to be matched with?
    match_description = models.TextField(
        help_text="What kind of album would you like to be matched with?"
    )

    # SECTION 5 - Match Optional

    # Q1 - Which microgenre(s) do you most want a match from?
    match_microgenre = models.CharField(
        max_length=100,
        blank=True,
        help_text="Which microgenre(s) do you most want a match from?"
    )

    # Q2 - Select the adjectives you want your match to embody.
    match_adjectives = models.JSONField(
        validators=[ListOfStringsValidator(
            'Your match adjectives are invalid.',
            'match adjectives',
            choices=ADJECTIVE_CHOICES
        )],
        default=list,
        blank=True,
        help_text="Select the adjectives you want your match to embody."
                  f"Valid choices are <select><option>{'</option><option>'.join(ADJECTIVE_CHOICES)}</option></select>"
    )

    # Q4 - What musical elements/instruments do you want your match to have
    # Vocals, Guitar, Drums, Bass/bassline, Piano/keyboard, Synths/beats, Brass, Crazy sounds!, Other (free choice)
    match_musical_elements = models.JSONField(
        validators=[ListOfStringsValidator('Your match musical elements are invalid.')],
        default=list,
        blank=True,
        help_text="What musical elements/instruments do you want your match to have?"
    )

    # Q5 - Are there any particular country(/ies) that you want your match to be from?
    match_country = models.CharField(
        max_length=100,
        blank=True,
        help_text="Are there any particular country(/ies) that you want your match album to be from?"
    )

    # FINAL QUESTION
    # QF - What do you want to get out of this?
    what_get_out = models.TextField(
        help_text="What do you want to get out of this?",
        blank=True
    )
