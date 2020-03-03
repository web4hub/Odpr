from rest_framework import permissions

ADMIN_DOCUMENT_DETAIL_DATA_ACCESS = (
	'date_created',
	'author',
	'title',
	'description',
	'visit_count',
	'privacy_setting',
	'tags'
)
ADMIN_DOCUMENT_DETAIL_READ_ONLY_DATA_ACCESS = (
	'id',
	'date_created',
	'author',
	'visit_count'
)
ADMIN_DOCUMENT_DETAIL_DATA_ACCESS_FULL = (
	'id',
) + ADMIN_DOCUMENT_DETAIL_DATA_ACCESS
ADMIN_DOCUMENT_LIST_DATA_ACCESS_FULL = (
	'id',
	'date_created',
	'author',
	'title',
	'description',
	'visit_count',
	'privacy_setting',
	'tags'
)
ADMIN_DOCUMENT_LIST_READ_ONLY_DATA_ACCESS = ADMIN_DOCUMENT_LIST_DATA_ACCESS_FULL

STAFF_DOCUMENT_DETAIL_DATA_ACCESS = (
	'date_created',
	'author',
	'title',
	'description',
	'visit_count',
	'privacy_setting',
	'tags'
)
STAFF_DOCUMENT_DETAIL_READ_ONLY_DATA_ACCESS = (
	'id',
	'date_created',
	'author',
	'visit_count'
)
STAFF_DOCUMENT_DETAIL_DATA_ACCESS_FULL = (
	'id',
) + STAFF_DOCUMENT_DETAIL_DATA_ACCESS
STAFF_DOCUMENT_LIST_DATA_ACCESS_FULL = (
	'id',
	'date_created',
	'author',
	'title',
	'description',
	'visit_count',
	'privacy_setting',
	'tags'
)
STAFF_DOCUMENT_LIST_READ_ONLY_DATA_ACCESS = STAFF_DOCUMENT_LIST_DATA_ACCESS_FULL

AUTHENTICATED_SELF_DOCUMENT_DETAIL_DATA_ACCESS = (
	'date_created',
	'author',
	'title',
	'description',
	'visit_count',
	'privacy_setting',
	'tags'
)
AUTHENTICATED_SELF_DOCUMENT_DETAIL_READ_ONLY_DATA_ACCESS = (
	'id',
	'date_created',
	'author',
	'visit_count'
)
AUTHENTICATED_SELF_DOCUMENT_DETAIL_DATA_ACCESS_FULL = (
	'id',
) + AUTHENTICATED_SELF_DOCUMENT_DETAIL_DATA_ACCESS

AUTHENTICATED_OTHER_DOCUMENT_DETAIL_DATA_ACCESS = (
	'date_created',
	'author',
	'title',
	'description',
	'visit_count',
	'tags'
)
AUTHENTICATED_OTHER_DOCUMENT_DETAIL_DATA_ACCESS_FULL = (
	'id',
) + AUTHENTICATED_OTHER_DOCUMENT_DETAIL_DATA_ACCESS
AUTHENTICATED_OTHER_DOCUMENT_DETAIL_READ_ONLY_DATA_ACCESS = AUTHENTICATED_OTHER_DOCUMENT_DETAIL_DATA_ACCESS_FULL

AUTHENTICATED_DOCUMENT_LIST_DATA_ACCESS_FULL = (
	'id',
	'date_created',
	'author',
	'title',
	'description',
	'visit_count',
	'tags'
)
AUTHENTICATED_DOCUMENT_LIST_READ_ONLY_DATA_ACCESS = AUTHENTICATED_DOCUMENT_LIST_DATA_ACCESS_FULL

UNAUTHENTICATED_DOCUMENT_DETAIL_DATA_ACCESS = (
	'date_created',
	'author',
	'title',
	'description',
	'visit_count',
	'tags'
)
UNAUTHENTICATED_DOCUMENT_DETAIL_DATA_ACCESS_FULL = (
	'id',
) + UNAUTHENTICATED_DOCUMENT_DETAIL_DATA_ACCESS
UNAUTHENTICATED_DOCUMENT_DETAIL_READ_ONLY_DATA_ACCESS = UNAUTHENTICATED_DOCUMENT_DETAIL_DATA_ACCESS_FULL

UNAUTHENTICATED_DOCUMENT_LIST_DATA_ACCESS_FULL = (
	'id',
	'date_created',
	'author',
	'title',
	'description',
	'visit_count',
	'tags'
)
UNAUTHENTICATED_DOCUMENT_LIST_READ_ONLY_DATA_ACCESS = UNAUTHENTICATED_DOCUMENT_LIST_DATA_ACCESS_FULL
