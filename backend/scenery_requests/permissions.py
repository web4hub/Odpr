from rest_framework import permissions

ADMIN_REQUEST_DETAIL_DATA_ACCESS = (
	'date_created',
	'author',
	'title',
	'description',
	'filter_properties',
	'visit_count',
	'privacy_setting',
	'is_closed',
	'tags',
	'get_upvote_count',
	'get_downvote_count',
	'get_starred_count',
	'get_reported_count',
	'get_final_vote_number'
)
ADMIN_REQUEST_DETAIL_READ_ONLY_DATA_ACCESS = (
	'id',
	'date_created',
	'author',
	'visit_count',
	'get_upvote_count',
	'get_downvote_count',
	'get_starred_count',
	'get_reported_count',
	'get_final_vote_number'
)
ADMIN_REQUEST_DETAIL_DATA_ACCESS_FULL = (
	'id',
) + ADMIN_REQUEST_DETAIL_DATA_ACCESS
ADMIN_REQUEST_LIST_DATA_ACCESS_FULL = (
	'id',
	'date_created',
	'author',
	'title',
	'description',
	'filter_properties',
	'visit_count',
	'privacy_setting',
	'is_closed',
	'tags',
	'get_upvote_count',
	'get_downvote_count',
	'get_starred_count',
	'get_reported_count',
	'get_final_vote_number'
)
ADMIN_REQUEST_LIST_READ_ONLY_DATA_ACCESS = ADMIN_REQUEST_LIST_DATA_ACCESS_FULL

STAFF_REQUEST_DETAIL_DATA_ACCESS = (
	'date_created',
	'author',
	'title',
	'description',
	'filter_properties',
	'visit_count',
	'privacy_setting',
	'is_closed',
	'tags',
	'get_upvote_count',
	'get_downvote_count',
	'get_starred_count',
	'get_reported_count',
	'get_final_vote_number'
)
STAFF_REQUEST_DETAIL_READ_ONLY_DATA_ACCESS = (
	'id',
	'date_created',
	'author',
	'visit_count',
	'get_upvote_count',
	'get_downvote_count',
	'get_starred_count',
	'get_reported_count',
	'get_final_vote_number'
)
STAFF_REQUEST_DETAIL_DATA_ACCESS_FULL = (
	'id',
) + STAFF_REQUEST_DETAIL_DATA_ACCESS
STAFF_REQUEST_LIST_DATA_ACCESS_FULL = (
	'id',
	'date_created',
	'author',
	'title',
	'description',
	'filter_properties',
	'visit_count',
	'privacy_setting',
	'is_closed',
	'tags',
	'get_upvote_count',
	'get_downvote_count',
	'get_starred_count',
	'get_reported_count',
	'get_final_vote_number'
)
STAFF_REQUEST_LIST_READ_ONLY_DATA_ACCESS = STAFF_REQUEST_LIST_DATA_ACCESS_FULL

AUTHENTICATED_SELF_REQUEST_DETAIL_DATA_ACCESS = (
	'date_created',
	'author',
	'title',
	'description',
	'filter_properties',
	'visit_count',
	'privacy_setting',
	'is_closed',
	'tags',
	'get_starred_count',
	'get_final_vote_number'
)
AUTHENTICATED_SELF_REQUEST_DETAIL_READ_ONLY_DATA_ACCESS = (
	'id',
	'date_created',
	'author',
	'visit_count',
	'get_starred_count',
	'get_final_vote_number'
)
AUTHENTICATED_SELF_REQUEST_DETAIL_DATA_ACCESS_FULL = (
	'id',
) + AUTHENTICATED_SELF_REQUEST_DETAIL_DATA_ACCESS

AUTHENTICATED_OTHER_REQUEST_DETAIL_DATA_ACCESS = (
	'date_created',
	'author',
	'title',
	'description',
	'filter_properties',
	'visit_count',
	'is_closed',
	'tags',
	'get_starred_count',
	'get_final_vote_number'
)
AUTHENTICATED_OTHER_REQUEST_DETAIL_DATA_ACCESS_FULL = (
	'id',
) + AUTHENTICATED_OTHER_REQUEST_DETAIL_DATA_ACCESS
AUTHENTICATED_OTHER_REQUEST_DETAIL_READ_ONLY_DATA_ACCESS = AUTHENTICATED_OTHER_REQUEST_DETAIL_DATA_ACCESS_FULL

AUTHENTICATED_REQUEST_LIST_DATA_ACCESS_FULL = (
	'id',
	'date_created',
	'author',
	'title',
	'description',
	'filter_properties',
	'visit_count',
	'is_closed',
	'tags',
	'get_starred_count',
	'get_final_vote_number'
)
AUTHENTICATED_REQUEST_LIST_READ_ONLY_DATA_ACCESS = AUTHENTICATED_REQUEST_LIST_DATA_ACCESS_FULL

UNAUTHENTICATED_REQUEST_DETAIL_DATA_ACCESS = (
	'date_created',
	'author',
	'title',
	'description',
	'filter_properties',
	'visit_count',
	'is_closed',
	'tags',
	'get_starred_count',
	'get_final_vote_number'
)
UNAUTHENTICATED_REQUEST_DETAIL_DATA_ACCESS_FULL = (
	'id',
) + UNAUTHENTICATED_REQUEST_DETAIL_DATA_ACCESS
UNAUTHENTICATED_REQUEST_DETAIL_READ_ONLY_DATA_ACCESS = UNAUTHENTICATED_REQUEST_DETAIL_DATA_ACCESS_FULL

UNAUTHENTICATED_REQUEST_LIST_DATA_ACCESS_FULL = (
	'id',
	'date_created',
	'author',
	'title',
	'description',
	'filter_properties',
	'visit_count',
	'is_closed',
	'tags',
	'get_starred_count',
	'get_final_vote_number'
)
UNAUTHENTICATED_REQUEST_LIST_READ_ONLY_DATA_ACCESS = UNAUTHENTICATED_REQUEST_LIST_DATA_ACCESS_FULL
