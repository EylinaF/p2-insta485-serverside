"""Views, one for each Insta485 page."""
from insta485.views.index import show_index
from insta485.views.uploads import get_uploaded_file
from insta485.views.user import show_user_profile
from insta485.views.followers import show_followers
from insta485.views.following import show_following
from insta485.views.posts import show_post
from insta485.views.explore import show_explore
from insta485.views.login import show_login
from insta485.views.likes import update_likes
from insta485.views.comments import handle_comments
from insta485.views.posts_change import manage_posts