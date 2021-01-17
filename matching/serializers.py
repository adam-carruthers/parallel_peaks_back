from rest_framework import serializers
from .models import MatchingEntry
from .validators import ListOfStringsValidator


class MatchingEntrySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    album_adjectives = serializers.ListField(
        child=serializers.CharField(
            trim_whitespace=True,
            allow_blank=False
        ),
        allow_empty=True,
        default=list,
        validators=[ListOfStringsValidator(
            'Your album macrogenre was not formatted correctly.',
            'album macrogenre',
            choices=MatchingEntry.MacroGenres.choices
        )],
        help_text="What adjectives would you use to describe your album? "
                  f"Valid choices are "
                  "<select><option>"
                  f"{'</option><option>'.join(MatchingEntry.ADJECTIVE_CHOICES)}"
                  "</option></select>"
    )
    album_musical_elements = serializers.ListField(
        child=serializers.CharField(
            trim_whitespace=True,
            allow_blank=False
        ),
        allow_empty=True,
        default=list,
        help_text="What musical elements/instruments do you love the most about your album?"
    )
    match_macrogenre = serializers.ListField(
        min_length=2,
        allow_empty=False,
        validators=[ListOfStringsValidator(
            'Your match macrogenre was invalid, you might not have selected enough genres.',
            'match macrogenre',
            choices=MatchingEntry.MacroGenres.choices,
            min_items=2
        )],
        help_text="Which macrogenres would you be happy to receive recommendations from, in order of preference? "
                  "Select at least 2. Valid choices are "
                  "<select><option>"
                  f"{'</option><option>'.join(x[0] + ' (' + x[1] + ')' for x in MatchingEntry.MacroGenres.choices)}"
                  f"</option></select>"
    )
    match_adjectives = serializers.ListField(
        child=serializers.CharField(
            trim_whitespace=True,
            allow_blank=False
        ),
        allow_empty=True,
        default=list,
        validators=[ListOfStringsValidator(
            'Your album macrogenre was not formatted correctly.',
            'album macrogenre',
            choices=MatchingEntry.MacroGenres.choices
        )],
        help_text="What adjectives would you use to describe your album? "
                  f"Valid choices are "
                  "<select><option>"
                  f"{'</option><option>'.join(MatchingEntry.ADJECTIVE_CHOICES)}"
                  "</option></select>"
    )
    match_musical_elements = serializers.ListField(
        child=serializers.CharField(
            trim_whitespace=True,
            allow_blank=False
        ),
        allow_empty=True,
        default=list,
        help_text="What musical elements/instruments do you love the most about your album?"
    )

    class Meta:
        model = MatchingEntry
        fields = [
            'user', 'created_at', 'talkativity_preference', 'minds_talking', 'minds_not_talking',
            'album_spotify_id', 'album_macrogenre', 'album_description', 'album_microgenre',
            'album_decade', 'album_adjectives', 'album_musical_elements', 'album_country',
            'artist_1_spotify_id', 'artist_2_spotify_id', 'adventurous', 'person_above_adventure', 'match_macrogenre',
            'match_language', 'match_instrumental', 'match_description', 'match_microgenre',
            'match_adjectives', 'match_musical_elements', 'match_country', 'what_get_out'
        ]
