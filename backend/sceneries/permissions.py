from rest_framework import permissions

ADMIN_SCENERY_DETAIL_DATA_ACCESS = (
	'date_created',
	'author',
	'title',
	'description',
	'filter_properties',
	'visit_count',
	'download_count',
	'privacy_setting',
	'is_closed',
	'tags',
	'get_upvote_count',
	'get_downvote_count',
	'get_starred_count',
	'get_reported_count',
	'get_final_vote_number',
	'get_images',
	'get_files'
)
ADMIN_SCENERY_DETAIL_READ_ONLY_DATA_ACCESS = (
	'id',
	'date_created',
	'author',
	'visit_count',
	'download_count',
	'get_upvote_count',
	'get_downvote_count',
	'get_starred_count',
	'get_reported_count',
	'get_final_vote_number',
	'get_images',
	'get_files'
)
ADMIN_SCENERY_DETAIL_DATA_ACCESS_FULL = (
	'id',
) + ADMIN_SCENERY_DETAIL_DATA_ACCESS
ADMIN_SCENERY_LIST_DATA_ACCESS_FULL = (
	'id',
	'date_created',
	'author',
	'title',
	'description',
	'filter_properties',
	'visit_count',
	'download_count',
	'privacy_setting',
	'is_closed',
	'tags',
	'get_upvote_count',
	'get_downvote_count',
	'get_starred_count',
	'get_reported_count',
	'get_final_vote_number',
	'get_images',
	'get_files'
)
ADMIN_SCENERY_LIST_READ_ONLY_DATA_ACCESS = ADMIN_SCENERY_LIST_DATA_ACCESS_FULL

STAFF_SCENERY_DETAIL_DATA_ACCESS = (
	'date_created',
	'author',
	'title',
	'description',
	'filter_properties',
	'visit_count',
	'download_count',
	'privacy_setting',
	'is_closed',
	'tags',
	'get_upvote_count',
	'get_downvote_count',
	'get_starred_count',
	'get_reported_count',
	'get_final_vote_number',
	'get_images',
	'get_files'
)
STAFF_SCENERY_DETAIL_READ_ONLY_DATA_ACCESS = (
	'id',
	'date_created',
	'author',
	'visit_count',
	'download_count',
	'get_upvote_count',
	'get_downvote_count',
	'get_starred_count',
	'get_reported_count',
	'get_final_vote_number',
	'get_images',
	'get_files'
)
STAFF_SCENERY_DETAIL_DATA_ACCESS_FULL = (
	'id',
) + STAFF_SCENERY_DETAIL_DATA_ACCESS
STAFF_SCENERY_LIST_DATA_ACCESS_FULL = (
	'id',
	'date_created',
	'author',
	'title',
	'description',
	'filter_properties',
	'visit_count',
	'download_count',
	'privacy_setting',
	'is_closed',
	'tags',
	'get_upvote_count',
	'get_downvote_count',
	'get_starred_count',
	'get_reported_count',
	'get_final_vote_number',
	'get_images',
	'get_files'
)
STAFF_SCENERY_LIST_READ_ONLY_DATA_ACCESS = STAFF_SCENERY_LIST_DATA_ACCESS_FULL

AUTHENTICATED_SELF_SCENERY_DETAIL_DATA_ACCESS = (
	'date_created',
	'author',
	'title',
	'description',
	'filter_properties',
	'visit_count',
	'download_count',
	'privacy_setting',
	'is_closed',
	'tags',
	'get_starred_count',
	'get_final_vote_number',
	'get_images',
	'get_files'
)
AUTHENTICATED_SELF_SCENERY_DETAIL_READ_ONLY_DATA_ACCESS = (
	'id',
	'date_created',
	'author',
	'visit_count',
	'download_count',
	'get_starred_count',
	'get_final_vote_number',
	'get_images',
	'get_files'
)
AUTHENTICATED_SELF_SCENERY_DETAIL_DATA_ACCESS_FULL = (
	'id',
) + AUTHENTICATED_SELF_SCENERY_DETAIL_DATA_ACCESS

AUTHENTICATED_OTHER_SCENERY_DETAIL_DATA_ACCESS = (
	'date_created',
	'author',
	'title',
	'description',
	'filter_properties',
	'visit_count',
	'download_count',
	'is_closed',
	'tags',
	'get_starred_count',
	'get_final_vote_number',
	'get_images',
	'get_files'
)
AUTHENTICATED_OTHER_SCENERY_DETAIL_DATA_ACCESS_FULL = (
	'id',
) + AUTHENTICATED_OTHER_SCENERY_DETAIL_DATA_ACCESS
AUTHENTICATED_OTHER_SCENERY_DETAIL_READ_ONLY_DATA_ACCESS = AUTHENTICATED_OTHER_SCENERY_DETAIL_DATA_ACCESS_FULL

AUTHENTICATED_SCENERY_LIST_DATA_ACCESS_FULL = (
	'id',
	'date_created',
	'author',
	'title',
	'description',
	'filter_properties',
	'visit_count',
	'download_count',
	'is_closed',
	'tags',
	'get_starred_count',
	'get_final_vote_number',
	'get_images',
	'get_files'
)
AUTHENTICATED_SCENERY_LIST_READ_ONLY_DATA_ACCESS = AUTHENTICATED_SCENERY_LIST_DATA_ACCESS_FULL

UNAUTHENTICATED_SCENERY_DETAIL_DATA_ACCESS = (
	'date_created',
	'author',
	'title',
	'description',
	'filter_properties',
	'visit_count',
	'download_count',
	'is_closed',
	'tags',
	'get_starred_count',
	'get_final_vote_number',
	'get_images',
	'get_files'
)
UNAUTHENTICATED_SCENERY_DETAIL_DATA_ACCESS_FULL = (
	'id',
) + UNAUTHENTICATED_SCENERY_DETAIL_DATA_ACCESS
UNAUTHENTICATED_SCENERY_DETAIL_READ_ONLY_DATA_ACCESS = UNAUTHENTICATED_SCENERY_DETAIL_DATA_ACCESS_FULL

UNAUTHENTICATED_SCENERY_LIST_DATA_ACCESS_FULL = (
	'id',
	'date_created',
	'author',
	'title',
	'description',
	'filter_properties',
	'visit_count',
	'download_count',
	'is_closed',
	'tags',
	'get_starred_count',
	'get_final_vote_number',
	'get_images',
	'get_files'
)
UNAUTHENTICATED_SCENERY_LIST_READ_ONLY_DATA_ACCESS = UNAUTHENTICATED_SCENERY_LIST_DATA_ACCESS_FULL
