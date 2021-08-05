from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField

from .models import Artist, Genre, Album, Disc, Song, Playlist, Creator, CreatorSection, LibraryAlbum
from core.serializers import UserSerializer


class ArtistSerializer(ModelSerializer):
    group_members = SerializerMethodField()

    class Meta:
        model = Artist
        fields = ('name', 'is_group', 'group_members', 'avi', 'cover', 'bio', 'id')

    @staticmethod
    def get_group_members(obj):
        if hasattr(obj, 'is_group') and obj.is_group:
            return ArtistSerializer(obj.group_members.all(), many=True, read_only=True).data


class GenreSerializer(ModelSerializer):

    class Meta:
        model = Genre
        fields = ('title', 'description', 'avi', 'cover', 'id')


class SongSerializer(ModelSerializer):
    additional_artists = ArtistSerializer(many=True, read_only=True)

    class Meta:
        model = Song
        fields = ('id', 'track_no', 'title', 'explicit', 'length', 'file', 'likes', 'streams', 'additional_artists')


class DiscSerializer(ModelSerializer):
    songs = SongSerializer(source='song_set', many=True, read_only=True)

    class Meta:
        model = Disc
        fields = ('id', 'name', 'songs')


class AlbumSerializer(ModelSerializer):
    discs = DiscSerializer(source='disc_set', many=True)
    album_type = CharField(source='al_code')
    artists = ArtistSerializer(many=True)
    genre = GenreSerializer()

    def __init__(self, *args, **kwargs):
        no_discs = kwargs.pop('no_discs', False)

        super(AlbumSerializer, self).__init__(*args, **kwargs)

        if no_discs:
            self.fields.pop('discs')

    class Meta:
        model = Album
        fields = (
            'id', 'title', 'notes', 'genre', 'date_of_release', 'album_type', 'cover', 'likes', 'artists', 'copyright',
            'published', 'discs'
        )


class PlaylistSerializer(ModelSerializer):
    songs = SongSerializer(many=True, read_only=True, source='songs_by_order')
    modified = SerializerMethodField()

    class Meta:
        model = Playlist
        fields = (
            'id', 'title', 'description', 'owner', 'songs', 'likes', 'cover', 'cover_wide', 'timely_cover',
            'timely_cover_wide', 'modified'
        )

    @staticmethod
    def get_modified(obj):
        if hasattr(obj, 'modified') and obj.modified:
            return obj.modified.strftime('%Y-%m-%d')


class CreatorSectionSerializer(ModelSerializer):
    artists = ArtistSerializer(many=True)
    albums = AlbumSerializer(many=True)
    playlists = PlaylistSerializer(many=True)

    class Meta:
        model = CreatorSection
        fields = ('id', 'name', 'artists', 'albums', 'playlists')


class CreatorSerializer(ModelSerializer):
    users = UserSerializer(many=True)
    genres = GenreSerializer(many=True)

    class Meta:
        model = Creator
        fields = ('id', 'name', 'description', 'avi', 'cover', 'users', 'genres')


class LibraryAlbumSerializer(ModelSerializer):
    added = SerializerMethodField()
    modified = SerializerMethodField()
    album = AlbumSerializer(no_discs=True, read_only=True)
    songs = SongSerializer(many=True, read_only=True)

    class Meta:
        model = LibraryAlbum
        fields = ('id', 'added', 'modified', 'album', 'songs')

    @staticmethod
    def get_modified(obj):
        if hasattr(obj, 'modified') and obj.modified:
            return obj.modified.strftime('%Y-%m-%d')

    @staticmethod
    def get_added(obj):
        if hasattr(obj, 'added') and obj.added:
            return obj.added.strftime('%Y-%m-%d')