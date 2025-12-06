from flask import Blueprint, jsonify, request
from datetime import datetime
from ...models.tables import ShortUrls
from ...extensions import db
from random import choice
import string
from ...constants.http_status_codes import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK

# Define the Blueprint
api_bp = Blueprint("api", __name__, url_prefix='/v1/api')

# Function to generate a random short_id
def generate_short_id(num_of_chars: int):
    """Function to generate short_id of specified number of characters"""
    return ''.join(choice(string.ascii_letters+string.digits) for _ in range(num_of_chars))

# Create a short URL
@api_bp.post('/')
def index():
      url = request.form.get('url') or request.get_json('url')

      if not url:
            return jsonify({'error': 'The URL is required!'}), HTTP_400_BAD_REQUEST

      short_id = generate_short_id(10)

      # Ensure the generated short_id is unique
      while ShortUrls.query.filter_by(short_id=short_id).first() is not None:
            short_id = generate_short_id(10)

      # Store the new short URL in the database
      new_link = ShortUrls(original_url=url, short_id=short_id, created_at=datetime.now())
      db.session.add(new_link)
      db.session.commit()
      # Construct the full short URL
      short_url = request.host_url + short_id

      return jsonify({'short_url': short_url}), HTTP_201_CREATED

# Get URL info by short_id
@api_bp.get('/<short_id>')
def get_url_info(short_id):
      link = ShortUrls.query.filter_by(short_id=short_id).first()
      if link:
            return jsonify({
                  'original_url': link.original_url,
                  'short_id': link.short_id,
                  'created_at': link.created_at
            }), HTTP_200_OK
      else:
            return jsonify({'error': 'Short URL not found'}), HTTP_404_NOT_FOUND
      
# Get all short URLs
@api_bp.get('/urls/all')
def get_all_urls():
      links = ShortUrls.query.all()
      all_links = [{
            'original_url': link.original_url,
            'short_id': link.short_id,
            'created_at': link.created_at
      } for link in links]
      return jsonify(all_links), HTTP_200_OK


# Improvement ideas:
# 1. Add pagination to the get_all_urls endpoint to handle large datasets.
# 2. Implement rate limiting to prevent abuse of the URL shortening service.
# 3. Add user authentication to allow users to manage their own short URLs.
# 4. Include analytics features, such as tracking the number of clicks on each short URL.
# 5. Allow users to customize their short_id instead of generating a random one.
# 6. Implement error handling for database operations to ensure robustness.
