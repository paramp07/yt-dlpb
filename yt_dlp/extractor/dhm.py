from .common import InfoExtractor
from ..utils import parse_duration

class DHMIE(InfoExtractor):
    # Indicates whether this extractor is currently working
    _WORKING = False
    
    # Description of this information extractor
    IE_DESC = 'Filmarchiv - Deutsches Historisches Museum'
    
    # Valid URL pattern to match URLs from the Deutsches Historisches Museum film archive
    _VALID_URL = r'https?://(?:www\.)?dhm\.de/filmarchiv/(?:[^/]+/)+(?P<id>[^/]+)'
    
    # Test cases to verify the functionality of this information extractor
    _TESTS = [{
        'url': 'http://www.dhm.de/filmarchiv/die-filme/the-marshallplan-at-work-in-west-germany/',
        'md5': '11c475f670209bf6acca0b2b7ef51827',
        'info_dict': {
            'id': 'the-marshallplan-at-work-in-west-germany',
            'ext': 'flv',
            'title': 'MARSHALL PLAN AT WORK IN WESTERN GERMANY, THE',
            'description': 'md5:1fabd480c153f97b07add61c44407c82',
            'duration': 660,
            'thumbnail': r're:^https?://.*\.jpg$',
        },
    }, {
        'url': 'http://www.dhm.de/filmarchiv/02-mapping-the-wall/peter-g/rolle-1/',
        'md5': '09890226332476a3e3f6f2cb74734aa5',
        'info_dict': {
            'id': 'rolle-1',
            'ext': 'flv',
            'title': 'ROLLE 1',
            'thumbnail': r're:^https?://.*\.jpg$',
        },
    }]

    def _real_extract(self, url):
        # Match the provided URL and extract the playlist ID
        playlist_id = self._match_id(url)

        # Download the webpage content
        webpage = self._download_webpage(url, playlist_id)

        # Search for the playlist URL within the webpage
        playlist_url = self._search_regex(
            r"file\s*:\s*'([^']+)'", webpage, 'playlist url')

        # Extract the playlist entries from the playlist URL
        entries = self._extract_xspf_playlist(playlist_url, playlist_id)

        # Search for the title within the webpage
        title = self._search_regex(
            [r'dc:title="([^"]+)"', r'<title> &raquo;([^<]+)</title>'],
            webpage, 'title').strip()
        
        # Search for the description within the webpage
        description = self._html_search_regex(
            r'<p><strong>Description:</strong>(.+?)</p>',
            webpage, 'description', default=None)
        
        # Parse the duration of the content from the webpage
        duration = parse_duration(self._search_regex(
            r'<em>Length\s*</em>\s*:\s*</strong>([^<]+)',
            webpage, 'duration', default=None))

        # Update the first entry with the extracted title, description, and duration
        entries[0].update({
            'title': title,
            'description': description,
            'duration': duration,
        })

        # Return the playlist result with the extracted entries and playlist ID
        return self.playlist_result(entries, playlist_id)

